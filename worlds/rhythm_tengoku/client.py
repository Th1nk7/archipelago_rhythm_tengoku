import asyncio
from typing import TYPE_CHECKING

from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class RhythmTengokuClient(BizHawkClient):
    system = "GBA"
    game = "Rhythm Tengoku"
    patch_suffix = ".aprhtg"

    # Placeholder memory address for checking game completion
    GAME_COMPLETE_ADDR = 0x02000000

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        ctx.game = self.game
        ctx.items_handling = 0b111
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        while True:
            # Example memory read; replace with actual game state checks
            await ctx.read_u8(self.GAME_COMPLETE_ADDR)
            await asyncio.sleep(1 / 60)
