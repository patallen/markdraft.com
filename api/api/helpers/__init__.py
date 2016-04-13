from flask import g
import math


def get_user():
    if hasattr(g, 'current_user'):
        return g.current_user


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


def format_result(result, page=None, limit=None, count=None):
    page, limit, count = [int(x) for x in (page, limit, count) if x]

    next_page, prev_page = None, None
    if limit * page < count:
        next_page = page + 1
    if page > 1:
        prev_page = page - 1

    pagination = dict(
        current=page,
        next=next_page,
        prev=prev_page,
        pages=math.ceil(count/limit)
    )
    result = dict(
        pagination=pagination,
        results=result
    )
    return result
