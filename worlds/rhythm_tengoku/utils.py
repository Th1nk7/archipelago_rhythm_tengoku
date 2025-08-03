# Lookup table: (x, y) => level_id
COORD_TO_LEVEL_ID = {
    (2, 6): 41,  # LEVEL_REMIX_1
    (3, 6): 42,  # LEVEL_REMIX_2
    (4, 6): 43,  # LEVEL_REMIX_3
    (5, 6): 44,  # LEVEL_REMIX_4
    (6, 6): 45,  # LEVEL_REMIX_5
    (7, 6): 46,  # LEVEL_REMIX_6
    (8, 6): 47,  # LEVEL_REMIX_7
    (9, 6): 48,  # LEVEL_REMIX_8

    (2, 7): 2,   # LEVEL_CLAPPY_TRIO
    (3, 7): 39,  # LEVEL_BON_ODORI
    (4, 7): 34,  # LEVEL_SPACE_DANCE
    (5, 7): 36,  # LEVEL_RAP_MEN
    (6, 7): 20,  # LEVEL_TAP_TRIAL
    (7, 7): 21,  # LEVEL_TAP_TRIAL_2
    (8, 7): 23,  # LEVEL_MARCHING_ORDERS_2
    (9, 7): 16,  # LEVEL_SNEAKY_SPIRITS_2

    (2, 8): 18,  # LEVEL_SPACEBALL
    (3, 8): 10,  # LEVEL_SICK_BEATS
    (4, 8): 32,  # LEVEL_TRAM_PAULINE
    (5, 8): 4,   # LEVEL_POLYRHYTHM
    (6, 8): 26,  # LEVEL_FIREWORKS
    (7, 8): 37,  # LEVEL_RAP_WOMEN
    (8, 8): 7,   # LEVEL_NIGHT_WALK_2
    (9, 8): 19,  # LEVEL_SPACEBALL_2

    (2, 9): 22,  # LEVEL_MARCHING_ORDERS
    (3, 9): 31,  # LEVEL_RAT_RACE
    (4, 9): 25,  # LEVEL_BUNNY_HOP
    (5, 9): 27,  # LEVEL_POWER_CALLIGRAPHY
    (6, 9): 29,  # LEVEL_TOSS_BOYS
    (7, 9): 35,  # LEVEL_COSMIC_DANCE
    (8, 9): 14,  # LEVEL_NINJA_REINCARNATE
    (9, 9): 5,   # LEVEL_POLYRHYTHM_2

    (2, 10): 8,  # LEVEL_RHYTHM_TWEEZERS
    (3, 10): 17, # LEVEL_SAMURAI_SLICE
    (4, 10): 33, # LEVEL_SHOWTIME
    (5, 10): 6,  # LEVEL_NIGHT_WALK
    (6, 10): 13, # LEVEL_NINJA_BODYGUARD
    (7, 10): 40, # LEVEL_BON_DANCE
    (8, 10): 9,  # LEVEL_RHYTHM_TWEEZERS_2
    (9, 10): 30, # LEVEL_TOSS_BOYS_2

    (2, 11): 0,  # LEVEL_KARATE_MAN
    (3, 11): 15, # LEVEL_SNEAKY_SPIRITS
    (4, 11): 24, # LEVEL_WIZARDS_WALTZ
    (5, 11): 38, # LEVEL_QUIZ_SHOW
    (6, 11): 11, # LEVEL_BOUNCY_ROAD
    (7, 11): 3,  # LEVEL_SNAPPY_TRIO
    (8, 11): 1,  # LEVEL_KARATE_MAN_2
    (9, 11): 12, # LEVEL_BOUNCY_ROAD_2
}

# Usage:
# level_id = COORD_TO_LEVEL_ID.get((x, y))
# If level_id is None, there's no game at (x, y) or it's not in Items.py

location_id_to_name = {
    0: "Karate Man OK",
    1: "Karate Man SUPERB",
    2: "Karate Man PERFECT",
    3: "Karate Man 2 OK",
    4: "Karate Man 2 SUPERB",
    5: "Karate Man 2 PERFECT",
    6: "Clappy Trio OK",
    7: "Clappy Trio SUPERB",
    8: "Clappy Trio PERFECT",
    9: "Snappy Trio OK",
    10: "Snappy Trio SUPERB",
    11: "Snappy Trio PERFECT",
    12: "Polyrhythm OK",
    13: "Polyrhythm SUPERB",
    14: "Polyrhythm PERFECT",
    15: "Polyrhythm 2 OK",
    16: "Polyrhythm 2 SUPERB",
    17: "Polyrhythm 2 PERFECT",
    18: "Night Walk OK",
    19: "Night Walk SUPERB",
    20: "Night Walk PERFECT",
    21: "Night Walk 2 OK",
    22: "Night Walk 2 SUPERB",
    23: "Night Walk 2 PERFECT",
    24: "Rhythm Tweezers OK",
    25: "Rhythm Tweezers SUPERB",
    26: "Rhythm Tweezers PERFECT",
    27: "Rhythm Tweezers 2 OK",
    28: "Rhythm Tweezers 2 SUPERB",
    29: "Rhythm Tweezers 2 PERFECT",
    30: "Sick Beats OK",
    31: "Sick Beats SUPERB",
    32: "Sick Beats PERFECT",
    33: "Bouncy Road OK",
    34: "Bouncy Road SUPERB",
    35: "Bouncy Road PERFECT",
    36: "Bouncy Road 2 OK",
    37: "Bouncy Road 2 SUPERB",
    38: "Bouncy Road 2 PERFECT",
    39: "Ninja Bodyguard OK",
    40: "Ninja Bodyguard SUPERB",
    41: "Ninja Bodyguard PERFECT",
    42: "Ninja Reincarnate OK",
    43: "Ninja Reincarnate SUPERB",
    44: "Ninja Reincarnate PERFECT",
    45: "Sneaky Spirits OK",
    46: "Sneaky Spirits SUPERB",
    47: "Sneaky Spirits PERFECT",
    48: "Sneaky Spirits 2 OK",
    49: "Sneaky Spirits 2 SUPERB",
    50: "Sneaky Spirits 2 PERFECT",
    51: "Samurai Slice OK",
    52: "Samurai Slice SUPERB",
    53: "Samurai Slice PERFECT",
    54: "Spaceball OK",
    55: "Spaceball SUPERB",
    56: "Spaceball PERFECT",
    57: "Spaceball 2 OK",
    58: "Spaceball 2 SUPERB",
    59: "Spaceball 2 PERFECT",
    60: "Tap Trial OK",
    61: "Tap Trial SUPERB",
    62: "Tap Trial PERFECT",
    63: "Tap Trial 2 OK",
    64: "Tap Trial 2 SUPERB",
    65: "Tap Trial 2 PERFECT",
    66: "Marching Orders OK",
    67: "Marching Orders SUPERB",
    68: "Marching Orders PERFECT",
    69: "Marching Orders 2 OK",
    70: "Marching Orders 2 SUPERB",
    71: "Marching Orders 2 PERFECT",
    72: "Wizards Waltz OK",
    73: "Wizards Waltz SUPERB",
    74: "Wizards Waltz PERFECT",
    75: "Bunny Hop OK",
    76: "Bunny Hop SUPERB",
    77: "Bunny Hop PERFECT",
    78: "Fireworks OK",
    79: "Fireworks SUPERB",
    80: "Fireworks PERFECT",
    81: "Power Calligraphy OK",
    82: "Power Calligraphy SUPERB",
    83: "Power Calligraphy PERFECT",
    84: "Power Calligraphy 2 OK",
    85: "Power Calligraphy 2 SUPERB",
    86: "Power Calligraphy 2 PERFECT",
    87: "Toss Boys OK",
    88: "Toss Boys SUPERB",
    89: "Toss Boys PERFECT",
    90: "Toss Boys 2 OK",
    91: "Toss Boys 2 SUPERB",
    92: "Toss Boys 2 PERFECT",
    93: "Rat Race OK",
    94: "Rat Race SUPERB",
    95: "Rat Race PERFECT",
    96: "Tram Pauline OK",
    97: "Tram Pauline SUPERB",
    98: "Tram Pauline PERFECT",
    99: "Showtime OK",
    100: "Showtime SUPERB",
    101: "Showtime PERFECT",
    102: "Space Dance OK",
    103: "Space Dance SUPERB",
    104: "Space Dance PERFECT",
    105: "Cosmic Dance OK",
    106: "Cosmic Dance SUPERB",
    107: "Cosmic Dance PERFECT",
    108: "Rap Men OK",
    109: "Rap Men SUPERB",
    110: "Rap Men PERFECT",
    111: "Rap Women OK",
    112: "Rap Women SUPERB",
    113: "Rap Women PERFECT",
    114: "Quiz Show OK",
    115: "Quiz Show SUPERB",
    116: "Quiz Show PERFECT",
    117: "Bon Odori OK",
    118: "Bon Odori SUPERB",
    119: "Bon Odori PERFECT",
    120: "Bon Dance OK",
    121: "Bon Dance SUPERB",
    122: "Bon Dance PERFECT",
    123: "Remix 1 OK",
    124: "Remix 1 SUPERB",
    125: "Remix 1 PERFECT",
    126: "Remix 2 OK",
    127: "Remix 2 SUPERB",
    128: "Remix 2 PERFECT",
    129: "Remix 3 OK",
    130: "Remix 3 SUPERB",
    131: "Remix 3 PERFECT",
    132: "Remix 4 OK",
    133: "Remix 4 SUPERB",
    134: "Remix 4 PERFECT",
    135: "Remix 5 OK",
    136: "Remix 5 SUPERB",
    137: "Remix 5 PERFECT",
    138: "Remix 6 OK",
    139: "Remix 6 SUPERB",
    140: "Remix 6 PERFECT",
    141: "Remix 7 OK",
    142: "Remix 7 SUPERB",
    143: "Remix 7 PERFECT",
    144: "Remix 8 OK",
    145: "Remix 8 SUPERB",
    146: "Remix 8 PERFECT",
}


l = ["Karate Man",
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
"Remix 8"]