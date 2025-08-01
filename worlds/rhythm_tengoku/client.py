# await bizhawk.display_message(ctx.bizhawk_ctx, "MESSAGE IN GAME")
# ctx.command_processor.output(ctx.command_processor, "OUTPUT IN GUI CLIENT ARCHIPELAGO")

import asyncio
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

from .utils import COORD_TO_LEVEL_ID

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
                if result[0][0] == 1 and not ctx.finished_game:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                
                result = await bizhawk.read(ctx.bizhawk_ctx, [(self.GAME_COMPLETE_ADDR + 0x22, 3, "System Bus")])
                if result[0][2] != 0xff:
                    await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_COMPLETE_ADDR + 0x24, [0xff], "System Bus")])
                    lvlID = COORD_TO_LEVEL_ID.get((result[0][0], result[0][1]), None)
                    if lvlID is not None and result[0][2] != 0x00:
                        if result[0][2] == 0x04:
                            await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_COMPLETE_ADDR + 0x26 + lvlID, [0x04], "System Bus")])
                            #await bizhawk.display_message(ctx.bizhawk_ctx, f"Level ID: {lvlID} check gotten OK")
                        elif result[0][2] == 0x05:
                            await bizhawk.write(ctx.bizhawk_ctx, [(self.GAME_COMPLETE_ADDR + 0x26 + lvlID, [0x05], "System Bus")])
                            #await bizhawk.display_message(ctx.bizhawk_ctx, f"Level ID: {lvlID} check gotten SUPERB")

            except Exception as e:
                print(f"[rhythm_tengoku] Memory read failed: {e} at line {e.__traceback__.tb_lineno}")
            await asyncio.sleep(ctx.watcher_timeout)
