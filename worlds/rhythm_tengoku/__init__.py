from typing import ClassVar

from BaseClasses import Region, Entrance, Location, Item, ItemClassification
from worlds.AutoWorld import World
from Options import PerGameCommonOptions

from .client import RhythmTengokuClient  # required for BizHawk registration


class RhythmTengokuItem(Item):
    game: ClassVar[str] = "Rhythm Tengoku"


class RhythmTengokuLocation(Location):
    game: ClassVar[str] = "Rhythm Tengoku"


class RhythmTengokuWorld(World):
    game = "Rhythm Tengoku"
    options_dataclass = PerGameCommonOptions
    topology_present = False

    item_name_to_id = {
        "Beat Game": 1,
    }
    location_name_to_id = {
        "Beat Game": 1,
    }

    def create_item(self, name: str) -> Item:
        return RhythmTengokuItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        game_region = Region("Rhythm Tengoku", self.player, self.multiworld)
        self.multiworld.regions += [menu, game_region]

        start_entrance = Entrance(self.player, "Start Game", menu)
        menu.exits.append(start_entrance)
        start_entrance.connect(game_region)

        beat_game_location = RhythmTengokuLocation(self.player, "Beat Game", None, game_region)
        game_region.locations.append(beat_game_location)

    def create_items(self) -> None:
        self.multiworld.itempool.append(self.create_item("Beat Game"))

    def set_rules(self) -> None:
        pass

    def fill_slot_data(self):
        return {}
