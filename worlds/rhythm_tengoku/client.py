import asyncio
from typing import TYPE_CHECKING, Dict, Set, Optional
import worlds._bizhawk as bizhawk

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient

try:
    from .utils import COORD_TO_LEVEL_ID
except Exception:
    COORD_TO_LEVEL_ID = {}

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class RhythmTengokuClient(BizHawkClient):
    system = "GBA"
    game = "Rhythm Tengoku"
    patch_suffix = ".aprhtg"

    GAME_SAVE_ADDR = 0x02000000

    _last_item_values: Dict[int, int]
    _last_level_ranks: Dict[int, int]
    _warned_bad_map: bool = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        await self._wait_for_bizhawk(ctx)
        try:
            await self._safe_read(ctx, [(0x100, 1, "ROM")])
        except Exception:
            pass

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self._last_item_values = {}
        self._last_level_ranks = {}

        return True

    async def on_connected(self, ctx: "BizHawkClientContext"):
        await super().on_connected(ctx)
        name = ctx.player_names.get(ctx.slot, f"Slot {ctx.slot}")
        print(f"[Rhythm Tengoku] Connected as {name} (team {ctx.team}, slot {ctx.slot})")

        sd = getattr(ctx, "slot_data", {}) or {}
        if "item_id_to_name" not in sd:
            print("[Rhythm Tengoku] WARNING: slot_data missing 'item_id_to_name'. "
                  "Add it in fill_slot_data() on the server side.")

        await self.sync_state(ctx)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        await self._wait_for_bizhawk(ctx)
        while True:
            try:
                mem = await self._safe_read(ctx, [(self.GAME_SAVE_ADDR, 1, "System Bus")])
                if mem[0][0] == 1 and not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

                mem = await self._safe_read(ctx, [(self.GAME_SAVE_ADDR + 0x22, 3, "System Bus")])
                x, y, rank = mem[0]
                if rank != 0xFF:
                    await self._safe_write(ctx, [(self.GAME_SAVE_ADDR + 0x24, [0xFF], "System Bus")])
                    lvl_id = COORD_TO_LEVEL_ID.get((x, y))
                    if lvl_id is not None and rank in (0x04, 0x05):
                        ok_loc = lvl_id * 3 + 0
                        superb_loc = lvl_id * 3 + 1
                        to_check = []

                        if rank == 0x04:
                            if ok_loc not in ctx.locations_checked:
                                to_check.append(ok_loc)
                        elif rank == 0x05:
                            if ok_loc not in ctx.locations_checked:
                                to_check.append(ok_loc)
                            if superb_loc not in ctx.locations_checked:
                                to_check.append(superb_loc)

                        if to_check:
                            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": to_check}])
                            await self._apply_rank_to_ram(ctx, lvl_id, rank)
                
                await self.sync_state(ctx)

            except Exception as e:
                tb = getattr(e, "__traceback__", None)
                line = getattr(tb, "tb_lineno", "?")
                filename = getattr(tb, "tb_frame", None)
                if filename:
                    filename = filename.f_code.co_filename
                else:
                    filename = "?"
                print(f"[Rhythm Tengoku] Memory read failed: {e} at {filename}:{line}")
            await asyncio.sleep(ctx.watcher_timeout)

    async def on_items_received(self, ctx: "BizHawkClientContext") -> None:
        id2name = self._id2name(ctx)
        for it in ctx.items_received:
            item_id = self._to_item_id(ctx, it.item, id2name)
            if item_id is None:
                continue
            name = id2name.get(item_id)
            if not name or name == "Blinking Trap":
                continue
            await self._write_item_value(ctx, item_id, 0x03)
        await self.sync_state(ctx)

    async def sync_state(self, ctx: "BizHawkClientContext"):
        """Bring emulator RAM in line with server truth (items received + locations checked + goal)."""
        id2name = self._id2name(ctx)

        received_ids: Set[int] = set()
        for it in ctx.items_received:
            iid = self._to_item_id(ctx, it.item, id2name)
            if iid is None:
                continue
            nm = id2name.get(iid)
            if nm and nm != "Blinking Trap":
                received_ids.add(iid)

        for item_id in id2name.keys():
            target = 0x03 if item_id in received_ids else 0x02
            await self._write_item_value(ctx, item_id, target)

        best_rank_for_level: Dict[int, int] = {}
        for loc_id in ctx.locations_checked:
            lvl_id = loc_id // 3
            mod = loc_id % 3
            rank_val = 0x04 if mod == 0 else (0x05 if mod == 1 else None)
            if rank_val is None:
                continue
            best_rank_for_level[lvl_id] = max(rank_val, best_rank_for_level.get(lvl_id, 0x02))
        for lvl_id, rank_val in best_rank_for_level.items():
            await self._apply_rank_to_ram(ctx, lvl_id, rank_val)

        if await self.check_goal_condition(ctx):
            await self._safe_write(ctx, [(self.GAME_SAVE_ADDR, [1], "System Bus")])
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    async def check_goal_condition(self, ctx: "BizHawkClientContext") -> bool:
        """Goal: all selected goal levels cleared at the chosen rank or better"""
        sd = getattr(ctx, "slot_data", {}) or {}
        goal_levels = {int(v) for v in sd.get("goal_levels", [])}
        goal_type = sd.get("goal_type", 0)
        goal_rank_value = 0x04 if goal_type == 0 else 0x05
        if not goal_levels:
            return False

        reads = [(self.GAME_SAVE_ADDR + 0x26 + lvl, 1, "System Bus") for lvl in goal_levels]
        mem = await self._safe_read(ctx, reads)
        for (_, bytes_read) in mem:
            if bytes_read[0] < goal_rank_value:
                return False
        return True

    async def _wait_for_bizhawk(self, ctx: "BizHawkClientContext"):
        """Poll until Lua side is actually connected to the bridge."""
        while True:
            try:
                await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 1, "System Bus")])
                return
            except Exception:
                await asyncio.sleep(0.25)

    def _id2name(self, ctx: "BizHawkClientContext") -> Dict[int, str]:
        sd = getattr(ctx, "slot_data", {}) or {}
        m = sd.get("item_id_to_name", {}) or {}
        if not m:
            if not self._warned_bad_map:
                print("[Rhythm Tengoku] WARNING: slot_data.item_id_to_name missing/empty.")
                self._warned_bad_map = True
            return {}
        items = list(m.items())[:3]
        keys_num = all(isinstance(k, int) or (isinstance(k, str) and k.isdigit()) for k, _ in items)
        vals_num = all(isinstance(v, int) or (isinstance(v, str) and str(v).isdigit()) for _, v in items)
        if keys_num and not vals_num:
            out = {}
            for k, v in m.items():
                try:
                    out[int(k)] = str(v)
                except Exception:
                    continue
            return out
        if (not keys_num) and vals_num:
            out = {}
            for k, v in m.items():
                try:
                    out[int(v)] = str(k)
                except Exception:
                    continue
            return out
        if not self._warned_bad_map:
            print("[Rhythm Tengoku] WARNING: slot_data.item_id_to_name has unexpected shape; ignoring.")
            self._warned_bad_map = True
        return {}

    def _to_item_id(self, ctx: "BizHawkClientContext", obj, id2name: Dict[int, str]) -> Optional[int]:
        if isinstance(obj, int):
            return obj
        s = str(obj)
        if s.isdigit():
            return int(s)
        for iid, nm in id2name.items():
            if nm == s:
                return iid
        if not self._warned_bad_map:
            print(f"[Rhythm Tengoku] WARNING: could not resolve item id from '{s}'.")
            self._warned_bad_map = True
        return None

    async def _safe_read(self, ctx: "BizHawkClientContext", args):
        while True:
            try:
                return await bizhawk.read(ctx.bizhawk_ctx, args)
            except Exception as e:
                msg = str(e).lower()
                if ("before a connection" in msg or "connection reset" in msg or "broken pipe" in msg):
                    print("[Rhythm Tengoku] Lost BizHawk connection, waiting to reconnect...")
                    await self._wait_for_bizhawk(ctx)
                    continue
                raise

    async def _safe_write(self, ctx: "BizHawkClientContext", args):
        while True:
            try:
                return await bizhawk.write(ctx.bizhawk_ctx, args)
            except Exception as e:
                msg = str(e).lower()
                if ("before a connection" in msg or "connection reset" in msg or "broken pipe" in msg):
                    print("[Rhythm Tengoku] Lost BizHawk connection, waiting to reconnect...")
                    await self._wait_for_bizhawk(ctx)
                    continue
                raise

    async def _write_once(self, ctx: "BizHawkClientContext", addr: int, data: list):
        try:
            cur = await self._safe_read(ctx, [(addr, len(data), "System Bus")])
            if list(cur[0][1]) == data:
                return
        except Exception:
            pass
        await self._safe_write(ctx, [(addr, data, "System Bus")])

    async def _write_item_value(self, ctx: "BizHawkClientContext", item_id: int, value: int):
        prev = self._last_item_values.get(item_id)
        if prev == value:
            return
        await self._safe_write(ctx, [(self.GAME_SAVE_ADDR + 0x26 + item_id, [value], "System Bus")])
        self._last_item_values[item_id] = value

    async def _apply_rank_to_ram(self, ctx: "BizHawkClientContext", level_id: int, rank_val: int):
        if rank_val not in (0x04, 0x05):
            return
        prev = self._last_level_ranks.get(level_id, 0x02)
        newv = max(prev, rank_val)
        if newv == prev:
            return
        await self._safe_write(ctx, [(self.GAME_SAVE_ADDR + 0x26 + level_id, [newv], "System Bus")])
        self._last_level_ranks[level_id] = newv
