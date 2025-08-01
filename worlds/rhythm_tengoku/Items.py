from __future__ import annotations
from typing import ClassVar, Dict

from BaseClasses import Item, ItemClassification


class RhythmTengokuItem(Item):
    """Archipelago representation of a Rhythm Tengoku item."""
    game: ClassVar[str] = "Rhythm Tengoku"


# Minimal item table; extend with actual game items later.
item_table: Dict[str, int] = {
    "Beat Game": 1,
}
