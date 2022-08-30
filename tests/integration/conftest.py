# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import pytest
from os import walk
from os.path import join
from requests import post
from dotenv import dotenv_values
from typing import TYPE_CHECKING
from flask.views import MethodView
from flask_ligand import create_app
from flask_migrate import downgrade
from flask.testing import FlaskClient
from marshmallow_sqlalchemy import auto_field
from flask_ligand.extensions.database import DB
from flask_ligand.extensions.jwt import jwt_role_required
from flask_ligand.extensions.api import Blueprint, AutoSchema

pytest_plugins = ["flask_ligand"]


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from flask import Flask
    from typing import Any, Optional


# ======================================================================================================================
# Globals
# ======================================================================================================================
INTEGRATION_TEST_URL = "/integration-test/"
MIGRATION_DIRECTORY = "tests/integration/migrations"
BLP = Blueprint(
    "INTEGRATION TEST",
    __name__,
    url_prefix=INTEGRATION_TEST_URL.rstrip("/"),
    description="JWT TEST",
)


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
class IntegrationTestModel(DB.Model):  # type: ignore
    """Test model class."""

    __tablename__ = "integration_test"

    message = DB.Column(DB.String(), primary_key=True, nullable=False)


class IntegrationTestSchema(AutoSchema):
    """Automatically generate schema from 'IntegrationTestModel'."""

    class Meta(AutoSchema.Meta):
        model = IntegrationTestModel

    message = auto_field(required=True)


@BLP.route("/")
class IntegrationTestView(MethodView):
    @BLP.etag
    @BLP.response(200, IntegrationTestSchema(many=True))
    @jwt_role_required(role="user")
    def get(self):

        items: list[IntegrationTestModel] = IntegrationTestModel.query.all()

        return items

    @BLP.etag
    @BLP.arguments(IntegrationTestSchema)
    @BLP.response(201, IntegrationTestSchema)
    def post(self, new_item):
        item = IntegrationTestModel(**new_item)
        DB.session.add(item)
        DB.session.commit()

        return item


# ======================================================================================================================
# Fixtures
# ======================================================================================================================
@pytest.fixture(scope="session")
def integration_test_url() -> str:
    """The URL for testing the 'IntegrationTestView' endpoint."""

    return INTEGRATION_TEST_URL


@pytest.fixture(scope="session")
def migration_directory() -> str:
    """The path to the migrations folder used by Flask-Migrate."""

    return MIGRATION_DIRECTORY


@pytest.fixture(scope="function")
def integration_test_data_set() -> list[dict[str, Any]]:
    """Test data set for the 'IntegrationTestView' endpoint."""

    data_set = [{"message": f"message_{i}"} for i in range(3)]

    return data_set


@pytest.fixture(scope="session")
def int_testing_env_vars() -> dict[str, Optional[str]]:
    """The full bevy of integration testing environment variables stored in the 'docker/env_files/*.env' files."""

    env_vars = {}

    for root, _, files in walk("docker/env_files"):
        for file in files:
            env_vars.update(dotenv_values(join(root, file)))

    return env_vars


@pytest.fixture(scope="session")
def access_token_headers(int_testing_env_vars: dict[str, Optional[str]]) -> dict[str, Any]:
    """
    JWT access token headers ready to use for making requests against protected endpoints using the 'admin'
    composite role.
    """

    # noinspection HttpUrlsUsage
    token_url = (
        f"http://{int_testing_env_vars['KC_HOSTNAME']}:{int_testing_env_vars['KC_PORT']}/"
        f"realms/{int_testing_env_vars['KC_REALM']}/"
        "protocol/openid-connect/token"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = (
        f"grant_type=client_credentials&"
        f"client_id={int_testing_env_vars['KC_CLIENT_ID']}&"
        f"client_secret={int_testing_env_vars['KC_CLIENT_SECRET']}"
    )

    access_token = post(token_url, data=payload, headers=headers, verify=False).json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="session")
def access_token_headers_no_roles(int_testing_env_vars: dict[str, Optional[str]]) -> dict[str, Any]:
    """JWT access token headers that lack the necessary roles for accessing protected endpoints."""

    # noinspection HttpUrlsUsage
    token_url = (
        f"http://{int_testing_env_vars['KC_HOSTNAME']}:{int_testing_env_vars['KC_PORT']}/"
        f"realms/{int_testing_env_vars['KC_REALM']}/"
        "protocol/openid-connect/token"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = (
        f"grant_type=client_credentials&"
        f"client_id={int_testing_env_vars['KC_CLIENT_ID_NO_ROLES']}&"
        f"client_secret={int_testing_env_vars['KC_CLIENT_SECRET']}"
    )

    access_token = post(token_url, data=payload, headers=headers, verify=False).json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
def basic_flask_app(
    open_api_client_name: str,
    migration_directory: str,
    int_testing_env_vars: dict[str, Optional[str]],
) -> Flask:
    """A basic Flask app ready to be used for testing."""

    db_uri = (
        f"postgresql+pg8000://"
        f"{int_testing_env_vars['POSTGRES_USER']}:{int_testing_env_vars['POSTGRES_PASSWORD']}@"
        f"{int_testing_env_vars['LOCAL_HOSTNAME']}:"
        f"{int_testing_env_vars['POSTGRES_PORT']}/"
        f"{int_testing_env_vars['LOCAL_APP_DB_NAME']}"
    )

    # noinspection HttpUrlsUsage
    override_settings = {
        "OIDC_ISSUER_URL": f"http://{int_testing_env_vars['KC_HOSTNAME']}:{int_testing_env_vars['KC_PORT']}",
        "OIDC_REALM": f"{int_testing_env_vars['KC_REALM']}",
        "SQLALCHEMY_DATABASE_URI": db_uri,
        "DB_AUTO_UPGRADE": True,
        "DB_MIGRATION_DIR": migration_directory,
    }

    return create_app(
        flask_env="local",
        api_title="Flask Ligand Integration Testing Service",
        api_version="1.0.1",
        openapi_client_name=open_api_client_name,
        **override_settings,
    )


@pytest.fixture(scope="function")
def app_test_client(basic_flask_app: Flask, migration_directory: str) -> FlaskClient:
    """Flask app test client with 'IntegrationTestView' pre-configured."""

    basic_flask_app.register_blueprint(BLP)

    yield basic_flask_app.test_client()

    # Teardown
    with basic_flask_app.app_context():
        downgrade(directory=migration_directory)


@pytest.fixture(scope="function")
def primed_test_client(
    app_test_client: FlaskClient,
    integration_test_url: str,
    integration_test_data_set: list[dict[str, Any]],
) -> FlaskClient:
    """Flask app configured for testing with the database pre-populated with test data."""

    for integration_test_data_item in integration_test_data_set:
        with app_test_client.post(integration_test_url, json=integration_test_data_item) as ret:
            assert ret.status_code == 201

    return app_test_client
