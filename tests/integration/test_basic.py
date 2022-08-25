"""Tests for basic functionality."""


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestBasic(object):
    """Test cases for verifying the basic operations."""

    def test_rbac_protected_endpoint(self, primed_test_client, integration_test_url, access_token_headers):
        """Verify that an endpoint can be secured via RBAC."""

        with primed_test_client.get(integration_test_url, headers=access_token_headers) as ret:
            assert ret.status_code == 200
            assert len(ret.json) == 3


class TestNegativeBasic(object):
    """Negative test cases for verifying the basic operations."""

    # noinspection PyTestParametrized
    def test_unauthorized_role(self, primed_test_client, integration_test_url, access_token_headers_no_roles):
        """
        Verify that the correct HTTP code is returned when attempting to access a protected endpoint using a JWT
        access token that doesn't have the appropriate role specified to access the endpoint.
        """

        with primed_test_client.get(integration_test_url, headers=access_token_headers_no_roles) as ret:
            assert ret.status_code == 403
            assert ret.json["message"] == "This endpoint requires the user to have the 'user' role!"
