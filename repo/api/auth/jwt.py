from datetime import datetime

from flask import request, Response, g
from itsdangerous import JSONWebSignatureSerializer, BadSignature

from api import app
from marklib.formats import dates
from models import User


EXPIRE_TIME = app.config.get('JWT_EXPIRE_TIME')
SECRET_KEY = app.config.get('JWT_SECRET_KEY')

if app.config.get('JWT_TOKEN_PREFIX') is not None:
    JWT_PREFIX = "%s " % app.config.get('JWT_TOKEN_PREFIX')


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
    return payload


def require_jwt(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)

        if auth_header is None:
            return Response("Authorization Required"), 401

        token = None
        if auth_header.startswith(JWT_PREFIX):
            token = auth_header[len(JWT_PREFIX):]

        if token is None:
            return Response("Authorization Required"), 401

        payload = verify_token(token)
        if not payload:
            return Response("Could not authorize."), 401

        user_id = payload.get('user_id')
        g.current_user = User.query.get(user_id)
        return f(*args, **kwargs)
    return wrapper
