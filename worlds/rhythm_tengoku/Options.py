from Options import Choice, Range, Toggle, DefaultOnToggle, OptionSet
from dataclasses import dataclass
from Options import OptionDict

class ProgressionBalancing(Range):
    """Move progression items earlier to avoid early-game bottlenecks.
    0 = off, 99 = maximum balancing"""
    display_name = "Progression Balancing"
    range_start = 0
    range_end = 99
    default = 50


class Accessibility(Choice):
    """Set item/goal reachability rules.
    Full: all items reachable
    Minimal: only goal-required items reachable"""
    display_name = "Accessibility Rules"
    option_full = 0
    option_minimal = 1
    default = 0


class GoalType(Choice):
    """Select goal type:
    clear_all_goals: beat levels
    superb_all_goals: get superb rank
    perfect_all_goals: get perfect rank"""
    display_name = "Goal Type"
    option_clear_all_goals = 0
    option_superb_all_goals = 1
    option_perfect_all_goals = 2
    default = 1


class GoalLevels(OptionSet):
    """Set of level indices that must be completed to reach goal."""
    display_name = "Goal Levels"
    valid_keys = list(range(0, 49))
    default = [41, 42, 43, 44, 45, 46, 47, 48]  # Remix levels


class ExcludedLevels(OptionSet):
    """Levels excluded from item pool or progression."""
    display_name = "Excluded Levels"
    valid_keys = list(range(0, 49))
    default = []


class StartLevel(OptionSet):
    """Levels available at game start."""
    display_name = "Start Level(s)"
    valid_keys = list(range(0, 49))
    default = [0]


class RankRewards(Choice):
    """Which ranks give item rewards.
    Options:
    C: Clear
    S: Superb
    P: Perfect
    CS, CP, SP, CSP = combinations"""
    display_name = "Rank Reward Type"
    option_C = 0
    option_S = 1
    option_P = 2
    option_CS = 3
    option_CP = 4
    option_SP = 5
    option_CSP = 6
    default = 3  # CS


# TODO: Add TrapOptions, DeathLink options when implemented


RHYTHM_TENGOKU_OPTION_DEFINITIONS = {
    "progression_balancing": ProgressionBalancing,
    "accessibility": Accessibility,
    "goal": GoalType,
    "goal_levels": GoalLevels,
    "excluded_levels": ExcludedLevels,
    "start_level": StartLevel,
    "rank_rewards": RankRewards,
}

@dataclass
class RhythmTengokuOptions(OptionDict):
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility
    goal: GoalType
    goal_levels: GoalLevels
    excluded_levels: ExcludedLevels
    start_level: StartLevel
    rank_rewards: RankRewards