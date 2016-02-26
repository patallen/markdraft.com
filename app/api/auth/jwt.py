from datetime import datetime

from itsdangerous import JSONWebSignatureSerializer, BadSignature
from flask import current_app as app

from marklib.formats import dates

EXPIRE_TIME = app.config.get('JWT_EXPIRE_TIME')
SECRET_KEY = app.config.get('JWT_SECRET_KEY')


jwt = JSONWebSignatureSerializer(SECRET_KEY)


def generate_claims(claims=None):
    now = dates.timestamp(datetime.now())
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


def verify_token(token):
    try:
        payload = jwt.loads(token)
    except BadSignature:
        print "Bad Signature"
        return False

    now = dates.timestamp(datetime.now())
    exp = payload.get('exp', 0)
    if int(now) > int(exp):
        return False
    return True
