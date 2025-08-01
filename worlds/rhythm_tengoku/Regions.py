from __future__ import annotations

from BaseClasses import MultiWorld, Region, Entrance

from .Locations import RhythmTengokuLocation, location_table


def create_regions(multiworld: MultiWorld, player: int) -> None:
    """Create the basic world regions and link them."""
    menu = Region("Menu", player, multiworld)
    game_region = Region("Rhythm Tengoku", player, multiworld)

    beat_game = RhythmTengokuLocation(player, "Beat Game", location_table["Beat Game"], game_region)
    game_region.locations.append(beat_game)

    start = Entrance(player, "Start Game", menu)
    menu.exits.append(start)
    start.connect(game_region)

    multiworld.regions.extend([menu, game_region])
