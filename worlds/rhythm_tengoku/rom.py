import os
from typing import TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

if TYPE_CHECKING:
    from . import RhythmTengokuWorld


class RhythmTengokuProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Rhythm Tengoku"
    hash = ""
    patch_file_ending = ".aprt"
    result_file_ending = ".gba"
    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        raise FileNotFoundError("Rhythm Tengoku base ROM not provided")


def write_tokens(world: "RhythmTengokuWorld", patch: RhythmTengokuProcedurePatch) -> None:
    # Placeholder for token data such as connection info
    patch.write_token(APTokenTypes.WRITE, 0x0, b"AP")
