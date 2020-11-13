import json
import os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from six.moves.urllib.request import urlopen


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    # from https://auth0.com/docs/quickstart/backend/python/01-authorization#create-the-jwt-validation-decorator
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    user_permissions = payload.get('permissions', None)
    if not user_permissions:
        raise AuthError({"code": "bad_request",
                         "description":
                         "Access token not in a valid format"
                         }, 400)
    if permission not in user_permissions:
        raise AuthError({"code": "unauthorized",
                         "description":
                         "You do not have needed presmissions "
                         "to complete this action"}, 403)
    return True


def verify_decode_jwt(token):
    # from  https://auth0.com/docs/quickstart/backend/python/01-authorization#create-the-jwt-validation-decorator
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if not rsa_key:
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer="https://"+AUTH0_DOMAIN+"/"
        )
    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired",
                         "description": "token is expired"}, 401)
    except jwt.JWTClaimsError:
        raise AuthError({"code": "invalid_claims",
                         "description":
                         "incorrect claims,"
                         "please check the audience and issuer"}, 401)
    except Exception:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Unable to parse authentication"
                         " token."}, 401)

    return payload


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator


# helpers


def current_user():
    return getattr(_request_ctx_stack.top, "current_user", None)
