from __future__ import annotations
from typing import ClassVar, Dict

from BaseClasses import Location


class RhythmTengokuLocation(Location):
    """Archipelago location for Rhythm Tengoku."""
    game: ClassVar[str] = "Rhythm Tengoku"


# Minimal location table; extend with real stage checks later.
location_table: Dict[str, int] = {
    "Beat Game": 1,
}
