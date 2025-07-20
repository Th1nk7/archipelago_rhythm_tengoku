from Options import Choice

class CheckType(Choice):
    """Which rank is required to clear a stage."""
    display_name = "Stage Check Type"
    option_completion = 0
    option_superb = 1
    option_perfect = 2


class RhythmTengokuOptions:
    check_type: CheckType
