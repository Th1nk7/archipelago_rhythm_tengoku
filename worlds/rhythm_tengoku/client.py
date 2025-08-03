# Updated client.py

import asyncio
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

from .utils import COORD_TO_LEVEL_ID, location_id_to_name
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

class RhythmTengokuClient(BizHawkClient):
    system = "GBA"
    game = "Rhythm Tengoku"
    patch_suffix = ".aprhtg"

    GAME_SAVE_ADDR = 0x02000000  # Save data base address

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            _ = await bizhawk.read(ctx.bizhawk_ctx, [(0x100, 1, "ROM")])
        except Exception:
            pass

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = False
        ctx.watcher_timeout = 0.125

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        while True:
            try:
                result = await bizhawk.read(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR, 1, "System Bus")])
                if result[0][0] == 1 and not ctx.finished_game:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])

                result = await bizhawk.read(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR + 0x22, 3, "System Bus")])
                if result[0][2] != 0xff:
                    await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR + 0x24, [0xff], "System Bus")])
                    lvlID = COORD_TO_LEVEL_ID.get((result[0][0], result[0][1]), None)
                    if lvlID is not None and result[0][2] != 0x00:
                        ok_loc_id = lvlID * 3 + 0  # OK
                        superb_loc_id = lvlID * 3 + 1  # SUPERB

                        to_check = []
                        if result[0][2] == 0x04:
                            if ok_loc_id not in ctx.locations_checked:
                                to_check.append(ok_loc_id)
                        elif result[0][2] == 0x05:
                            if ok_loc_id not in ctx.locations_checked:
                                to_check.append(ok_loc_id)
                            if superb_loc_id not in ctx.locations_checked:
                                to_check.append(superb_loc_id)

                        if to_check:
                            await ctx.send_msgs([{ "cmd": "LocationChecks", "locations": to_check }])

                        await self.sync_state(ctx)

            except Exception as e:
                print(f"[rhythm_tengoku] Memory read failed: {e} at line {e.__traceback__.tb_lineno}")
            await asyncio.sleep(ctx.watcher_timeout)

    async def on_items_received(self, ctx: "BizHawkClientContext") -> None:
        for item in ctx.items_received:
            item_name = ctx.slot_data.item_id_to_name.get(item.item, None)
            if item_name in (None, "Blinking Trap"):
                continue  # Ignore filler
            await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR + 0x26 + item.item, [0x03], "System Bus")])

        await self.sync_state(ctx)

    async def on_connected(self, ctx: "BizHawkClientContext"):
        await super().on_connected(ctx)
        await self.sync_state(ctx)

    async def sync_state(self, ctx: "BizHawkClientContext"):
        received_items = set(item.item for item in ctx.items_received if ctx.slot_data.item_id_to_name.get(item.item) != "Blinking Trap")

        for item_id, item_name in ctx.slot_data.item_id_to_name.items():
            if item_name == "Blinking Trap":
                continue
            value = [0x03] if item_id in received_items else [0x02]
            await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR + 0x26 + item_id, value, "System Bus")])

        for loc_id in ctx.locations_checked:
            lvlID = loc_id // 3
            rank_mod = loc_id % 3
            if rank_mod == 0:
                val = [0x04]
            elif rank_mod == 1:
                val = [0x05]
            else:
                continue  # Ignore PERFECT
            await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR + 0x26 + lvlID, val, "System Bus")])

        goal_met = await self.check_goal_condition(ctx)
        if goal_met:
            await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR, [1], "System Bus")])

    async def check_goal_condition(self, ctx: "BizHawkClientContext") -> bool:
        goal_levels = set(ctx.slot_data.goal_levels)
        goal_rank_value = 0x04 if ctx.slot_data.goal_type == 0 else 0x05  # 0: clear, 1: superb

        for level_id in goal_levels:
            mem = await bizhawk.read(ctx.bizhawk_ctx, [(self.GAME_SAVE_ADDR + 0x26 + level_id, 1, "System Bus")])
            if mem[0][0] < goal_rank_value:
                return False
        return True
