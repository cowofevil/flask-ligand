"""Tests for the extensions classes and functions."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import pytest
from flask import Flask
from typing import TYPE_CHECKING
from collections import OrderedDict
from flask_ligand.default_settings import TestingConfig as ConfigForTesting  # Renamed because of pytest warning

# noinspection PyProtectedMember
from flask_ligand.default_settings import (
    _DefaultConfig,
    ProdConfig,
    StagingConfig,
    FlaskLocalConfig,
    ENVIRONMENTS,
    flask_environment_configurator,
)


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from typing import Any
    from unittest.mock import MagicMock
    from pytest_mock import MockerFixture
    from pytest_flask_ligand import FlaskLigandTestHelpers


# ======================================================================================================================
# Globals
# ======================================================================================================================
MOCK_REQUIRED_ENV_VARS = OrderedDict(
    {
        "SERVICE_PUBLIC_URL": "http://service.public.url",
        "SERVICE_PRIVATE_URL": "http://service.private.url",
        "ALLOWED_ROLES": "user,admin",
        "OIDC_ISSUER_URL": "http://oidc.issuer.url",
        "OIDC_REALM": "oidc_realm",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "OPENAPI_GEN_SERVER_URL": "http://openapi.gen.server.url",
    }
)


# ======================================================================================================================
# Fixtures
# ======================================================================================================================
@pytest.fixture(scope="session")
def default_config_args() -> dict[str, Any]:
    """The default arguments to use when instantiating a config class."""

    return {"api_title": "TEST CONFIG", "api_version": "1.0.1", "openapi_client_name": "test-config-client"}


@pytest.fixture(scope="session")
def unconfigured_flask_app() -> Flask:
    """An unconfigured Flask app for testing settings."""

    return Flask("TEST_APP")


@pytest.fixture(scope="function")
def mocked_req_env_vars(mocker: MockerFixture) -> OrderedDict[str, Any]:
    """Mock the environment variables for required settings."""

    return mocker.patch.dict("os.environ", MOCK_REQUIRED_ENV_VARS)


# ======================================================================================================================
# Test Suites
# ======================================================================================================================
class TestDefaultConfig(object):
    """Test cases for the '_DefaultConfig' class."""

    def test_happy_path(self, default_config_args: dict[str, Any], mocked_req_env_vars: OrderedDict[str, Any]) -> None:
        """Verify that the correct default config settings are created for all inherited environments."""

        config_exp: dict[str, Any] = {
            "API_TITLE": default_config_args["api_title"],
            "API_VERSION": default_config_args["api_version"],
            "OPENAPI_CLIENT_NAME": default_config_args["openapi_client_name"],
            "SERVICE_PUBLIC_URL": mocked_req_env_vars["SERVICE_PUBLIC_URL"],
            "SERVICE_PRIVATE_URL": mocked_req_env_vars["SERVICE_PRIVATE_URL"],
            "ALLOWED_ROLES": mocked_req_env_vars["ALLOWED_ROLES"].split(","),
            "SQLALCHEMY_DATABASE_URI": mocked_req_env_vars["SQLALCHEMY_DATABASE_URI"],
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "DB_AUTO_UPGRADE": False,
            "DB_MIGRATION_DIR": "migrations",
            "JSON_SORT_KEYS": False,
            "OIDC_ISSUER_URL": mocked_req_env_vars["OIDC_ISSUER_URL"],
            "OIDC_REALM": mocked_req_env_vars["OIDC_REALM"],
            "VERIFY_SSL_CERT": True,
            "JWT_TOKEN_LOCATION": "headers",
            "JWT_HEADER_NAME": "Authorization",
            "JWT_HEADER_TYPE": "Bearer",
            "JWT_ERROR_MESSAGE_KEY": "message",
            "JWT_PUBLIC_KEY": "",
            "OPENAPI_GEN_SERVER_URL": mocked_req_env_vars["OPENAPI_GEN_SERVER_URL"],
            "OPENAPI_VERSION": "3.0.3",
            "OPENAPI_URL_PREFIX": "/",
            "OPENAPI_JSON_PATH": "/openapi/api-spec.json",
            "OPENAPI_SWAGGER_UI_PATH": "/apidocs",
            "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
            "API_SPEC_OPTIONS": {
                "servers": [{"url": mocked_req_env_vars["SERVICE_PUBLIC_URL"], "description": "Public URL"}]
            },
        }

        config_actual = _DefaultConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
        )

        # noinspection PyUnresolvedReferences
        assert config_actual == config_exp

    def test_override_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that an unprotected default setting can be overridden."""

        config_setting_override_exp: dict[str, Any] = {"OPENAPI_VERSION": "override_setting"}

        config_actual = _DefaultConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_setting_override_exp,
        )

        assert helpers.is_sub_dict(config_setting_override_exp, config_actual)

    def test_additional_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that additional settings can be specified."""

        config_additional_setting_exp: dict[str, Any] = {"A_NEW_SETTING": "a new setting value"}

        config_actual = _DefaultConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_additional_setting_exp,
        )

        assert helpers.is_sub_dict(config_additional_setting_exp, config_actual)


class TestNegativeDefaultConfig(object):
    """Negative test cases for the '_DefaultConfig' class."""

    @pytest.mark.parametrize(
        "mocked_env_var_index,mocked_env_vars",
        [
            (0, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 0}),
            (1, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 1}),
            (2, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 2}),
            (3, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 3}),
            (4, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 4}),
            (5, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 5}),
            (6, {items[0]: items[1] for i, items in enumerate(MOCK_REQUIRED_ENV_VARS.items()) if i != 6}),
        ],
    )
    def test_required_env_var_not_set(
        self,
        default_config_args: dict[str, Any],
        mocker: MockerFixture,
        mocked_env_var_index: int,
        mocked_env_vars: OrderedDict[str, Any],
    ):
        """Verify that unset required environment variable(s) have appropriate default values or 'None'."""

        mocker.patch.dict("os.environ", mocked_env_vars)

        with pytest.raises(RuntimeError) as e:
            _DefaultConfig(
                default_config_args["api_title"],
                default_config_args["api_version"],
                default_config_args["openapi_client_name"],
            )

        assert (
            str(e.value) == f"The '{list(MOCK_REQUIRED_ENV_VARS)[mocked_env_var_index]}' "
            f"environment variable must be set when running in this Flask environment!"
        )

    @pytest.mark.parametrize("protected_setting", ["API_TITLE", "API_VERSION", "OPENAPI_CLIENT_NAME"])
    def test_override_protected_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        protected_setting: str,
    ) -> None:
        """Verify that attempting to override a protected setting will raise the appropriate exception."""

        with pytest.raises(RuntimeError) as e:
            _DefaultConfig(
                default_config_args["api_title"],
                default_config_args["api_version"],
                default_config_args["openapi_client_name"],
                **{protected_setting: "not_allowed"},  # type: ignore
            )

        # noinspection PyUnresolvedReferences
        assert str(e.value) == f"The '{protected_setting}' setting is not allowed to be overridden!"

    def test_add_lowercase_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
    ):
        """Verify that attempting to add an all lowercase setting will raise the appropriate exception."""

        setting_name_exp: dict[str, Any] = {"lower_case_setting": "is_not_allowed"}

        with pytest.raises(RuntimeError) as e:
            _DefaultConfig(
                default_config_args["api_title"],
                default_config_args["api_version"],
                default_config_args["openapi_client_name"],
                **setting_name_exp,
            )

        # noinspection PyUnresolvedReferences
        assert str(e.value) == "The setting name 'lower_case_setting' must be uppercase!"


class TestProdConfig(object):
    """Test cases for the 'ProdConfig' class."""

    def test_happy_path(
        self,
        default_config_args: dict[str, Any],
        mocker: MockerFixture,
        helpers: FlaskLigandTestHelpers,
    ) -> None:
        """Verify that the correct config settings are created for the 'prod' environment."""

        mocked_env = {"JWT_DECODE_AUDIENCE": "account", **MOCK_REQUIRED_ENV_VARS}

        mocker.patch.dict("os.environ", mocked_env)

        config_exp: dict[str, Any] = {
            "JWT_ALGORITHM": "RS256",
            "JWT_DECODE_AUDIENCE": mocked_env["JWT_DECODE_AUDIENCE"],
        }

        config_actual = ProdConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
        )

        assert helpers.is_sub_dict(config_exp, config_actual)

    def test_override_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that an unprotected default setting can be overridden."""

        config_setting_override_exp: dict[str, Any] = {"JWT_ALGORITHM": "RS512"}

        config_actual = ProdConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_setting_override_exp,
        )

        assert helpers.is_sub_dict(config_setting_override_exp, config_actual)

    def test_additional_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that additional settings can be specified."""

        config_additional_setting_exp: dict[str, Any] = {"A_NEW_SETTING": "a new setting value"}

        config_actual = ProdConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_additional_setting_exp,
        )

        assert helpers.is_sub_dict(config_additional_setting_exp, config_actual)


class TestNegativeProdConfig(object):
    """Negative test cases for the 'ProdConfig' class."""

    def test_required_env_var_not_set(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
    ):
        """Verify that unset required environment variable(s) have no default value."""

        config_actual = ProdConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
        )

        assert config_actual["JWT_DECODE_AUDIENCE"] is None


class TestStagingConfig(object):
    """Test cases for the 'StagingConfig' class."""

    def test_happy_path(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that the correct config settings are created for the 'dev' environment."""

        config_exp: dict[str, Any] = {"VERIFY_SSL_CERT": False}

        config_actual = StagingConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
        )

        assert helpers.is_sub_dict(config_exp, config_actual)

    def test_override_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that an unprotected default setting can be overridden."""

        config_setting_override_exp: dict[str, Any] = {"VERIFY_SSL_CERT": True}

        config_actual = StagingConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_setting_override_exp,
        )

        assert helpers.is_sub_dict(config_setting_override_exp, config_actual)

    def test_additional_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that additional settings can be specified."""

        config_additional_setting_exp: dict[str, Any] = {"A_NEW_SETTING": "a new setting value"}

        config_actual = StagingConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_additional_setting_exp,
        )

        assert helpers.is_sub_dict(config_additional_setting_exp, config_actual)


class TestFlaskLocalConfig(object):
    """Test cases for the 'FlaskLocalConfig' class."""

    def test_happy_path(
        self,
        default_config_args: dict[str, Any],
        mocker: MockerFixture,
        helpers: FlaskLigandTestHelpers,
    ) -> None:
        """Verify that the correct config settings are created for the 'local' environment."""

        mocked_env = {
            "OIDC_ISSUER_URL": MOCK_REQUIRED_ENV_VARS["OIDC_ISSUER_URL"],
            "OIDC_REALM": MOCK_REQUIRED_ENV_VARS["OIDC_REALM"],
        }

        mocker.patch.dict("os.environ", mocked_env)

        # noinspection HttpUrlsUsage
        config_exp: dict[str, Any] = {
            "SERVICE_PUBLIC_URL": "http://localhost:5000",
            "SERVICE_PRIVATE_URL": "http://localhost:5000",
            "ALLOWED_ROLES": ["user", "admin"],
            "OIDC_ISSUER_URL": MOCK_REQUIRED_ENV_VARS["OIDC_ISSUER_URL"],
            "OIDC_REALM": MOCK_REQUIRED_ENV_VARS["OIDC_REALM"],
            "VERIFY_SSL_CERT": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "OPENAPI_GEN_SERVER_URL": "http://api.openapi-generator.tech",
            "API_SPEC_OPTIONS": {"servers": [{"url": "http://localhost:5000", "description": "Public URL"}]},
        }

        config_actual = FlaskLocalConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
        )

        assert helpers.is_sub_dict(config_exp, config_actual)

    def test_override_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that an unprotected default setting can be overridden."""

        config_setting_override_exp: dict[str, Any] = {"API_SPEC_OPTIONS": "something_different"}

        config_actual = FlaskLocalConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_setting_override_exp,
        )

        assert helpers.is_sub_dict(config_setting_override_exp, config_actual)

    def test_additional_setting(
        self,
        default_config_args: dict[str, Any],
        mocked_req_env_vars: OrderedDict[str, Any],
        helpers: FlaskLigandTestHelpers,
    ):
        """Verify that additional settings can be specified."""

        config_additional_setting_exp: dict[str, Any] = {"A_NEW_SETTING": "a new setting value"}

        config_actual = FlaskLocalConfig(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_additional_setting_exp,
        )

        assert helpers.is_sub_dict(config_additional_setting_exp, config_actual)


class TestTestingConfig(object):
    """Test cases for the 'TestingConfig' class."""

    def test_happy_path(self, default_config_args: dict[str, Any], helpers: FlaskLigandTestHelpers) -> None:
        """Verify that the correct config settings are created for the 'testing' environment."""

        config_exp: dict[str, Any] = {
            "SERVICE_PUBLIC_URL": "http://public.url",
            "SERVICE_PRIVATE_URL": "http://private.url",
            "ALLOWED_ROLES": ["user", "admin"],
            "OIDC_ISSUER_URL": "TESTING",
            "OIDC_REALM": "TESTING",
            "VERIFY_SSL_CERT": False,
            "JWT_ACCESS_TOKEN_EXPIRES": 300,
            "JWT_SECRET_KEY": "super-duper-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "OPENAPI_GEN_SERVER_URL": "http://openapi.fake.address",
            "API_SPEC_OPTIONS": {"servers": [{"url": "http://public.url", "description": "Public URL"}]},
        }

        config_actual = ConfigForTesting(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
        )

        assert helpers.is_sub_dict(config_exp, config_actual)

    def test_override_setting(self, default_config_args: dict[str, Any], helpers: FlaskLigandTestHelpers):
        """Verify that an unprotected default setting can be overridden."""

        config_setting_override_exp: dict[str, Any] = {"JWT_ACCESS_TOKEN_EXPIRES": 200}

        config_actual = ConfigForTesting(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_setting_override_exp,
        )

        assert helpers.is_sub_dict(config_setting_override_exp, config_actual)

    def test_additional_setting(self, default_config_args: dict[str, Any], helpers: FlaskLigandTestHelpers):
        """Verify that additional settings can be specified."""

        config_additional_setting_exp: dict[str, Any] = {"A_NEW_SETTING": "a new setting value"}

        config_actual = ConfigForTesting(
            default_config_args["api_title"],
            default_config_args["api_version"],
            default_config_args["openapi_client_name"],
            **config_additional_setting_exp,
        )

        assert helpers.is_sub_dict(config_additional_setting_exp, config_actual)


class TestFlaskEnvironmentConfigurator(object):
    """Test cases for the 'flask_environment_configurator' function."""

    def test_environment_count(self):
        """Verify that the expected number of environments exist. (No more, no less)"""

        assert len(ENVIRONMENTS) == 4

    @pytest.mark.parametrize(
        "env_name,env_config_class",
        [("prod", ProdConfig), ("dev", StagingConfig), ("local", FlaskLocalConfig), ("testing", ConfigForTesting)],
    )
    def test_configure_environment(
        self,
        default_config_args: dict[str, Any],
        unconfigured_flask_app: Flask,
        mocker: MockerFixture,
        env_name: str,
        env_config_class: ProdConfig | StagingConfig | FlaskLocalConfig | ConfigForTesting,
    ) -> None:
        """Verify the configurator builds the correct config settings for each defined environment."""

        mock_env_config: MagicMock = mocker.create_autospec(env_config_class)

        mocker.patch.dict("flask_ligand.default_settings.ENVIRONMENTS", {env_name: mock_env_config})

        flask_environment_configurator(unconfigured_flask_app, env_name, **default_config_args)

        mock_env_config.assert_called()


class TestNegativeFlaskEnvironmentConfigurator(object):
    """Negative test cases for the 'flask_environment_configurator' function."""

    def test_specify_invalid_environment_name(self, default_config_args: dict[str, Any], unconfigured_flask_app):
        """Verify that specifying an invalid environment name will raise the expected exception."""

        invalid_env_name = "bad!"

        with pytest.raises(RuntimeError) as e:
            flask_environment_configurator(unconfigured_flask_app, invalid_env_name, **default_config_args)

        # noinspection PyUnresolvedReferences
        assert str(e.value) == f"The specified '{invalid_env_name}' environment is invalid!"
