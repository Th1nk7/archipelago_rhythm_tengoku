from __future__ import annotations

from BaseClasses import MultiWorld
from worlds.generic.Rules import add_rule


def set_rules(multiworld: MultiWorld, player: int) -> None:
    """Define access rules and the win condition for Rhythm Tengoku."""

    world = multiworld.worlds[player]
    goal_levels = set(world.options.goal_levels.value)
    excluded_levels = set(world.options.excluded_levels.value)

    # Sanitize goal levels: remove any excluded levels
    goal_levels = goal_levels - excluded_levels

    # Handle edge case: no goal levels specified
    if not goal_levels:
        # Log warning and make "Beat Game" always accessible
        multiworld.completion_condition[player] = lambda state: state.has("Beat Game", player)
    else:
        # Win condition: must have "Beat Game" item
        multiworld.completion_condition[player] = lambda state: state.has("Beat Game", player)

        # Require all goal levels as items to access "Beat Game"
        def beat_game_requirements(state):
            return all(state.has(world.item_name_to_id[level_name], player)
                       for level_id in goal_levels
                       for level_name in [list(world.item_name_to_id.keys())[level_id]])

        add_rule(multiworld.get_location("Beat Game", player), beat_game_requirements)

    # Starting levels are accessible by default (no rules added)

    # Add item-based access rules for all levels (excluding excluded levels)
    for level_name in world.item_name_to_id:
        if level_name == "Beat Game":
            continue
        # Derive level index from name
        try:
            level_index = list(world.item_name_to_id.keys()).index(level_name)
        except ValueError:
            continue  # skip if not found

        if level_index in excluded_levels:
            continue

        for rank in ["OK", "SUPERB", "PERFECT"]:
            location_name = f"{level_name} {rank}"
            add_rule(multiworld.get_location(location_name, player),
                     lambda state, lvl=level_name: state.has(lvl, player))