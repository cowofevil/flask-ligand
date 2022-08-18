# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import flask
import pytest
from typing import TYPE_CHECKING
from flask.testing import FlaskClient
from pytest_mock import MockerFixture
from flask_ligand import create_app
from flask_jwt_extended import create_access_token
from flask_ligand.extensions.jwt import JWT

pytest_plugins = ["flask_ligand"]


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from typing import Any, Callable


# ======================================================================================================================
# Fixtures: Public
# ======================================================================================================================
@pytest.fixture(scope="session")
def jwt_init_app() -> Callable[[flask.Flask], None]:
    """Initialize JWT with basic access token capabilities."""

    return JWT.init_app


@pytest.fixture(scope="function")
def basic_flask_app(
    jwt_init_app: Callable[[flask.Flask], None], open_api_client_name: str, mocker: MockerFixture
) -> flask.Flask:
    """A basic Flask app ready to be used for testing."""

    # Prevent JWT from retrieving public key from OIDC issuer URL
    mocker.patch("flask_ligand.extensions.jwt.init_app", side_effect=jwt_init_app)

    return create_app(
        flask_env="testing",
        api_title="Flask Ligand Service",
        api_version="1.0.1",
        openapi_client_name=open_api_client_name,
    )


@pytest.fixture(scope="function")
def app_test_client(basic_flask_app: flask.Flask) -> FlaskClient:
    """Flask app test client."""

    return basic_flask_app.test_client()


@pytest.fixture(scope="function")
def access_token_headers(app_test_client: FlaskClient, user_info: dict[str, str]) -> dict[str, Any]:
    """
    JWT access token headers ready to use for making requests against protected endpoints using the 'admin'
    composite role.
    """

    jwt_claims = {
        "sub": user_info["id"],
        "realm_access": {"roles": user_info["roles"]},
    }

    with app_test_client.application.app_context():
        jwt_access_token = create_access_token("username", fresh=True, additional_claims=jwt_claims)

    return {"Authorization": f"Bearer {jwt_access_token}"}
