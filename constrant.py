from enum import Enum

RESOLUTION = (1280, 720)
TITLE = "Miner"


class SceneCode(Enum):
    HOME = 0
    BEFORE = 1
    PLAYING = 2
    AFTER = 3
    STORE = 4