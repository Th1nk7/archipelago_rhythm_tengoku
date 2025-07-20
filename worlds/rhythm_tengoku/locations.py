from dataclasses import dataclass
from typing import Dict

from BaseClasses import Location


@dataclass
class LocationData:
    id: int


location_table: Dict[str, LocationData] = {
    name: LocationData(2000 + idx)
    for idx, name in enumerate([f"Stage {i}" for i in range(1, 49)])
}


class RhythmTengokuLocation(Location):
    game: str = "Rhythm Tengoku"
