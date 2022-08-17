"""Default Flask application settings"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import os
import flask
from typing import TYPE_CHECKING


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from typing import Any


# ======================================================================================================================
# Classes: Private
# ======================================================================================================================
class _DefaultConfig(dict):  # type: ignore
    def __init__(self, api_title: str, api_version: str, openapi_client_name: str, **kwargs: dict[str, Any]):
        """The default Flask settings for all environments.

        Args:
            api_title: The title (name) of the API to display in the OpenAPI documentation.
            api_version: The semantic version for the OpenAPI client.
            openapi_client_name: The package name to use for generated OpenAPI clients.
            kwargs: Additional settings to add to the configuration.

        Raises:
            RuntimeError: Attempted to override a protected setting or specified an additional setting that was not all
                uppercase.
        """

        open_api_default_settings: dict[str, Any] = {
            "OPENAPI_GEN_SERVER_URL": os.getenv("OPENAPI_GEN_SERVER_URL"),
            "OPENAPI_VERSION": "3.0.3",
            "OPENAPI_URL_PREFIX": "/",
            "OPENAPI_JSON_PATH": "/openapi/api-spec.json",
            "OPENAPI_SWAGGER_UI_PATH": "/apidocs",
            "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        }

        # TODO: This needs to be changed to using an env_var for configuring PostgreSQL as the database. []
        basic_default_settings: dict[str, Any] = {
            "SERVICE_PUBLIC_URL": os.getenv("SERVICE_PUBLIC_URL"),
            "SERVICE_PRIVATE_URL": os.getenv("SERVICE_PRIVATE_URL"),
            "API_SPEC_OPTIONS": {"servers": [{"url": os.getenv("SERVICE_PUBLIC_URL"), "description": "Public URL"}]},
            "JSON_SORT_KEYS": False,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_DATABASE_URI": os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:"),
            "VERIFY_SSL_CERT": True,
        }

        auth_default_settings: dict[str, Any] = {
            "OIDC_REALM": os.getenv("OIDC_REALM"),
            "JWT_TOKEN_LOCATION": "headers",
            "JWT_HEADER_NAME": "Authorization",
            "JWT_HEADER_TYPE": "Bearer",
            "JWT_ERROR_MESSAGE_KEY": "message",
            "JWT_PUBLIC_KEY": "",
        }

        super().__init__(
            {
                "API_TITLE": api_title,
                "API_VERSION": api_version,
                "OPENAPI_CLIENT_NAME": openapi_client_name,
                **open_api_default_settings,
                **basic_default_settings,
                **auth_default_settings,
            }
        )

        for key in kwargs:
            if key.isupper():
                if key not in ["API_TITLE", "API_VERSION", "OPENAPI_CLIENT_NAME"]:
                    self[key] = kwargs[key]
                else:
                    raise RuntimeError(f"The '{key}' setting is not allowed to be overridden!")
            else:
                raise RuntimeError(f"The setting name '{key}' must be uppercase!")


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
class ProdConfig(_DefaultConfig):
    def __init__(self, api_title: str, api_version: str, openapi_client_name: str, **kwargs: dict[str, Any]):
        """Configuration for production environments.

        Args:
            api_title: The title (name) of the API to display in the OpenAPI documentation.
            api_version: The semantic version for the OpenAPI client.
            openapi_client_name: The package name to use for generated OpenAPI clients.
            kwargs: Additional settings to add to the configuration.

        Raises:
            RuntimeError: Attempted to override a protected setting or specified an additional setting that was not all
                uppercase.
        """

        prod_settings: dict[str, Any] = {
            "JWT_ALGORITHM": "RS256",
            "JWT_DECODE_AUDIENCE": "account",
            "JWT_IDENTITY_CLAIM": "email",
            "OIDC_ISSUER_URL": os.getenv("OIDC_ISSUER_URL"),
        }

        combined_settings = {**prod_settings, **kwargs}

        super().__init__(api_title, api_version, openapi_client_name, **combined_settings)


class DevConfig(ProdConfig):
    def __init__(self, api_title: str, api_version: str, openapi_client_name: str, **kwargs: dict[str, Any]):
        """Configuration for development/staging environments.

        Args:
            api_title: The title (name) of the API to display in the OpenAPI documentation.
            api_version: The semantic version for the OpenAPI client.
            openapi_client_name: The package name to use for generated OpenAPI clients.
            kwargs: Additional settings to add to the configuration.

        Raises:
            RuntimeError: Attempted to override a protected setting or specified an additional setting that was not all
                uppercase.
        """

        dev_settings: dict[str, Any] = {"VERIFY_SSL_CERT": False}

        combined_settings = {**dev_settings, **kwargs}

        super().__init__(f"DEV {api_title}", api_version, openapi_client_name, **combined_settings)


class FlaskLocalConfig(DevConfig):
    def __init__(self, api_title: str, api_version: str, openapi_client_name: str, **kwargs: dict[str, Any]):
        """Configuration used for running a local Flask server.

        Args:
            api_title: The title (name) of the API to display in the OpenAPI documentation.
            api_version: The semantic version for the OpenAPI client.
            openapi_client_name: The package name to use for generated OpenAPI clients.
            kwargs: Additional settings to add to the configuration.

        Raises:
            RuntimeError: Attempted to override a protected setting or specified an additional setting that was not all
                uppercase.
        """

        flask_local_settings: dict[str, Any] = {
            "OPENAPI_GEN_SERVER_URL": os.getenv("OPENAPI_GEN_SERVER_URL", "http://api.openapi-generator.tech"),
            "SERVICE_PUBLIC_URL": os.getenv("SERVICE_PUBLIC_URL", "http://localhost:5000"),
            "SERVICE_PRIVATE_URL": os.getenv("SERVICE_PRIVATE_URL", "http://localhost:5000"),
            "API_SPEC_OPTIONS": {
                "servers": [
                    {"url": os.getenv("SERVICE_PUBLIC_URL", "http://localhost:5000"), "description": "Public URL"}
                ]
            },
            "OIDC_ISSUER_URL": os.getenv("OIDC_ISSUER_URL"),
        }

        combined_settings = {**flask_local_settings, **kwargs}

        super().__init__(f"FLASK LOCAL {api_title}", api_version, openapi_client_name, **combined_settings)


class TestingConfig(_DefaultConfig):
    def __init__(self, api_title: str, api_version: str, openapi_client_name: str, **kwargs: dict[str, Any]):
        """Configuration used for unit testing.

        Args:
            api_title: The title (name) of the API to display in the OpenAPI documentation.
            api_version: The semantic version for the OpenAPI client.
            openapi_client_name: The package name to use for generated OpenAPI clients.
            kwargs: Additional settings to add to the configuration.

        Raises:
            RuntimeError: Attempted to override a protected setting or specified an additional setting that was not all
                uppercase.
        """

        testing_settings: dict[str, Any] = {
            "OPENAPI_GEN_SERVER_URL": "http://openapi.fake.address",
            "SERVICE_PUBLIC_URL": os.getenv("SERVICE_PUBLIC_URL", "http://public.url"),
            "SERVICE_PRIVATE_URL": os.getenv("SERVICE_PRIVATE_URL", "http://private.url"),
            "API_SPEC_OPTIONS": {
                "servers": [{"url": os.getenv("SERVICE_PUBLIC_URL", "http://public.url"), "description": "Public URL"}]
            },
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "VERIFY_SSL_CERT": False,
            "JWT_SECRET_KEY": "super-duper-secret",
            "JWT_ACCESS_TOKEN_EXPIRES": 300,
            "OIDC_ISSUER_URL": "TESTING",
        }

        combined_settings = {**testing_settings, **kwargs}

        super().__init__(f"TESTING {api_title}", api_version, openapi_client_name, **combined_settings)


# ======================================================================================================================
# Globals: Needs to be after class declarations to work right.
# ======================================================================================================================
ENVIRONMENTS = {
    "prod": ProdConfig,
    "dev": DevConfig,
    "local": FlaskLocalConfig,
    "testing": TestingConfig,
}


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def flask_environment_configurator(
    app: flask.Flask,
    environment: str,
    api_title: str,
    api_version: str,
    openapi_client_name: str,
    **kwargs: dict[str, Any],
) -> None:
    """Update a Flask app configuration for a given environment with optional setting overrides.

    Args:
        app: The root Flask app to configure with the given extension.
        environment: The target environment to create a Flask configuration object for. Available environments:
            'prod': Configured for use in a production environment.
            'dev': Configured for use in a development/staging environment.
            'local': Configured for use with a local Flask server.
            'testing': Configured for use in unit testing.
        api_title: The title (name) of the API to display in the OpenAPI documentation.
        api_version: The semantic version for the OpenAPI client.
        openapi_client_name: The package name to use for generated OpenAPI clients.
        kwargs: Additional settings to add to the configuration object.

    Raises:
        RuntimeError: Attempted to override a protected setting, specified an additional setting that was not all
            uppercase or the specified environment is invalid.
    """

    try:
        app.config.from_mapping(ENVIRONMENTS[environment](api_title, api_version, openapi_client_name, **kwargs))
    except KeyError:
        raise RuntimeError(f"The specified '{environment}' environment is invalid!")
