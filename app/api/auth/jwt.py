from itsdangerous import JSONWebSignatureSerializer
from flask import current_app as app

EXPIRE_TIME = app.config.get('JWT_EXPIRE_TIME')
SECRET_KEY = app.config.get('JWT_SECRET_KEY')


jwt = JSONWebSignatureSerializer(SECRET_KEY)

import time
import math
from datetime import datetime


def timestamp(dt):
    stamp = time.mktime((
        dt.year, dt.month, dt.day, dt.hour,
        dt.minute, dt.second, -1, -1, -1)
    ) + dt.microsecond / 1e6
    return int(math.floor(stamp))


def generate_claims(claims=None):
    now = timestamp(datetime.now())
    exp = now + EXPIRE_TIME
    rv = {"iat": now, "exp": exp}
    for k, v in claims.iteritems():
        if not hasattr(rv, k):
            rv[k] = v
    return rv


def create_token_for_user(user):
    fname = user.first_name or user.username
    user = dict(
        username=user.username,
        user_id=user.id,
        first_name=fname
    )
    headers = {"typ": "JWT"}
    return jwt.dumps(generate_claims(user), header_fields=headers)
