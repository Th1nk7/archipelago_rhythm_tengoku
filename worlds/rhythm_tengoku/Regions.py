from typing import List
from dataclasses import dataclass

@dataclass
class RTRegion:
    name: str

@dataclass
class LevelRegion(RTRegion):
    level_id: int
    level_x: int
    level_y: int

class Regions:
    l0 = LevelRegion("Karate Man", 0, 2, 11)
    l1 = LevelRegion("Karate Man 2", 1, 8, 11)

    l2 = LevelRegion("Clappy Trio", 2, 2, 7)
    l3 = LevelRegion("Snappy Trio", 3, 7, 11)

    l4 = LevelRegion("Polyrhythm", 4, 5, 8)
    l5 = LevelRegion("Polyrhythm 2", 5, 9, 9)

    l6 = LevelRegion("Night Walk", 6, 5, 10)
    l7 = LevelRegion("Night Walk 2", 7, 8, 8)

    l8 = LevelRegion("Rhythm Tweezers", 8, 2, 10)
    l9 = LevelRegion("Rhythm Tweezers 2", 9, 8, 10)

    l10 = LevelRegion("Sick Beats", 10, 3, 8)

    l11 = LevelRegion("Bouncy Road", 11, 6, 11)
    l12 = LevelRegion("Bouncy Road 2", 12, 9, 11)

    l13 = LevelRegion("Ninja Bodyguard", 13, 6, 10)
    l14 = LevelRegion("Ninja Reincarnate", 14, 8, 9)

    l15 = LevelRegion("Sneaky Spirits", 15, 3, 11)
    l16 = LevelRegion("Sneaky Spirits 2", 16, 9, 7)

    l17 = LevelRegion("Samurai Slice", 17, 3, 10)

    l18 = LevelRegion("Spaceball", 18, 2, 8)
    l19 = LevelRegion("Spaceball 2", 19, 9, 8)

    l20 = LevelRegion("Tap Trial", 20, 6, 7)
    l21 = LevelRegion("Tap Trial 2", 21, 7, 7)

    l22 = LevelRegion("Marching Orders", 22, 2, 9)
    l23 = LevelRegion("Marching Orders 2", 23, 8, 7)

    l24 = LevelRegion("Wizards Waltz", 24, 4, 11)

    l25 = LevelRegion("Bunny Hop", 25, 4, 9)

    l26 = LevelRegion("Fireworks", 26, 6, 8)

    l27 = LevelRegion("Power Calligraphy", 27, 5, 9)

    l28 = LevelRegion("Toss Boys", 28, 6, 9)
    l29 = LevelRegion("Toss Boys 2", 29, 9, 10)

    l30 = LevelRegion("Rat Race", 30, 3, 9)

    l31 = LevelRegion("Tram Pauline", 31, 4, 8)

    l32 = LevelRegion("Showtime", 32, 4, 10)

    l33 = LevelRegion("Space Dance", 33, 4, 7)
    l34 = LevelRegion("Cosmic Dance", 34, 7, 9)

    l35 = LevelRegion("Rap Men", 35, 5, 7)
    l36 = LevelRegion("Rap Women", 36, 7, 8)

    l37 = LevelRegion("Quiz Show", 37, 5, 11)
    
    l38 = LevelRegion("Bon Odori", 38, 3, 7)
    l39 = LevelRegion("Bon Dance", 39, 7, 10)

    l40 = LevelRegion("Remix 1", 40, 2, 6)
    l41 = LevelRegion("Remix 2", 41, 3, 6)
    l42 = LevelRegion("Remix 3", 42, 4, 6)
    l43 = LevelRegion("Remix 4", 43, 5, 6)
    l44 = LevelRegion("Remix 5", 44, 6, 6)
    l45 = LevelRegion("Remix 6", 45, 7, 6)
    l46 = LevelRegion("Remix 7", 46, 8, 6)
    l47 = LevelRegion("Remix 8", 47, 9, 6)

    all_regions: List[RTRegion] = [
        l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19,
        l20, l21, l22, l23, l24, l25, l26, l27, l28, l29, l30, l31, l32, l33, l34, l35, l36, l37, l38, l39,
        l40, l41, l42, l43, l44, l45, l46, l47
    ]

    @classmethod
    def get_from_name(cls, name: str) -> RTRegion:
        for region in cls.all_regions:
            if region.name == name:
                return region
        return None
    
    @classmethod
    def get_from_id(cls, id: int) -> RTRegion:
        for region in [region for region in cls.all_regions if isinstance(region, LevelRegion)]:
            if region.level_id == id:
                return region
        return None

    @classmethod
    def get_from_coordinates(cls, x: int, y: int):
        for region in [region for region in cls.all_regions if isinstance(region, LevelRegion)]:
            if region.level_x == x and region.level_y == y:
                return region
        return None