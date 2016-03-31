import functools as func

from itsdangerous import TimedJSONWebSignatureSerializer
from flask import request, Response, g, current_app as app

from data.models import User
from marklib.request import MakeResponse


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


def create_refresh_token(user_id=None, agent=None):
    EXPIRES_IN = app.config.get('JWT_REFRESH_EXPIRY')
    SECRET_KEY = app.config.get('JWT_REFRESH_SECRET')
    jwt = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=EXPIRES_IN)

    if not (user_id and agent):
        raise ValueError

    payload = dict(u=user_id, a=agent)
    token = jwt.dumps(payload)

    return token


def verify_token(token, secret=None):
    SECRET_KEY = secret or app.config.get('JWT_SECRET_KEY')
    jwt = TimedJSONWebSignatureSerializer(SECRET_KEY)
    try:
        payload = jwt.loads(token)
    except Exception as e:
        # Should either log here, or catch different exceptions
        return False
    return payload


def generate_refresh_payload(user_id, agent):
    return dict(u=user_id, a=agent)


def verify_refresh_token(token, user_id, agent):
    SECRET_KEY = app.config.get('JWT_REFRESH_SECRET')
    payload = verify_token(token, SECRET_KEY)
    check_payload = generate_refresh_payload(user_id, agent)
    if payload == check_payload:
        return True
    return False


def require_jwt(f):
    @func.wraps(f)
    def wrapper(*args, **kwargs):
        JWT_PREFIX = app.config.get('JWT_TOKEN_PREFIX')
        auth_header = request.headers.get('Authorization', None)

        payload = None

        xhr = MakeResponse()
        xhr.set_error(401, "Authorization Required")

        if auth_header is None:
            return xhr.response

        if len(auth_header) > 0 and auth_header.startswith(JWT_PREFIX):
            payload = verify_token(auth_header[len(JWT_PREFIX):].strip())

        if not payload:
            return xhr.response

        user_id = payload.get('user_id')
        g.current_user = User.query.get(user_id)
        return f(*args, **kwargs)
    return wrapper
