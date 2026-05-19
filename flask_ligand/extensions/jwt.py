"""JWT authentication and authorization."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING

from flask import current_app
from flask_jwt_extended import JWTManager, get_current_user, verify_jwt_in_request
from jwt.algorithms import RSAAlgorithm
from requests import get
from requests.exceptions import RequestException

from flask_ligand.extensions.api import abort

# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable

    from flask import Flask


# ======================================================================================================================
# Globals
# ======================================================================================================================
JWT = JWTManager()


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
@dataclass
class User:
    """
    A simple class representing pertinent user information.

    Args:
        id: The UUID of the user.
        roles: A list of roles that the user has been assigned.
    """

    id: str
    roles: list[str]


# ======================================================================================================================
# Decorators: Public
# ======================================================================================================================
def jwt_role_required(role: str):  # type: ignore
    """A decorator for restricting access to an endpoint based on role membership.

    Note: This decorator style was chosen because of: https://stackoverflow.com/a/42581103

    Args:
        role: The role membership required by the user in order to access this endpoint.
    """

    def decorator(fn: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # standard flask_jwt_extended token verifications
            verify_jwt_in_request()

            if role not in current_app.config["ALLOWED_ROLES"]:
                abort(HTTPStatus(500), message="Endpoint required role is not an allowed role!")

            # custom role membership verification
            user: User = get_current_user()
            if role not in user.roles:
                abort(HTTPStatus(403), message=f"This endpoint requires the user to have the '{role}' role!")

            return fn(*args, **kwargs)

        return wrapper

    return decorator


# ======================================================================================================================
# Functions: Callbacks
# ======================================================================================================================
@JWT.user_lookup_loader
def user_lookup_callback(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> User:
    """This callback function is used to convert a JWT into a python object that can be used in a protected endpoint.

    Note: https://flask-jwt-extended.readthedocs.io/en/stable/api/#flask_jwt_extended.JWTManager.user_lookup_loader

    Args:
        _jwt_header: Header data of the JWT. (Unused argument)
        jwt_data: Payload data of the JWT.
    """

    return User(
        id=jwt_data["sub"],
        roles=jwt_data["realm_access"]["roles"],
    )


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def init_app(app: Flask) -> None:  # pragma: no cover (Covered by integration tests)
    """Initialize JWT."""

    verify_ssl_cert = app.config["VERIFY_SSL_CERT"]

    try:
        # Retrieve master openid-configuration endpoint from issuer realm
        oidc_config = get(app.config["OIDC_DISCOVERY_URL"], verify=verify_ssl_cert).json()

        # Retrieve data from jwks_uri endpoint
        oidc_jwks_uri = get(oidc_config["jwks_uri"], verify=verify_ssl_cert).json()
    except (RequestException, KeyError):
        raise RuntimeError(
            f"Failed to retrieve public key from the '{app.config['OIDC_DISCOVERY_URL']}' OIDC Discovery URL!"
        )

    # Retrieve first jwk entry from jwks_uri endpoint and use it to construct the RSA public key
    app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(json.dumps(oidc_jwks_uri["keys"][0]))  # type: ignore

    JWT.init_app(app)
