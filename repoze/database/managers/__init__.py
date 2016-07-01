"""Manager package compiler."""

from database.managers.basic import BasicManager
from database.managers.user import UserManager
from database.managers.post import PostsManager


__all__ = ('BasicManager', 'UserManager', 'PostsManager')
