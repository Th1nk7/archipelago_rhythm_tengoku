# await bizhawk.display_message(ctx.bizhawk_ctx, "MESSAGE IN GAME")
# ctx.command_processor.output(ctx.command_processor, "OUTPUT IN GUI CLIENT ARCHIPELAGO")

import asyncio
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

class RhythmTengokuClient(BizHawkClient):
    system = "GBA"
    game = "Rhythm Tengoku"
    patch_suffix = ".aprhtg"

    GAME_COMPLETE_ADDR = 0x02000000  # Replace with real value later

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Force a real read to ensure client registers
            _ = await bizhawk.read(ctx.bizhawk_ctx, [(0x100, 1, "ROM")])
        except Exception:
            pass  # Ignore read failure

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = False
        ctx.watcher_timeout = 0.125

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        while True:
            try:
                result = await bizhawk.read(ctx.bizhawk_ctx, [(self.GAME_COMPLETE_ADDR, 1, "System Bus")])
                value = result[0][0]
                if value == 1 and not ctx.finished_game:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
            except Exception as e:
                print(f"[rhythm_tengoku] Memory read failed: {e}")
            await asyncio.sleep(ctx.watcher_timeout)
