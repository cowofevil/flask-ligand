"""Tests for the 'openapi' API endpoint"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest
import flask_ligand
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from flask_ligand.controllers import get_openapi_client_dl_link

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
def mock_get_openapi_client_dl_link(mocker: MockerFixture) -> MagicMock:
    """Magic Mock of 'flask_ligand.controllers.get_openapi_client_dl_link'."""

    magic_mock = mocker.create_autospec(spec=get_openapi_client_dl_link)
    mocker.patch("flask_ligand.views.openapi.get_openapi_client_dl_link", side_effect=magic_mock)

    return magic_mock


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestOpenApiTypescriptAxios(object):
    """Test cases for getting clients from the 'openapi/typescript-axios/' endpoint."""

    def test_get_client_no_params(
        self, app_test_client, typescript_axios_url, open_api_client_name, mock_get_openapi_client_dl_link
    ):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when no URL parameters are provided."""

        with app_test_client.get(typescript_axios_url):
            assert mock_get_openapi_client_dl_link.call_args.args[1] is True

            assert mock_get_openapi_client_dl_link.call_args.args[2] == "typescript-axios"

            assert mock_get_openapi_client_dl_link.call_args.args[3] == {
                "npmName": open_api_client_name,
                "npmVersion": flask_ligand.__version__,
                "supportsES6": True,
                "useSingleRequestParameter": True,
            }

    def test_get_client_private(self, app_test_client, typescript_axios_url, mock_get_openapi_client_dl_link):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{typescript_axios_url}?use_private_url=true"):
            assert mock_get_openapi_client_dl_link.call_args.args[1] is True

    def test_get_client_public(self, app_test_client, typescript_axios_url, mock_get_openapi_client_dl_link):
        """Verify that the 'SERVICE_PUBLIC_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{typescript_axios_url}?use_private_url=false"):
            assert mock_get_openapi_client_dl_link.call_args.args[1] is False


class TestNegativeOpenApiTypescriptAxios(object):
    """Negative test cases for getting clients from the 'openapi/typescript-axios/' endpoint."""

    def test_get_client_when_open_svc_unavailable(self, app_test_client, typescript_axios_url):
        """
        Verify that the correct HTTP code is returned when attempting to get a client when the 'openapi' service is
        unavailable.
        """

        with app_test_client.get(typescript_axios_url) as ret:
            assert ret.status_code == 500


class TestOpenApiPython(object):
    """Test cases for getting clients from the 'openapi/python/' endpoint."""

    def test_get_client_no_params(
        self, app_test_client, python_url, open_api_client_name, mock_get_openapi_client_dl_link
    ):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when no URL parameters are provided."""

        with app_test_client.get(python_url):
            assert mock_get_openapi_client_dl_link.call_args.args[1] is True

            assert mock_get_openapi_client_dl_link.call_args.args[2] == "python"

            assert mock_get_openapi_client_dl_link.call_args.args[3] == {
                "packageName": open_api_client_name.replace("-", "_"),
                "projectName": open_api_client_name,
                "packageVersion": flask_ligand.__version__,
            }

    def test_get_client_private(self, app_test_client, python_url, mock_get_openapi_client_dl_link):
        """Verify that the 'SERVICE_PRIVATE_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{python_url}?use_private_url=true"):
            assert mock_get_openapi_client_dl_link.call_args.args[1] is True

    def test_get_client_public(self, app_test_client, python_url, mock_get_openapi_client_dl_link):
        """Verify that the 'SERVICE_PUBLIC_URL' is used by default when explicitly declared in the URL parameters."""

        with app_test_client.get(f"{python_url}?use_private_url=false"):
            assert mock_get_openapi_client_dl_link.call_args.args[1] is False


class TestNegativeOpenApiPython(object):
    """Negative test cases for for getting clients from the 'openapi/python/' endpoint."""

    def test_get_client_when_open_svc_unavailable(self, app_test_client, python_url):
        """
        Verify that the correct HTTP code is returned when attempting to get a client when the 'openapi' service is
        unavailable.
        """

        with app_test_client.get(python_url) as ret:
            assert ret.status_code == 500
