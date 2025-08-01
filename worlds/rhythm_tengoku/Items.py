from __future__ import annotations
from typing import ClassVar, Dict, List

from BaseClasses import Item, ItemClassification


class RhythmTengokuItem(Item):
    """Archipelago representation of a Rhythm Tengoku item."""
    game: ClassVar[str] = "Rhythm Tengoku"


# List of all Rhythm Tengoku levels in order of their in-game IDs.
level_table: List[str] = [
    "Karate Man",
    "Karate Man 2",
    "Clappy Trio",
    "Snappy Trio",
    "Polyrhythm",
    "Polyrhythm 2",
    "Night Walk",
    "Night Walk 2",
    "Rhythm Tweezers",
    "Rhythm Tweezers 2",
    "Sick Beats",
    "Bouncy Road",
    "Bouncy Road 2",
    "Ninja Bodyguard",
    "Ninja Reincarnate",
    "Sneaky Spirits",
    "Sneaky Spirits 2",
    "Samurai Slice",
    "Spaceball",
    "Spaceball 2",
    "Tap Trial",
    "Tap Trial 2",
    "Marching Orders",
    "Marching Orders 2",
    "Wizards Waltz",
    "Bunny Hop",
    "Fireworks",
    "Power Calligraphy",
    "Power Calligraphy 2",
    "Toss Boys",
    "Toss Boys 2",
    "Rat Race",
    "Tram Pauline",
    "Showtime",
    "Space Dance",
    "Cosmic Dance",
    "Rap Men",
    "Rap Women",
    "Quiz Show",
    "Bon Odori",
    "Bon Dance",
    "Remix 1",
    "Remix 2",
    "Remix 3",
    "Remix 4",
    "Remix 5",
    "Remix 6",
    "Remix 7",
    "Remix 8",
    "Blinking Trap",
    "Beat Game",
]


# Map each level name to its corresponding Archipelago item ID.
item_table: Dict[str, int] = {name: idx for idx, name in enumerate(level_table)}