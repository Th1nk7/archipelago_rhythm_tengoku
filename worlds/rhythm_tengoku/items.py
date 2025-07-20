from dataclasses import dataclass
from typing import Dict

from BaseClasses import Item, ItemClassification


@dataclass
class ItemData:
    code: int
    classification: ItemClassification


level_names = [f"Stage {i}" for i in range(1, 49)]

item_table: Dict[str, ItemData] = {
    name: ItemData(1000 + idx, ItemClassification.progression)
    for idx, name in enumerate(level_names)
}


class RhythmTengokuItem(Item):
    game: str = "Rhythm Tengoku"
