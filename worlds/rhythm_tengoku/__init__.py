from __future__ import annotations

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World

from .Items import RhythmTengokuItem, item_table
from .Locations import location_table
from .Regions import create_regions
from .Rules import set_rules
from .Options import RhythmTengokuOptions
from .client import RhythmTengokuClient


class RhythmTengokuWorld(World):
    """Minimal Archipelago world definition for Rhythm Tengoku."""
    game = "Rhythm Tengoku"
    topology_present = False
    options_dataclass = RhythmTengokuOptions

    item_name_to_id = item_table
    location_name_to_id = location_table

    def create_item(self, name: str) -> Item:
        return RhythmTengokuItem(name, ItemClassification.progression, item_table[name], self.player)

    def create_items(self) -> None:
        for item_name in item_table:
            self.multiworld.itempool.append(self.create_item(item_name))

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str) -> None:
        # TODO: generate patched ROM and spoiler log
        pass

    def fill_slot_data(self):
        # TODO: provide slot-specific data for clients
        return {}
