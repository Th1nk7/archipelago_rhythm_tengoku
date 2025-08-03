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
            elif item.type == ItemType.Level and (
                item.name in self.options.starting_levels.value
                or item.name in self.options.skipped_levels.value):
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

        for r in Regions.all_regions:
            name: str = f"Cleared {r.name}"
            self.event_names.append(name)

            if r.name in self.options.skipped_levels.value:
                continue

            region: Region = self.get_region(r.name)
            location: RhythmTengokuLocation = RhythmTengokuLocation(player, name, None, region)

            if not name[8:] in self.options.goal_levels.value:
                location.place_locked_item(self.create_event("Level Completed"))
            region.locations.append(location)

        for goal_level in self.options.goal_levels.value:
            trophy: Location = self.get_location("Cleared " + goal_level)
            trophy.place_locked_item(self.create_event("Trophy - " + goal_level))
        
        multiworld.completion_condition[player] = lambda state: state.has_all([f"Trophy - {goal_level}" for goal_level in self.options.goal_levels.value])

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "locations": self.game_id_to_long,
            "starting_levels": self.options.starting_levels.value,
            "goal_levels": self.options.goal_levels.value,
            "goal_rank": self.options.goal_rank.value,
            "skipped_levels": self.options.skipped_levels.value,
            "ok_rewards": bool(self.options.ok_rewards),
            "superb_rewards": bool(self.options.superb_rewards),
            "perfect_rewards": bool(self.options.perfect_rewards),
            "death_link": bool(self.options.death_link),
        }
        return slot_data

class RhythmTengokuItem(Item):
    game: str = "Rhythm Tengoku"

class RhythmTengokuLocation(Location):
    game: str = "Rhythm Tengoku"