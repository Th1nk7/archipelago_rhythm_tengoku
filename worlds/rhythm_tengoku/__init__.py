from typing import ClassVar
import os

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial, World
from worlds.AutoWorld import WebWorld

from .items import item_table, RhythmTengokuItem
from .locations import location_table, RhythmTengokuLocation
from .options import RhythmTengokuOptions
from .rom import RhythmTengokuProcedurePatch, write_tokens


class RhythmTengokuWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Rhythm Tengoku for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Archipelago"]
    )]


class RhythmTengokuWorld(World):
    """Basic Archipelago world for Rhythm Tengoku."""

    game = "Rhythm Tengoku"
    web = RhythmTengokuWebWorld()
    options_dataclass = RhythmTengokuOptions
    options: RhythmTengokuOptions

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in location_table.items()}

    data_version = 0
    required_client_version = (0, 4, 6)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return RhythmTengokuItem(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        region = Region("Rhythm Tengoku", self.player, self.multiworld)
        self.multiworld.regions.append(region)
        menu.connect(region)
        for loc_name, loc in location_table.items():
            region.locations.append(RhythmTengokuLocation(self.player, loc_name, loc.id, region))

    def create_items(self) -> None:
        for item_name in item_table:
            self.multiworld.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        pass

    def fill_slot_data(self) -> dict:
        return {"check_type": self.options.check_type.current_key}

    def generate_output(self, output_directory: str) -> None:
        patch = RhythmTengokuProcedurePatch(player=self.player,
                                            player_name=self.multiworld.get_player_name(self.player),
                                            server=self.multiworld.server_address)
        write_tokens(self, patch)
        patch.write(os.path.join(output_directory,
                                 f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
