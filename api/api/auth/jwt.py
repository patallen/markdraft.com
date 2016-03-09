from datetime import datetime

from flask import request, Response, g
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature

from api import app
import functools as func
from marklib.formats import dates
from data.models import User


EXPIRE_TIME = app.config.get('JWT_EXPIRE_TIME')
SECRET_KEY = app.config.get('JWT_SECRET_KEY')

if app.config.get('JWT_TOKEN_PREFIX') is not None:
    JWT_PREFIX = "%s " % app.config.get('JWT_TOKEN_PREFIX')


jwt = TimedJSONWebSignatureSerializer(SECRET_KEY)


def generate_claims(claims=None):
    return {k: v for k, v in claims.iteritems()}


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
    except Exception as e:
        # Should either log here, or catch different exceptions
        return False
    return payload


def require_jwt(f):
    @func.wraps(f)
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
