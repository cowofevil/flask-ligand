"""Tests for the built-in Flask sub-commands for OpenAPI related functionality."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestOpenApiGenClientCli(object):
    """Test cases for generating clients from the Flask command-line interface."""

    def test_gen_python_client(self, app_test_client):
        """Verify that a user can generate a Python client."""

        with app_test_client.application.app_context():
            runner = CliRunner()
            result = runner.invoke(app_test_client.application.cli, ["genclient", "python"])

            assert result.exit_code == 0
            assert result.output.startswith(
                f"{app_test_client.application.config['OPENAPI_GEN_SERVER_URL']}/api/gen/download"
            )

    def test_gen_typescript_client(self, app_test_client):
        """Verify that a user can generate a TypeScript client."""

        with app_test_client.application.app_context():
            runner = CliRunner()
            result = runner.invoke(app_test_client.application.cli, ["genclient", "typescript"])

            assert result.exit_code == 0
            assert result.output.startswith(
                f"{app_test_client.application.config['OPENAPI_GEN_SERVER_URL']}/api/gen/download"
            )
