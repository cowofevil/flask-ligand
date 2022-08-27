"""Tests for the "extensions.jwt" classes and functions."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import pytest
from typing import TYPE_CHECKING
from flask.views import MethodView
from flask.testing import FlaskClient
from marshmallow_sqlalchemy import auto_field
from flask_ligand.extensions.database import DB
from flask_ligand.extensions.jwt import jwt_role_required
from flask_ligand.extensions.api import Blueprint, AutoSchema


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from typing import Any
    from flask import Flask


# ======================================================================================================================
# Globals
# ======================================================================================================================
JWT_TEST_URL = "/jwttest/"
BLP = Blueprint(
    "JWT TEST",
    __name__,
    url_prefix=JWT_TEST_URL.rstrip("/"),
    description="JWT TEST",
)
USER_ROLES = ["user"]
ADMIN_ROLES = ["user", "admin"]


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
class JwtTestModel(DB.Model):  # type: ignore
    """Test model class."""

    __tablename__ = "jwttest"

    message = DB.Column(DB.String(), primary_key=True, nullable=False)


class JwtTestSchema(AutoSchema):
    """Automatically generate schema from 'JwtTestModel'."""

    class Meta(AutoSchema.Meta):
        model = JwtTestModel

    message = auto_field(required=True)


@BLP.route("/")
class JwtTestView(MethodView):
    @BLP.etag
    @BLP.response(200, JwtTestSchema(many=True))
    @jwt_role_required(role="user")
    def get(self):

        items: list[JwtTestModel] = JwtTestModel.query.all()

        return items

    @BLP.etag
    @BLP.arguments(JwtTestSchema)
    @BLP.response(201, JwtTestSchema)
    def post(self, new_item):
        item = JwtTestModel(**new_item)
        DB.session.add(item)
        DB.session.commit()

        return item


@BLP.route("/broken/")
class JwtBrokenView(MethodView):
    @BLP.etag
    @BLP.response(200, JwtTestSchema(many=True))
    @jwt_role_required(role="broken")
    def get(self):

        items: list[JwtTestModel] = JwtTestModel.query.all()

        return items


# ======================================================================================================================
# Fixtures
# ======================================================================================================================
@pytest.fixture(scope="session")
def jwt_test_url() -> str:
    """The URL for testing the 'JwtTestView' endpoint."""

    return JWT_TEST_URL


@pytest.fixture(scope="function")
def jwt_test_data_set() -> list[dict[str, Any]]:
    """Test data set for the 'JwtTestView' endpoint."""

    data_set = [{"message": f"message_{i}"} for i in range(3)]

    return data_set


@pytest.fixture(scope="function")
def jwt_test_client(basic_flask_app: Flask) -> FlaskClient:
    """Flask app test client with 'JwtTestView' pre-configured."""

    basic_flask_app.register_blueprint(BLP)

    return basic_flask_app.test_client()


@pytest.fixture(scope="function")
def primed_test_client(
    jwt_test_client: FlaskClient, jwt_test_url: str, jwt_test_data_set: list[dict[str, Any]]
) -> FlaskClient:
    """Flask app configured for testing with the database pre-populated with test data."""

    for jwt_test_data_item in jwt_test_data_set:
        with jwt_test_client.post(jwt_test_url, json=jwt_test_data_item) as ret:
            assert ret.status_code == 201

    return jwt_test_client


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestJwtExtension(object):
    """Test cases for verifying the JWT decorators."""

    # noinspection PyTestParametrized
    @pytest.mark.parametrize("default_roles", [USER_ROLES, ADMIN_ROLES])
    def test_authorized_role(self, primed_test_client, jwt_test_url, access_token_headers):
        """Verify that the current user role is authorized to access endpoint"""

        with primed_test_client.get(jwt_test_url, headers=access_token_headers) as ret:
            assert ret.status_code == 200
            assert len(ret.json) == 3


class TestNegativeJwtExtension(object):
    """Negative test cases for verifying the JWT decorators."""

    # noinspection PyTestParametrized
    @pytest.mark.parametrize("default_roles", [["insufficient_role"]])
    def test_unauthorized_role(self, primed_test_client, jwt_test_url, access_token_headers):
        """
        Verify that the correct HTTP code is returned when attempting to access a protected endpoint using a JWT
        access token that doesn't have the appropriate role specified to access the endpoint.

        Note: This test does a trick with parameterization to override the implicitly imported "default_roles"
        fixture. See this documentation for more details:

        https://docs.pytest.org/en/6.2.x/fixture.html#override-a-fixture-with-direct-test-parametrization
        """

        with primed_test_client.get(jwt_test_url, headers=access_token_headers) as ret:
            assert ret.status_code == 403
            assert ret.json["message"] == "This endpoint requires the user to have the 'user' role!"

    def test_role_not_allowed(self, primed_test_client, jwt_test_url, access_token_headers):
        """
        Verify that the correct exception is raised when trying to access an endpoint that is decorated with a role
        that is not allowed.

        Note: This test does a trick with parameterization to override the implicitly imported "default_roles"
        fixture. See this documentation for more details:

        https://docs.pytest.org/en/6.2.x/fixture.html#override-a-fixture-with-direct-test-parametrization
        """

        with primed_test_client.get(f"{jwt_test_url}broken/", headers=access_token_headers) as ret:
            assert ret.status_code == 500
            assert ret.json["message"] == "Endpoint required role is not an allowed role!"
