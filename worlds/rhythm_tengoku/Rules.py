from worlds.generic.Rules import set_rule, add_item_rule
from BaseClasses import CollectionState

from .Regions import Regions
from .Locations import location_list, LocationType
from .Items import group_dict

class RhythmTengokuRules:
    def __init__(self, world):
        self.world = world
        self.multiworld = world.multiworld
        self.player = world.player

    def set_rules(self) -> None:
        """
        - Precollect starting level items.
        - Gate each rank location (OK/SUPERB/PERFECT) behind its level item.
        - Gate each "Cleared <Level>" event behind its level item.
        - Forbid placing a level's own item at any of its rank locations (no self-locks).
        """
        self._precollect_starting_levels()
        self._apply_rank_location_rules()
        self._apply_clear_event_rules()

    def _precollect_starting_levels(self) -> None:
        for level_name in sorted(self.world.options.starting_levels.value):
            self.multiworld.push_precollected(self.world.create_item(level_name))

    def _apply_rank_location_rules(self) -> None:
        """
        Each rank location for a level requires having that level's item.
        Also forbid placing that level's own item at any of its rank locations.
        """
        for rt_loc in location_list:
            if rt_loc.type in self.world.skipped_location_types:
                continue

            ap_loc = self.world.get_location(rt_loc.name)
            level_name = rt_loc.region.name

            set_rule(ap_loc, lambda state, lvl=level_name: self._has_level(state, lvl))

            add_item_rule(ap_loc, lambda item, lvl=level_name: item.name != lvl)

    def _apply_clear_event_rules(self) -> None:
        """
        "Cleared <Level>" event is reachable if the level is reachable (i.e., you have the level item).
        The *rank requirement* for trophies is enforced client-side when the check is sent.
        """
        for region in Regions.all_regions:
            level_name = region.name

            if level_name in self.world.options.skipped_levels.value:
                continue

            clear_loc_name = f"Cleared {level_name}"
            ap_loc = self.world.get_location(clear_loc_name)

            set_rule(ap_loc, lambda state, lvl=level_name: self._has_level(state, lvl))

    def _has_level(self, state: CollectionState, level_name: str) -> bool:
        return state.has(level_name, self.player)
