from enum import Enum


class Strategy(Enum):
    POPULARITY_BASED = 'POPULARITY_BASED'
    CONTENT_BASED = 'CONTENT_BASED'
    COLLABORATIVE_BASED = 'COLLABORATIVE_BASED'
    DYNAMIC = 'DYNAMIC'
