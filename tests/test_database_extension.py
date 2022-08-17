"""Tests for the "extensions.database" classes and functions."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import uuid
import pytest

# noinspection PyPackageRequirements
from marshmallow import fields

from typing import TYPE_CHECKING
from flask.views import MethodView
from flask.testing import FlaskClient

# noinspection PyPackageRequirements
from marshmallow.validate import Length

from marshmallow_sqlalchemy import field_for
from sqlalchemy_utils.types.uuid import UUIDType
from flask_ligand.extensions.database import DB
from flask_ligand.extensions.api import Blueprint, SQLCursorPage, Schema, AutoSchema


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from flask import Flask
    from typing import Any


# ======================================================================================================================
# Globals
# ======================================================================================================================
NAME_MAX_LENGTH = 255
NAME_VALIDATOR = Length(min=1, max=NAME_MAX_LENGTH)
DATABASE_TEST_URL: str = "/dbtest/"
BLP = Blueprint(
    "DB TEST",
    __name__,
    url_prefix=DATABASE_TEST_URL.rstrip("/"),
    description="DB TEST",
)


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
class DatabaseTestModel(DB.Model):  # type: ignore
    """Test model class."""

    __tablename__ = "databasetest"

    id = DB.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = DB.Column(DB.String(length=NAME_MAX_LENGTH), nullable=False)


class DatabaseTestSchema(AutoSchema):
    """Automatically generate schema from 'DatabaseTestModel'."""

    class Meta(AutoSchema.Meta):
        model = DatabaseTestModel

    id = field_for(DatabaseTestModel, "id", dump_only=True)
    name = field_for(DatabaseTestModel, "name", required=True, validate=NAME_VALIDATOR)


class DatabaseTestQueryArgsSchema(Schema):
    """A schema for filtering 'DatabaseTestSchema'."""

    # noinspection PyTypeChecker
    name = fields.Str(validate=NAME_VALIDATOR)


@BLP.route("/")
class DatabaseTestView(MethodView):
    @BLP.etag
    @BLP.arguments(DatabaseTestQueryArgsSchema, location="query")
    @BLP.response(200, DatabaseTestSchema(many=True))
    @BLP.paginate(SQLCursorPage)  # noqa
    def get(self, args):

        return DatabaseTestModel.query.filter_by(**args)

    @BLP.etag
    @BLP.arguments(DatabaseTestSchema)
    @BLP.response(201, DatabaseTestSchema)
    def post(self, new_item):

        item = DatabaseTestModel(**new_item)
        DB.session.add(item)
        DB.session.commit()

        return item


@BLP.route("/first")
class DatabaseTestViewFirst(MethodView):
    @BLP.etag
    @BLP.response(200, DatabaseTestSchema)
    def get(self):

        return DatabaseTestModel.query.first_or_404(description="Database is empty!")


@BLP.route("/<uuid:item_id>")
class DatabaseTestViewById(MethodView):
    @BLP.etag
    @BLP.response(200, DatabaseTestSchema)
    def get(self, item_id):

        return DatabaseTestModel.query.get_or_404(item_id, description="Invalid item!")

    @BLP.etag
    @BLP.arguments(DatabaseTestSchema)
    @BLP.response(200, DatabaseTestSchema)
    def put(self, new_item, item_id):

        item = DatabaseTestModel.query.get_or_404(item_id, description="Invalid item!")
        BLP.check_etag(item, DatabaseTestSchema)
        DatabaseTestSchema().update(item, new_item)
        DB.session.add(item)
        DB.session.commit()

        return item


# ======================================================================================================================
# Fixtures
# ======================================================================================================================
@pytest.fixture(scope="session")
def db_test_url() -> str:
    """The URL for testing the 'DatabaseTestView' endpoint."""

    return DATABASE_TEST_URL


@pytest.fixture(scope="function")
def db_test_data_set() -> list[dict[str, Any]]:
    """Test data set for the 'DatabaseTestView' endpoint."""

    data_set = [{"name": f"test_name_{i}"} for i in range(3)]

    return data_set


@pytest.fixture(scope="function")
def db_test_client(basic_flask_app: Flask) -> FlaskClient:
    """Flask app test client with 'DatabaseTestView' pre-configured."""

    basic_flask_app.register_blueprint(BLP)

    return basic_flask_app.test_client()


@pytest.fixture(scope="function")
def primed_test_client(
    db_test_client: FlaskClient, db_test_url: str, db_test_data_set: list[dict[str, Any]]
) -> FlaskClient:
    """Flask app configured for testing with the database pre-populated with test data."""

    for i in range(3):
        with db_test_client.post(db_test_url, json=db_test_data_set[i]) as ret:
            assert ret.status_code == 201

    return db_test_client


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestDatabaseExtension(object):
    """Test cases for creating DB models and auto-schemas."""

    def test_add_items(self, primed_test_client):
        """Verify that items can be added."""

        assert primed_test_client

    @pytest.mark.parametrize("name", ["a", "a" * 255])
    def test_add_item_with_name_boundary_check(self, name, db_test_client, db_test_url, helpers):
        """Verify that a question can be added with a minimal and maximal allowable name length."""

        item_exp = {"name": name}

        with db_test_client.post(db_test_url, json=item_exp) as ret:
            assert ret.status_code == 201
            assert helpers.is_sub_dict(item_exp, ret.json)

    def test_get_all(self, primed_test_client, db_test_url):
        """Verify that the endpoint returns all items."""

        with primed_test_client.get(db_test_url) as ret:
            assert ret.status_code == 200
            assert len(ret.json) == 3

    def test_get_first(self, primed_test_client, db_test_url, db_test_data_set, helpers):
        """Verify that the endpoint returns the first item."""

        with primed_test_client.get(f"{db_test_url}first") as ret:
            assert ret.status_code == 200
            assert helpers.is_sub_dict(db_test_data_set[0], ret.json)

    def test_get_with_pagination(self, primed_test_client, db_test_url, helpers):
        """Verify that the endpoint supports pagination."""

        with primed_test_client.get(f"{db_test_url}?page=1&page_size=2") as ret:
            assert ret.status_code == 200
            assert len(ret.json) == 2

            assert helpers.loads(ret.headers["X-Pagination"])["total"] == 3
            assert helpers.loads(ret.headers["X-Pagination"])["total_pages"] == 2

    def test_filter_by_name(self, primed_test_client, db_test_url, db_test_data_set, helpers):
        """Verify that an item can be retrieved by name."""

        item_exp = db_test_data_set[0]

        with primed_test_client.get(f"{db_test_url}?name={item_exp['name']}") as ret:
            assert ret.status_code == 200
            assert helpers.is_sub_dict(item_exp, ret.json[0])

    def test_update_item(self, primed_test_client, db_test_url, db_test_data_set, helpers):
        """Verify that an item can be updated with new data."""

        item_id = primed_test_client.get(db_test_url).json[0]["id"]
        item_etag = primed_test_client.get(f"{db_test_url}{item_id}").headers["ETag"]
        item_exp = {"name": "updated_test_name_0"}

        with primed_test_client.put(f"{db_test_url}{item_id}", headers={"If-Match": item_etag}, json=item_exp) as ret:
            assert ret.status_code == 200

        with primed_test_client.get(f"{db_test_url}{item_id}") as ret:
            assert ret.status_code == 200
            assert helpers.is_sub_dict(item_exp, ret.json)


class TestNegativeDatabaseExtension(object):
    """Negative test cases for creating DB models and auto-schemas."""

    def test_add_item_with_invalid_data(self, db_test_client, db_test_url):
        """Verify that the correct HTTP code is returned when an invalid data is sent."""

        item_exp = {"not": "valid"}

        with db_test_client.post(db_test_url, json=item_exp) as ret:
            assert ret.status_code == 422

    @pytest.mark.parametrize("name", ["", "a" * 256])
    def test_add_item_with_name_neg_boundary_check(self, name, db_test_client, db_test_url):
        """Verify that the correct HTTP code is returned when the name is outside the allowable length."""

        item_exp = {"name": name}

        with db_test_client.post(db_test_url, json=item_exp) as ret:
            assert ret.status_code == 422

    def test_filter_items_no_results(self, primed_test_client, db_test_url):
        """Verify that a filter specifying a value that does not exist returns no results."""

        with primed_test_client.get(f"{db_test_url}?name=does_not_exist") as ret:
            assert ret.status_code == 200
            assert len(ret.json) == 0

    def test_get_by_invalid_item_id(self, primed_test_client, db_test_url, dummy_id):
        """Verify that the correct HTTP code is returned when an invalid item ID is specified."""

        with primed_test_client.get(f"{db_test_url}{dummy_id}") as ret:
            assert ret.status_code == 404

    def test_first_item_in_empty_database(self, db_test_client, db_test_url):
        """
        Verify that the correct HTTP code is returned when attempting to retrieve the first item from an empty
        database.
        """

        with db_test_client.get(f"{db_test_url}first") as ret:
            assert ret.status_code == 404
