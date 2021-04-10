from PyQt5.QtCore import Qt
from enum import IntEnum


class UserRoles(IntEnum):
    MOVIE_ID = Qt.UserRole + 1,
    ACTOR_ID = Qt.UserRole + 2,
    CATEGORY_ID = Qt.UserRole + 3


class WindowSelectionRoles(IntEnum):
    ACTOR = 1,
    MOVIE = 2,
    CATEGORY = 3