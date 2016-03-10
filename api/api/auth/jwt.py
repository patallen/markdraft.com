import functools as func

from itsdangerous import TimedJSONWebSignatureSerializer
from flask import request, Response, g, current_app as app

from data.models import User


def generate_claims(claims=None):
    return {k: v for k, v in claims.iteritems()}


def create_token_for_user(user):
    SECRET_KEY = app.config.get('JWT_SECRET_KEY')
    jwt = TimedJSONWebSignatureSerializer(SECRET_KEY)
    fname = user.first_name or user.username
    user = dict(
        username=user.username,
        user_id=user.id,
        first_name=fname
    )
    headers = {"typ": "JWT"}
    return jwt.dumps(generate_claims(user), header_fields=headers)


def verify_token(token):
    SECRET_KEY = app.config.get('JWT_SECRET_KEY')
    jwt = TimedJSONWebSignatureSerializer(SECRET_KEY)
    try:
        payload = jwt.loads(token)
    except Exception as e:
        # Should either log here, or catch different exceptions
        return False
    return payload


def require_jwt(f):
    @func.wraps(f)
    def wrapper(*args, **kwargs):
        JWT_PREFIX = app.config.get('JWT_TOKEN_PREFIX')
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
