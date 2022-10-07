Built-in Flask Environments
===========================

The ``flask-ligand`` library has several pre-configured environments that can be used for production, staging, local
development and testing. This document covers each environment and the settings available in each that can be
overridden by environment variables.

Selecting which environment to use requires setting the environment variable ``FLASK_ENV`` to one of the environments
listed below. Each environment has certain settings pre-configured with some of those settings allowed to be
overridden via environment variables. The sections below will detail the default settings applied to the underlying
libraries used to setup microservices as well as whether they can be overridden.

If a setting does need to be changed to fit the needs of your project consuming this library then it can be done via
code by passing the overrides to the ``create_app`` as kwargs. The only restriction is that the ``API_TITLE``,
``API_VERSION`` and ``OPENAPI_CLIENT_NAME`` client settings cannot be overridden via the kwargs.

(**Note**: this project does support the use of '.env' files for loading environment variables)

prod
----

The 'prod' environment is meant to run the microservice in a production environment.

.. list-table:: **Environment Settings**
   :widths: 25 15 10 50
   :header-rows: 1

   * - Setting
     - Default
     - ENV Override?
     - Description
   * - ``SERVICE_PUBLIC_URL``
     - *Not set* (must be provided)
     - *Yes*
     - The public URL for this service. (Also used for generating OpenAPI clients)
   * - ``SERVICE_PRIVATE_URL``
     - *Not set* (must be provided)
     - *Yes*
     - The private URL for this service. (Also used for generating OpenAPI clients)
   * - ``ALLOWED_ROLES``
     - *Not set* (must be provided)
     - *Yes*
     - A comma separated list of user roles that are allowed for endpoint protection. (e.g. 'user,admin')
   * - ``OIDC_DISCOVERY_URL``
     - *Not set* (must be provided)
     - *Yes*
     - The `OpenID Connect Provider Configuration Request`_ URL.
   * - ``VERIFY_SSL_CERT``
     - ``True``
     - *No*
     - Verify the SSL/TLS certificate of the ``OIDC_DISCOVERY_URL``.
   * - ``JWT_ALGORITHM``
     - ``RS256``
     - *No*
     - Which algorithm to sign the JWT with. See PyJWT for the available algorithms. (See `flask-jwt-extended`_ for
       more information)
   * - ``JWT_DECODE_AUDIENCE``
     - ``None``
     - *Yes*
     - The string or list of audiences (aud) expected in a JWT when decoding it. Setting this will add an extra layer
       of security for guaranteeing that the OIDC IAM issuing the token supports the correct claims or is issuing tokens
       for the correct URL for a multi-microservice web app. (See `flask-jwt-extended`_ for more information)
   * - ``JWT_TOKEN_LOCATION``
     - ``headers``
     - *No*
     - Where to look for a JWT when processing a request. The available options are "headers", "cookies", "query_string"
       , and "json". (See `flask-jwt-extended`_ for more information)
   * - ``JWT_HEADER_NAME``
     - ``Authorization``
     - *No*
     - What header should contain the JWT in a request. (See `flask-jwt-extended`_ for more information)
   * - ``JWT_HEADER_TYPE``
     - ``Bearer``
     - *No*
     - What type of header the JWT is in. If this is an empty string, the header should contain nothing besides the
       JWT. (See `flask-jwt-extended`_ for more information)
   * - ``JWT_ERROR_MESSAGE_KEY``
     - ``message``
     - *No*
     - The key for error messages in a JSON response returned by this extension. (See `flask-jwt-extended`_ for more
       information)
   * - ``JWT_PUBLIC_KEY``
     - *Empty string*
     - *No*
     - The secret key used to decode JWTs when using an asymmetric signing algorithm (such as RS* or ES*). This setting
       should remain empty to allow ``flask-ligand`` to automatically set the public key from the ``OIDC_DISCOVERY_URL``
       upon microservice startup. Muck with it at your own peril! (See `flask-jwt-extended`_ for more information)
   * - ``SQLALCHEMY_DATABASE_URI``
     - *Not set* (must be provided)
     - *Yes*
     - The URI for a PostgreSQL database to use for persistent storage. (See `database_configuration.rst`_ for more
       information)
   * - ``SQLALCHEMY_TRACK_MODIFICATIONS``
     - ``False``
     - *No*
     - If set to ``True``, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None,
       which enables tracking but issues a warning that it will be disabled by default in the future. This requires
       extra memory and should be disabled if not needed. (See :doc:`Flask-SQLAlchemy <flask-sqlalchemy:config>` for
       more information)
   * - ``DB_AUTO_UPGRADE``
     - ``False``
     - *No*
     - If set to ``True``, the microservice will automatically run ``flask db upgrade`` upon start-up which will
       create/alter all tables in the the configured database. **USE WITH CAUTION!!** Only suggested to use in testing
       or experimentation with the given microservice. (See `Flask-Migrate`_ for more information)
   * - ``DB_MIGRATION_DIR``
     - ``migrations``
     - *No*
     - The directory containing the migration scripts for performing database upgrades and downgrades. (See
       `Flask-Migrate`_ for more information)
   * - ``JSON_SORT_KEYS``
     - ``False``
     - *No*
     - Sort the keys of JSON objects alphabetically. This is useful for caching because it ensures the data is
       serialized the same way no matter what Python’s hash seed is. While not recommended, you can disable this for a
       possible performance improvement at the cost of caching. (See `flask`_ for more information)
   * - ``OPENAPI_GEN_SERVER_URL``
     - *Not set* (must be provided)
     - *Yes*
     - The OpenAPI online generator server URL to use for creating clients. (See `smorest/OpenAPI`_ for more
       information)
   * - ``OPENAPI_VERSION``
     - ``3.0.3``
     - *Yes*
     - Version of the OpenAPI standard used to describe the API. It should be provided as a string. (See
       `smorest/OpenAPI`_ documentation for more details.)
   * - ``OPENAPI_URL_PREFIX``
     - ``/``
     - *No*
     - Defines the base path for both the JSON file and the UI. If None, the documentation is not served and the
       following parameters are ignored. (See `smorest/OpenAPI`_ documentation for more details.)
   * - ``OPENAPI_JSON_PATH``
     - ``/openapi/api-spec.json``
     - *No*
     - Path to the JSON file, relative to the base path. (See `smorest/OpenAPI`_ for more information)
   * - ``OPENAPI_SWAGGER_UI_PATH``
     - ``/apidocs``
     - *Yes*
     - Path to the Swagger UI page, relative to the base path. (See `smorest/OpenAPI`_ for more information)
   * - ``OPENAPI_SWAGGER_UI_URL``
     - ``https://cdn.jsdelivr.net/npm/swagger-ui-dist/``
     - *No*
     - URL to the Swagger UI script. Versions prior to 3.x are not supported. (See `smorest/apispec`_ for more
       information)
   * - ``API_SPEC_OPTIONS``
     - ``{"servers": [{"url": os.getenv("SERVICE_PUBLIC_URL"), "description": "Public URL"}]}``
     - *No*
     - Additional root document attributes. (See `smorest/apispec`_ for more information)

stage
-----

The 'stage' environment is meant to run the microservice in a staging/development environment. The table below contains
only the settings that are different from the ``prod`` environment settings.

.. list-table:: **Environment Settings**
   :widths: 25 35 10 50
   :header-rows: 1

   * - Setting
     - Default
     - ENV Override?
     - Description
   * - ``VERIFY_SSL_CERT``
     - ``False``
     - *No*
     - Verify the SSL/TLS certificate of the ``OIDC_DISCOVERY_URL``.

local
-----

The 'local' environment is meant to start the microservice in a local development/testing/experiment environment. The
table below contains only the settings that are different from the ``prod`` environment settings.

.. list-table:: **Environment Settings**
   :widths: 25 35 10 50
   :header-rows: 1

   * - Setting
     - Default
     - ENV Override?
     - Description
   * - ``SERVICE_PUBLIC_URL``
     - ``http://localhost:5000``
     - *Yes*
     - The public URL for this service. (Also used for generating OpenAPI clients)
   * - ``SERVICE_PRIVATE_URL``
     - ``http://localhost:5000``
     - *Yes*
     - The private URL for this service. (Also used for generating OpenAPI clients)
   * - ``ALLOWED_ROLES``
     - ``user,admin``
     - *Yes*
     - A comma separated list of user roles that are allowed for endpoint protection. (e.g. 'user,admin')
   * - ``VERIFY_SSL_CERT``
     - ``False``
     - *No*
     - Verify the SSL/TLS certificate of the ``OIDC_DISCOVERY_URL``.
   * - ``SQLALCHEMY_DATABASE_URI``
     - ``sqlite:///:memory:``
     - *Yes*
     - The URI for a PostgreSQL database to use for persistent storage. (See `database_configuration.rst`_ for more
       information)
   * - ``OPENAPI_GEN_SERVER_URL``
     - ``http://api.openapi-generator.tech``
     - *Yes*
     - The OpenAPI online generator server URL to use for creating clients. (See `smorest/OpenAPI`_ for more
       information)
   * - ``API_SPEC_OPTIONS``
     - ``{"servers": [{"url": os.getenv("SERVICE_PUBLIC_URL", "http://localhost:5000"), "description": "Public URL"}]}``
     - *No*
     - Additional root document attributes. (See `smorest/apispec`_ for more information)

testing
-------

The 'testing' environment is meant to be used for unit testing only. The table below contains only the settings that
are different from the ``prod`` environment settings.

.. list-table:: **Environment Settings**
   :widths: 25 35 10 50
   :header-rows: 1

   * - Setting
     - Default
     - ENV Override?
     - Description
   * - ``SERVICE_PUBLIC_URL``
     - ``http://public.url``
     - *Yes*
     - The public URL for this service. (Also used for generating OpenAPI clients)
   * - ``SERVICE_PRIVATE_URL``
     - ``http://private.url``
     - *Yes*
     - The private URL for this service. (Also used for generating OpenAPI clients)
   * - ``OIDC_DISCOVERY_URL``
     - *Not set* (must be provided)
     - *Yes*
     - The `OpenID Connect Provider Configuration Request`_ URL.
   * - ``VERIFY_SSL_CERT``
     - ``False``
     - *No*
     - Verify the SSL/TLS certificate of the ``OIDC_DISCOVERY_URL``.
   * - ``JWT_ACCESS_TOKEN_EXPIRES``
     - ``300``
     - *No*
     - How long an access token should be valid before it expires. This can be a datetime.timedelta,
       dateutil.relativedelta, or a number of seconds (Integer). (See `flask-jwt-extended`_ for more information)
   * - ``JWT_SECRET_KEY``
     - ``super-duper-secret``
     - *No*
     - The secret key used to encode and decode JWTs when using a symmetric signing algorithm (such as HS*). It should
       be a long random string of bytes, although unicode is accepted too. For example, copy the output of this to your
       config. (See `flask-jwt-extended`_ for more information)
   * - ``SQLALCHEMY_DATABASE_URI``
     - ``sqlite:///:memory:``
     - *Yes*
     - The URI for a PostgreSQL database to use for persistent storage. (See `database_configuration.rst`_ for more
       information)
   * - ``OPENAPI_GEN_SERVER_URL``
     - ``http://openapi.fake.address``
     - *Yes*
     - The OpenAPI online generator server URL to use for creating clients. (See `smorest/OpenAPI`_ for more
       information)
   * - ``API_SPEC_OPTIONS``
     - ``{"servers": [{"url": os.getenv("SERVICE_PUBLIC_URL", "http://public.url"), "description": "Public URL"}]}``
     - *No*
     - Additional root document attributes. (See `smorest/apispec`_ for more information)

.. _database_configuration.rst: docs/database_configuration.rst
.. _smorest/OpenAPI: https://flask-smorest.readthedocs.io/en/latest/openapi.html#serve-the-openapi-documentation
.. _smorest/apispec: https://flask-smorest.readthedocs.io/en/latest/openapi.html?highlight=API_SPEC_OPTIONS#populate-the-root-document-object
.. _flask: https://flask.palletsprojects.com/en/2.2.x/config/
.. _flask-jwt-extended: https://flask-jwt-extended.readthedocs.io/en/stable/options/
.. _Flask-Migrate: https://flask-migrate.readthedocs.io/en/latest/index.html#command-reference
.. _`OpenID Connect Provider Configuration Request`: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfigurationRequest
