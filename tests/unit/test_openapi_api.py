"""Tests for the 'openapi' API endpoint"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import pytest
import flask_ligand
from typing import TYPE_CHECKING
from click.testing import CliRunner
from unittest.mock import MagicMock
from flask_ligand import create_app
from pytest_mock import MockerFixture

# noinspection PyProtectedMember
from flask_ligand.controllers import _gen_openapi_client_dl_link, gen_python_dl_link, gen_typescript_dl_link


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from flask import Flask


# ======================================================================================================================
# Globals
# ======================================================================================================================
OPENAPI_URL: str = "/openapi/"


# ======================================================================================================================
# Fixtures
# ======================================================================================================================
@pytest.fixture(scope="session")
def typescript_axios_url() -> str:
    """The URL for the 'openapi/typescript-axios' API endpoint."""

    return f"{OPENAPI_URL}typescript-axios/"


@pytest.fixture(scope="session")
def python_url() -> str:
    """The URL for the 'openapi/python' API endpoint."""

    return f"{OPENAPI_URL}python/"


@pytest.fixture(scope="function")
def offline_flask_app(
    open_api_client_name: str,
    mocker: MockerFixture,
) -> Flask:
    """A basic Flask app ready to be used for offline testing."""

    mocked_env = {
        "SERVICE_PUBLIC_URL": "http://public.url",
        "SERVICE_PRIVATE_URL": "http://private.url",
        "ALLOWED_ROLES": "user,admin",
        "OIDC_DISCOVERY_URL": "TESTING",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "OPENAPI_GEN_SERVER_URL": "http://api.openapi-generator.tech",
    }

    mocker.patch.dict("os.environ", mocked_env)

    app, _ = create_app(
        flask_app_name="flask_ligand_offline_unit_testing",
        flask_env="cli",
        api_title="Flask Ligand Offline Unit Testing Service",
        api_version="1.0.1",
        openapi_client_name=open_api_client_name,
    )

    return app


@pytest.fixture(scope="function")
def mock_gen_openapi_client_dl_link(mocker: MockerFixture) -> MagicMock:
    """Magic Mock of 'flask_ligand.controllers._gen_openapi_client_dl_link'."""

    magic_mock = mocker.create_autospec(spec=_gen_openapi_client_dl_link)
    mocker.patch("flask_ligand.controllers._gen_openapi_client_dl_link", side_effect=magic_mock)

    return magic_mock


@pytest.fixture(scope="function")
def mock_gen_python_dl_link(mocker: MockerFixture) -> MagicMock:
    """Magic Mock of 'flask_ligand.controllers.gen_python_dl_link'."""

    magic_mock = mocker.create_autospec(spec=gen_python_dl_link)
    mocker.patch("flask_ligand.cli.gen_python_dl_link", side_effect=magic_mock)

    return magic_mock


@pytest.fixture(scope="function")
def mock_gen_typescript_dl_link(mocker: MockerFixture) -> MagicMock:
    """Magic Mock of 'flask_ligand.controllers.gen_typescript_dl_link'."""

    magic_mock = mocker.create_autospec(spec=gen_typescript_dl_link)
    mocker.patch("flask_ligand.cli.gen_typescript_dl_link", side_effect=magic_mock)

    return magic_mock


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestOpenApiTypescriptAxios(object):
    """Test cases for generating clients from the 'openapi/typescript-axios/' endpoint."""

    def test_gen_client_no_params(
        self, app_test_client, typescript_axios_url, open_api_client_name, mock_gen_openapi_client_dl_link
    ):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when no URL parameters are provided."""

        with app_test_client.get(typescript_axios_url):
            assert mock_gen_openapi_client_dl_link.call_args.args[1] is True

            assert mock_gen_openapi_client_dl_link.call_args.args[2] == "typescript-axios"

            assert mock_gen_openapi_client_dl_link.call_args.args[3] == {
                "npmName": open_api_client_name,
                "npmVersion": flask_ligand.__version__,
                "supportsES6": True,
                "useSingleRequestParameter": True,
            }

    def test_gen_client_private(self, app_test_client, typescript_axios_url, mock_gen_openapi_client_dl_link):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{typescript_axios_url}?use_private_url=true"):
            assert mock_gen_openapi_client_dl_link.call_args.args[1] is True

    def test_gen_client_public(self, app_test_client, typescript_axios_url, mock_gen_openapi_client_dl_link):
        """Verify that the 'SERVICE_PUBLIC_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{typescript_axios_url}?use_private_url=false"):
            assert mock_gen_openapi_client_dl_link.call_args.args[1] is False


class TestNegativeOpenApiTypescriptAxios(object):
    """Negative test cases for getting clients from the 'openapi/typescript-axios/' endpoint."""

    def test_gen_client_when_open_svc_unavailable(self, app_test_client, typescript_axios_url):
        """
        Verify that the correct HTTP code is returned when attempting to get a client when the 'openapi' service is
        unavailable.
        """

        with app_test_client.get(typescript_axios_url) as ret:
            assert ret.status_code == 500


class TestOpenApiPython(object):
    """Test cases for generating clients from the 'openapi/python/' endpoint."""

    def test_gen_client_no_params(
        self, app_test_client, python_url, open_api_client_name, mock_gen_openapi_client_dl_link
    ):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when no URL parameters are provided."""

        with app_test_client.get(python_url):
            assert mock_gen_openapi_client_dl_link.call_args.args[1] is True

            assert mock_gen_openapi_client_dl_link.call_args.args[2] == "python-prior"

            assert mock_gen_openapi_client_dl_link.call_args.args[3] == {
                "packageName": open_api_client_name.replace("-", "_"),
                "projectName": open_api_client_name,
                "packageVersion": flask_ligand.__version__,
            }

    def test_gen_client_private(self, app_test_client, python_url, mock_gen_openapi_client_dl_link):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{python_url}?use_private_url=true"):
            assert mock_gen_openapi_client_dl_link.call_args.args[1] is True

    def test_gen_client_public(self, app_test_client, python_url, mock_gen_openapi_client_dl_link):
        """Verify that the 'SERVICE_PUBLIC_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{python_url}?use_private_url=false"):
            assert mock_gen_openapi_client_dl_link.call_args.args[1] is False


class TestNegativeOpenApiPython(object):
    """Negative test cases for getting clients from the 'openapi/python/' endpoint."""

    def test_gen_client_when_open_svc_unavailable(self, app_test_client, python_url):
        """
        Verify that the correct HTTP code is returned when attempting to get a client when the 'openapi' service is
        unavailable.
        """

        with app_test_client.get(python_url) as ret:
            assert ret.status_code == 500


class TestOpenApiGenClientCli(object):
    """Test cases for generating clients from the Flask command-line interface."""

    def test_gen_python_client(self, offline_flask_app, mock_gen_python_dl_link):
        """Verify that a user can generate a Python client."""

        with offline_flask_app.app_context():
            runner = CliRunner()
            result = runner.invoke(offline_flask_app.cli, ["genclient", "python"])

            assert result.exit_code == 0

            assert mock_gen_python_dl_link.call_count == 1
            assert mock_gen_python_dl_link.call_args.args[1] is False

    def test_gen_python_client_private(self, offline_flask_app, mock_gen_python_dl_link):
        """Verify that a user can generate a Python client using the SERVICE_PRIVATE_URL."""

        with offline_flask_app.app_context():
            runner = CliRunner()
            result = runner.invoke(offline_flask_app.cli, ["genclient", "--private", "python"])

            assert result.exit_code == 0

            assert mock_gen_python_dl_link.call_count == 1
            assert mock_gen_python_dl_link.call_args.args[1] is True

    def test_gen_typescript_client(self, offline_flask_app, mock_gen_typescript_dl_link):
        """Verify that a user can generate a TypeScript client."""

        with offline_flask_app.app_context():
            runner = CliRunner()
            result = runner.invoke(offline_flask_app.cli, ["genclient", "typescript"])

            assert result.exit_code == 0

            assert mock_gen_typescript_dl_link.call_count == 1
            assert mock_gen_typescript_dl_link.call_args.args[1] is False

    def test_gen_typescript_client_private(self, offline_flask_app, mock_gen_typescript_dl_link):
        """Verify that a user can generate a TypeScript client using the SERVICE_PRIVATE_URL."""

        with offline_flask_app.app_context():
            runner = CliRunner()
            result = runner.invoke(offline_flask_app.cli, ["genclient", "--private", "typescript"])

            assert result.exit_code == 0

            assert mock_gen_typescript_dl_link.call_count == 1
            assert mock_gen_typescript_dl_link.call_args.args[1] is True
