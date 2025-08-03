from typing import Dict, List, Any, Union
from BaseClasses import Region, Location, Item, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World
from .Items import ItemType, base_id, item_list, group_dict
from .Locations import LocationType, location_list
from .Regions import Regions
from .Rules import RhythmTengokuRules
from .Options import RhythmTengokuOptions

class RhythmTengokuWorld(World):
    """The first Rhythm Heaven game"""
    game = "Rhythm Tengoku"
    
    item_name_to_id = {item.name: (base_id + index) for index, item in enumerate(item_list)}
    location_name_to_id = {loc.name: (base_id + index) for index, loc in enumerate(location_list)}

    item_name_groups = group_dict
    options_dataclass = RhythmTengokuOptions
    options: RhythmTengokuOptions

    def __init__(self, multiworld, player):
        super(RhythmTengokuWorld, self).__init__(multiworld, player)
        self.skipped_location_types: List[LocationType] = []

        self.item_classifications: Dict[ItemType, Union[ItemClassification, None]] = {}
        self.item_classifications[ItemType.Level] = ItemClassification.progression
        self.item_classifications[ItemType.Filler] = ItemClassification.filler
        self.item_classifications[ItemType.Trap] = ItemClassification.trap

        self.event_names: List[str] = []
        self.game_id_to_long: Dict[str, int] = {}

    def set_rules(self):
        RhythmTengokuRules(self).set_rules()
    
    def create_item(self, name: str) -> "RhythmTengokuItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id
        classification = ItemClassification.filler
        if self.item_classifications[item_list[id].type] != None:
            classification = self.item_classifications[item_list[id].type]
        
        # Add ItemClassification changes for individual items dependant on options here

        return RhythmTengokuItem(name, classification, item_id, self.player)
    
    def create_event(self, event: str):
        return RhythmTengokuItem(event, ItemClassification.progression_skip_balancing, None, self.player)
    
    def generate_early(self):
        if not self.options.starting_levels.value:
            raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                              f"No starting level(s) specified.")
        
        if not self.options.goal_levels.value:
            raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                              f"No goal level(s) specified.")

        for starting_level in self.options.starting_levels.value:
            if starting_level in self.options.skipped_levels.value:
                raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                                  f"Starting level ({starting_level}) cannot be skipped.")
        
        for goal_level in self.options.goal_levels.value:
            if goal_level in self.options.skipped_levels.value:
                raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                                  f"Goal level ({goal_level}) cannot be skipped.")
            
        if self.options.goal_rank == "ok" and not self.options.ok_rewards:
            raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                              f"Goal rank required OK, but OK rewards are disabled.")
        
        if self.options.goal_rank == "superb" and not self.options.superb_rewards:
            raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                              f"Goal rank required SUPERB, but SUPERB rewards are disabled.")
        
        if self.options.goal_rank == "perfect" and not self.options.perfect_rewards:
            raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                              f"Goal rank required PERFECT, but PERFECT rewards are disabled.")
        
        if not self.options.ok_rewards and not self.options.superb_rewards and not self.options.perfect_rewards:
            raise OptionError(f"[Rhythm Tengoku - '{self.player_name}'] "
                              f"No rank rewards are selected. Select at least one rank reward.")
        
        if not self.options.ok_rewards:
            self.skipped_location_types.append(LocationType.OkRank)

        if not self.options.superb_rewards:
            self.skipped_location_types.append(LocationType.SuperbRank)

        if not self.options.perfect_rewards:
            self.skipped_location_types.append(LocationType.PerfectRank)
        
    def create_items(self):
        pool = []

        for item in item_list:
            if self.item_classifications[item.type] == None:
                continue
            elif item.type == ItemType.Level and item.name in self.options.starting_levels.value or item.name in self.options.skipped_levels.value:
                continue
            elif item.type == ItemType.Filler or item.type == ItemType.Trap:
                continue
            
            pool.append(self.create_item(item.name))
        
        junk: int = max(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool), 0)

        trap: int = round(junk * (self.options.trap_percent / 100))
        filler: int = junk - trap

        for _ in range(trap):
            pool.append(self.create_item(self.random.choices(list(self.options.trap_weights.value.keys()), list(self.options.trap_weights.value.values()))[0]))

        for _ in range(filler):
            pool.append(self.create_item(self.random.choices(list(self.options.filler_weights.value.keys()), list(self.options.filler_weights.value.values()))[0]))

        self.multiworld.itempool += pool

    def create_regions(self):
        player = self.player
        multiworld = self.multiworld

        menu = Region("Menu", player, multiworld)

        for r in Regions.all_regions:
            multiworld.regions += [Region(r.name, player, multiworld)]
            menu.add_exits({r.name})

        multiworld.regions.append(menu)

        for index, loc in enumerate(location_list):
            if loc.type in self.skipped_location_types:
                continue
            self.game_id_to_long[loc.game_id] = (base_id + index)

            region: Region = self.get_region(loc.region.name)
            location: RhythmTengokuLocation = RhythmTengokuLocation(player, loc.name, (base_id + index), region)
            region.locations.append(location)

            if loc.region.name in self.options.skipped_levels.value:
                self.options.exclude_locations.value.add(loc.name)

        # Create events for level completion
        for r in Regions.all_regions:
            name: str = f"Cleared {r.name}"
            self.event_names.append(name)

            if r.name in self.options.skipped_levels.value:
                continue

            region: Region = self.get_region(r.name)
            location: RhythmTengokuLocation = RhythmTengokuLocation(player, name, None, region)

            if not r.name in self.options.goal_levels.value:
                location.place_locked_item(self.create_event("Level Completed"))
            region.locations.append(location)

        for goal_level in self.options.goal_levels.value:
            victory: Location = self.get_location("Cleared " + goal_level)
            victory.place_locked_item(self.create_event(f"Victory - {goal_level}"))

        g_levels = list(self.options.goal_levels.value)
        multiworld.completion_condition[player] = lambda state: all(
            state.has(f"Victory - {g}", player) for g in g_levels
        )

        # Goal levels should have items still
        #
        # Victory should count for goal levels per rank required
        #
        # Regions are next
            



class RhythmTengokuItem(Item):
    game: str = "Rhythm Tengoku"


class RhythmTengokuLocation(Location):
    game: str = "Rhythm Tengoku"





#from BaseClasses import Region, ItemClassification, Tutorial
#from worlds.AutoWorld import World
#from .Items import item_table, RhythmTengokuItem
#from .Locations import location_table, level_table, RhythmTengokuLocation
#from .Options import RhythmTengokuOptions
#from .Rules import set_rules
#
#class RhythmTengokuWorld(World):
#    game = "Rhythm Tengoku"
#    options_dataclass = RhythmTengokuOptions
#    options: RhythmTengokuOptions
#    topology_present = False
#
#    item_name_to_id = item_table
#    location_name_to_id = location_table
#    starting_inventory = {}
#
#    def create_items(self) -> None:
#        start_levels = set(self.options.start_level.value)
#        goal_levels = set(self.options.goal_levels.value)
#        excluded_levels = set(self.options.excluded_levels.value)
#
#        rank_options = {
#            0: ["OK"], 1: ["SUPERB"], 2: ["PERFECT"],
#            3: ["OK", "SUPERB"], 4: ["OK", "PERFECT"],
#            5: ["SUPERB", "PERFECT"], 6: ["OK", "SUPERB", "PERFECT"]
#        }
#        valid_ranks = rank_options.get(self.options.rank_rewards.value, ["OK", "SUPERB"])
#        print(f"[DEBUG] Rank Rewards: {valid_ranks}")
#
#        start_levels -= excluded_levels
#        goal_levels -= excluded_levels
#
#        removed_locations = []
#        for loc_name in list(location_table.keys()):
#            level_name, rank = loc_name.rsplit(" ", 1)
#            if rank == "PERFECT" and "PERFECT" not in valid_ranks:
#                removed_locations.append(loc_name)
#                del location_table[loc_name]
#        if removed_locations:
#            print(f"[DEBUG] Removed PERFECT locations: {removed_locations}")
#
#        total_items = 0
#        for level_name in level_table:
#            if level_name in excluded_levels:
#                continue
#            classification = (
#                ItemClassification.progression if level_name in goal_levels
#                else ItemClassification.useful
#            )
#            item = RhythmTengokuItem(level_name, classification, item_table[level_name], self.player)
#            if level_name in start_levels:
#                self.multiworld.push_precollected(item)
#            else:
#                self.multiworld.itempool.append(item)
#                total_items += 1
#
#        for loc_name in location_table:
#            level_name, rank = loc_name.rsplit(" ", 1)
#            if level_name in excluded_levels or rank not in valid_ranks:
#                continue
#            loc = self.multiworld.get_location(loc_name, self.player)
#            loc.locked = False
#
#        valid_locs = [loc for loc in self.multiworld.get_locations(self.player) if loc.item is None and not loc.locked]
#        filler_needed = max(0, len(valid_locs) - total_items)
#        for _ in range(filler_needed):
#            filler = RhythmTengokuItem("Blinking Trap", ItemClassification.filler, item_table["Blinking Trap"], self.player)
#            self.multiworld.itempool.append(filler)
#
#        print(f"[DEBUG] Total items: {total_items}, Fillers added: {filler_needed}, Fill locations: {len(valid_locs)}")
#
#    def create_regions(self) -> None:
#        menu_region = Region("Menu", self.player, self.multiworld)
#        self.multiworld.regions.append(menu_region)
#
#        game_region = Region("Rhythm Tengoku", self.player, self.multiworld)
#        for loc_name, loc_id in location_table.items():
#            location = RhythmTengokuLocation(self.player, loc_name, loc_id, game_region)
#            game_region.locations.append(location)
#
#        self.multiworld.regions.append(game_region)
#
#    def set_rules(self) -> None:
#        set_rules(self.multiworld, self.player)
#
#    def fill_slot_data(self) -> dict:
#        return {
#            "goal_levels": sorted(list(set(self.options.goal_levels.value) - set(self.options.excluded_levels.value))),
#            "goal_type": self.options.goal.value,
#            "start_items": sorted(list(self.options.start_level.value))
#        }
#
#    def generate_output(self, output_directory: str) -> None:
#        pass
#
#    def create_tutorial(self) -> Tutorial:
#        tutorial = Tutorial("Rhythm Tengoku Tutorial")
#        tutorial.text = (
#            "Load the patched ROM into BizHawk.\n"
#            "Connect to Archipelago from the BizHawk client.\n"
#            "Complete goal levels with required rank to finish."
#        )
#        return tutorial
#