# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import pytest
from typing import TYPE_CHECKING
from flask_ligand import create_app
from flask_ligand.extensions.jwt import JWT
from flask_ligand.extensions.database import DB
from flask_jwt_extended import create_access_token

pytest_plugins = ["flask_ligand"]


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from flask import Flask
    from typing import Any, Callable
    from flask.testing import FlaskClient
    from pytest_mock import MockerFixture


# ======================================================================================================================
# Fixtures: Public
# ======================================================================================================================
@pytest.fixture(scope="session")
def jwt_init_app() -> Callable[[Flask], None]:
    """Initialize JWT with basic access token capabilities."""

    return JWT.init_app


@pytest.fixture(scope="function")
def basic_flask_app(jwt_init_app: Callable[[Flask], None], open_api_client_name: str, mocker: MockerFixture) -> Flask:
    """A basic Flask app ready to be used for testing."""

    # Prevent JWT from retrieving public key from OIDC issuer URL
    mocker.patch("flask_ligand.extensions.jwt.init_app", side_effect=jwt_init_app)

    app = create_app(
        flask_env="testing",
        api_title="Flask Ligand Unit Testing Service",
        api_version="1.0.1",
        openapi_client_name=open_api_client_name,
    )

    with app.app_context():
        DB.create_all()

    return app


@pytest.fixture(scope="function")
def app_test_client(basic_flask_app: Flask) -> FlaskClient:
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
