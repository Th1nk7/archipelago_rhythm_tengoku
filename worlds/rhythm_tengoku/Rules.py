from worlds.generic.Rules import add_rule
from BaseClasses import CollectionState
from typing import Callable, Dict, TYPE_CHECKING
from .Regions import Regions

if TYPE_CHECKING:
    from . import RhythmTengokuWorld
else:
    RhythmTengokuWorld = object

DEBUG: bool = True

class RhythmTengokuRules:
    def __init__(self, world: "RhythmTengokuWorld") -> None:
        self.world = world
    
    def set_rules(self) -> None:
        player = self.world.player
        options = self.world.options

        #def can_reach_level(state: CollectionState, name: str) -> bool:


        # Continue from here with rules
        # Take inspiration from ULTRAKILL