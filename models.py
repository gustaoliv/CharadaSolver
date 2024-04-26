from enum import Enum


class State(Enum):
    NotTested = 1
    NotExists = 2
    WrongPlace = 3
    CorrectPlace = 4