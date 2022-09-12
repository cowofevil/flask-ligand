"""Tests for the "extensions.api" classes and functions."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest
from http import HTTPStatus
from flask_ligand.extensions.api import abort

# noinspection PyPackageRequirements
from werkzeug.exceptions import HTTPException


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestAbort(object):
    """Test cases the 'abort' extension function."""

    def test_abort_with_default_message(self, app_test_client):
        """Verify that abort will return the correct default message when none is specified."""

        with app_test_client.application.app_context():
            with pytest.raises(HTTPException) as e:
                abort(HTTPStatus(404))

        # noinspection PyUnresolvedReferences
        assert e.value.response.json["message"] == HTTPStatus(404).phrase  # type: ignore

    def test_abort_with_custom_message(self, app_test_client):
        """Verify that abort will return a user specified message."""

        message_exp = "A custom message!"

        with app_test_client.application.app_context():
            with pytest.raises(HTTPException) as e:
                abort(HTTPStatus(404), message=message_exp)

        # noinspection PyUnresolvedReferences
        assert e.value.response.json["message"] == message_exp  # type: ignore


class TestNegativeAbort(object):
    """Negative test cases the 'abort' extension function."""

    def test_abort_with_invalid_status_code(self, app_test_client):
        """Verify that the correct exception is raised when an invalid HTTP status code is specified."""

        invalid_http_status_code = 42

        with app_test_client.application.app_context():
            with pytest.raises(ValueError):
                abort(HTTPStatus(invalid_http_status_code))

    def test_abort_with_invalid_status_code_and_custom_message(self, app_test_client):
        """Verify that the correct exception is raised when an invalid HTTP status code is specified along with a
        custom message.
        """

        invalid_http_status_code = 42

        with app_test_client.application.app_context():
            with pytest.raises(ValueError):
                abort(HTTPStatus(invalid_http_status_code), message="Oh no!")
