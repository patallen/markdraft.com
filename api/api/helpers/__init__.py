from flask import g
from data.models import User


def get_user():
    if hasattr(g, 'current_user'):
        return g.current_user
    if hasattr(g, 'current_user_id'):
        user = User.query.get(g.current_user_id)
        return user
    return None


def filter_by_access(user, entities, permissions=None):
    if permissions is None:
        permissions = ('read',)

    accessible = []
    for entity in entities:
        has_permissions = True
        for perm in permissions:
            if not entity.user_has_access(user, perm):
                has_permissions = False
                break
        if has_permissions:
            accessible.append(entity)

    return accessible
