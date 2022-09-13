"""flask-ligand microservice library package."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from flask import Flask
from flask_cors import CORS
from typing import TYPE_CHECKING
from flask_ligand import extensions, views
from flask_ligand.default_settings import flask_environment_configurator


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


# ======================================================================================================================
# Globals
# ======================================================================================================================
__version__ = "0.3.4"


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def create_app(flask_env: str, api_title: str, api_version: str, openapi_client_name: str, **kwargs: Any) -> Flask:
    """Create Flask application.

    Args:
        flask_env: Specify the environment to use when launching the flask app. Available environments:
            'prod': Configured for use in a production environment.
            'stage': Configured for use in a development/staging environment.
            'local': Configured for use with a local Flask server.
            'testing': Configured for use in unit testing.
        api_title: The title (name) of the API to display in the OpenAPI documentation.
        api_version: The semantic version for the OpenAPI client.
        openapi_client_name: The package name to use for generated OpenAPI clients.
        kwargs: Additional settings to add to the configuration object or overrides for unprotected settings.

    Returns:
        Fully configured Flask application.

    Raises:
        RuntimeError: Attempted to override a protected setting, specified an additional setting that was not all
            uppercase or the specified environment is invalid.
    """

    app = Flask(__name__)
    CORS(app, expose_headers=["x-pagination", "etag"])  # TODO: this needs to be configurable! [271]

    flask_environment_configurator(app, flask_env, api_title, api_version, openapi_client_name, **kwargs)

    api = extensions.create_api(app)
    views.register_blueprints(api)

    return app
