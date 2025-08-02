from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum

base_id = 29300

class ItemType(Enum):
    Level = 0
    Filler = 1
    Trap = 2

@dataclass
class RTItem:
    name: str
    type: ItemType
    count: int = 1

item_list: List[RTItem] = [
    # Levels
    RTItem("Karate Man", ItemType.Level),
    RTItem("Karate Man 2", ItemType.Level),
    RTItem("Clappy Trio", ItemType.Level),
    RTItem("Snappy Trio", ItemType.Level),
    RTItem("Polyrhythm", ItemType.Level),
    RTItem("Polyrhythm 2", ItemType.Level),
    RTItem("Night Walk", ItemType.Level),
    RTItem("Night Walk 2", ItemType.Level),
    RTItem("Rhythm Tweezers", ItemType.Level),
    RTItem("Rhythm Tweezers 2", ItemType.Level),
    RTItem("Sick Beats", ItemType.Level),
    RTItem("Bouncy Road", ItemType.Level),
    RTItem("Bouncy Road 2", ItemType.Level),
    RTItem("Ninja Bodyguard", ItemType.Level),
    RTItem("Ninja Reincarnate", ItemType.Level),
    RTItem("Sneaky Spirits", ItemType.Level),
    RTItem("Sneaky Spirits 2", ItemType.Level),
    RTItem("Samurai Slice", ItemType.Level),
    RTItem("Spaceball", ItemType.Level),
    RTItem("Spaceball 2", ItemType.Level),
    RTItem("Tap Trial", ItemType.Level),
    RTItem("Tap Trial 2", ItemType.Level),
    RTItem("Marching Orders", ItemType.Level),
    RTItem("Marching Orders 2", ItemType.Level),
    RTItem("Wizards Waltz", ItemType.Level),
    RTItem("Bunny Hop", ItemType.Level),
    RTItem("Fireworks", ItemType.Level),
    RTItem("Power Calligraphy", ItemType.Level),
    RTItem("Toss Boys", ItemType.Level),
    RTItem("Toss Boys 2", ItemType.Level),
    RTItem("Rat Race", ItemType.Level),
    RTItem("Tram Pauline", ItemType.Level),
    RTItem("Showtime", ItemType.Level),
    RTItem("Space Dance", ItemType.Level),
    RTItem("Cosmic Dance", ItemType.Level),
    RTItem("Rap Men", ItemType.Level),
    RTItem("Rap Women", ItemType.Level),
    RTItem("Quiz Show", ItemType.Level),
    RTItem("Bon Odori", ItemType.Level),
    RTItem("Bon Dance", ItemType.Level),
    RTItem("Remix 1", ItemType.Level),
    RTItem("Remix 2", ItemType.Level),
    RTItem("Remix 3", ItemType.Level),
    RTItem("Remix 4", ItemType.Level),
    RTItem("Remix 5", ItemType.Level),
    RTItem("Remix 6", ItemType.Level),
    RTItem("Remix 7", ItemType.Level),
    RTItem("Remix 8", ItemType.Level),

    # Filler
    RTItem("RT Filler", ItemType.Filler),

    # Traps
    RTItem("Blinking Trap", ItemType.Trap)
]

group_dict: Dict[str, Set[str]] = {
    "junk": {"RT Filler",
             "Blinking Trap"},
    "filler": {"RT Filler"},
    "trap": {"Blinking Trap"},
    "levels": {"Karate Man",
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
               "Remix 8"},
}