"""Module providing Enum class for inheriting"""
from enum import Enum


class Team(Enum):
    """This enum represents every teams in game"""
    # Red team
    RED = 1
    R = 1

    # Black/Blue team
    BLACK = -1
    BLUE = -1
    B = -1

    # None team
    NONE = 0
    N = 0

    def __str__(self):
        return self.name.lower()
