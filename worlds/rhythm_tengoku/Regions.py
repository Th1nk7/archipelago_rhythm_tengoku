from __future__ import annotations

from BaseClasses import MultiWorld, Region, Entrance

from .Locations import RhythmTengokuLocation, location_table


def create_regions(multiworld: MultiWorld, player: int) -> None:
    """Create the basic world regions and link them."""
    menu = Region("Menu", player, multiworld)
    game_region = Region("Rhythm Tengoku", player, multiworld)

    for name, loc_id in location_table.items():
        game_region.locations.append(RhythmTengokuLocation(player, name, loc_id, game_region))

    start = Entrance(player, "Start Game", menu)
    menu.exits.append(start)
    start.connect(game_region)

    multiworld.regions.extend([menu, game_region])
