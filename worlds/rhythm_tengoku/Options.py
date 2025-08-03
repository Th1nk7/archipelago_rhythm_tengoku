import typing
from dataclasses import dataclass
from Options import Choice, Range, OptionSet, Toggle, DefaultOnToggle, ItemDict, DeathLink, PerGameCommonOptions
from .Regions import Regions
from .Items import group_dict

class ItemWeights(ItemDict):
    def __init__(self, value: typing.Dict[str, int]):
        if any(item_count < 0 for item_count in value.values()):
            raise Exception("Cannot have negative item counts.")
        if all(item_count == 0 for item_count in value.values()):
            raise Exception("At least one item count must be positive.")
        super(ItemDict, self).__init__(value)

class StartingLevels(OptionSet):
    """
    Levels the player starts with. Minimum 1 level must be specified.
    """
    display_name = "Starting Levels"
    valid_keys = {r.name for r in Regions.all_regions}
    default = {"Karate Man"}

class GoalLevels(OptionSet):
    """
    Levels that must be completed to win. Minimum 1 level must be specified.
    """
    display_name = "Goal Levels"
    valid_keys = {r.name for r in Regions.all_regions}
    default = {"Remix 1", "Remix 2", "Remix 3", "Remix 4", "Remix 5", "Remix 6", "Remix 7", "Remix 8"}

class GoalRank(Choice):
    """
    Rank required on all goal levels in order to complete goal.
    """
    display_name = "Goal Rank"
    option_ok = 0
    option_superb = 1
    option_perfect = 2
    default = 1

class SkipLevels(OptionSet):
    """
    Exclude level locations and items
    """
    display_name = "Skipped Levels"
    valid_keys = {r.name for r in Regions.all_regions}
    default = {"Quiz Show"}

class OkRewards(DefaultOnToggle):
    """
    Adds rewards for getting OK rank on levels.
    """
    display_name = "OK Rewards"

class SuperbRewards(DefaultOnToggle):
    """
    Adds rewards for getting SUPERB rank on levels.
    """
    display_name = "SUPERB Rewards"

class PerfectRewards(Toggle):
    """
    Adds rewards for getting PERFECT rank on levels.
    """
    display_name = "PERFECT Rewards"

class TrapPercent(Range):
    """
    Choose the percentage of trap items that will appear when filling the item pool with junk.
    """
    display_name = "Trap Item Percentage"
    range_start = 0
    range_end = 100
    default = 25

class FillerWeights(ItemWeights):
    """Choose the odds of each filler item being created when filling the item pool with junk."""
    display_name = "Filler Item Weights"
    valid_keys = group_dict["filler"]
    default = {item: 50 for item in group_dict["filler"]}

class TrapWeights(ItemWeights):
    """Choose the odds of each trap item being created when filling the item pool with traps."""
    display_name = "Trap Item Weights"
    valid_keys = group_dict["trap"]
    default = {item: 50 for item in group_dict["trap"]}

class RTDeathLink(DeathLink):
    """
    When you fail a level (TRY AGAIN), everyone dies. The reverse is also true.

    Death in this game simply exits the level.
    """

@dataclass
class RhythmTengokuOptions(PerGameCommonOptions):
    starting_levels: StartingLevels
    goal_levels: GoalLevels
    goal_rank: GoalRank
    skipped_levels: SkipLevels
    ok_rewards: OkRewards
    superb_rewards: SuperbRewards
    perfect_rewards: PerfectRewards
    trap_percent: TrapPercent
    filler_weights: FillerWeights
    trap_weights: TrapWeights
    death_link: RTDeathLink
    