from __future__ import annotations

from BaseClasses import MultiWorld


def set_rules(multiworld: MultiWorld, player: int) -> None:
    """Define basic access rules and the win condition."""
    # Placeholder completion condition: require the Beat Game item
    multiworld.completion_condition[player] = lambda state: state.has("Beat Game", player)
