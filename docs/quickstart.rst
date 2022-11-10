.. rstcheck: ignore-roles=sqlalchemy,swagger-ui,auth0
.. rstcheck: ignore-directives=code-include,collapse

==========
Quickstart
==========

.. important:: There is a companion `example project`_ that you should clone beforehand to get the most out of this
    guide. All example code in this guide is copied straight from the `example project`_.

``flask-ligand`` combines together several excellent libraries to create a framework for developing Flask microservices,
so it is strongly recommended that a user familiarize themselves with the following documentation after going through
this guide:

- :doc:`flask-smorest Quickstart <flask-smorest:quickstart>`
- :doc:`flask-sqlalchemy Quickstart <flask-sqlalchemy:quickstart>`
- :doc:`marshmallow-sqlalchemy Recipes <marshmallow-sqlalchemy:recipes>`
- :doc:`flask-jwt-extended Basic Usage <flask-jwt-extended:basic_usage>`
- :doc:`flask-migrate Example <flask-migrate:index>`
- :doc:`marshmallow-sqlalchemy <marshmallow-sqlalchemy:index>`
    - :sqlalchemy:`SQLAlchemy Getting Started <index.html>`
- :doc:`sqlalchemy-utils Data types <sqlalchemy-utils:data_types>`

Simple Example
==============

Here is a basic “Petstore example” which is based on the :doc:`flask-smorest Quickstart example
<flask-smorest:quickstart>`. (Which is a core library that ``flask-ligand`` is built upon)

Database Model
--------------

The :data:`DB.Model <flask_ligand.extensions.database.DB>` below will store our ``PetModel`` in the configured
database and also act as the basis for a schema for defining the acceptable inputs and outputs of endpoints
(a.k.a. :class:`Flask View <flask.views.MethodView>`) initiated later. The ``PetModel`` below demonstrates how to
utilize :doc:`sqlalchemy-utils <sqlalchemy-utils:data_types>` to implement much stricter data typing than what is
available out-of-the-box for :sqlalchemy:`SQLAlchemy <index.html>`.

.. code-block:: python

    class PetModel(DB.Model):  # type: ignore
        """Pet model class."""

        __tablename__ = "pet"

        id = DB.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
        name = DB.Column(DB.String(length=NAME_MAX_LENGTH), nullable=False)
        description = DB.Column(DB.Text(), nullable=False)
        created_at = DB.Column(DB.DateTime, default=DB.func.current_timestamp(), nullable=False)
        updated_at = DB.Column(
            DB.DateTime, default=DB.func.current_timestamp(), onupdate=DB.func.current_timestamp(), nullable=False
        )
.. collapse:: Click for full example...

    .. code-block:: python

        """Models"""

        # ======================================================================================================================
        # Imports
        # ======================================================================================================================
        import uuid
        from flask_ligand.extensions.database import DB
        from sqlalchemy_utils.types.uuid import UUIDType


        # ======================================================================================================================
        # Globals
        # ======================================================================================================================
        NAME_MAX_LENGTH: int = 255


        # ======================================================================================================================
        # Classes: Public
        # ======================================================================================================================
        class PetModel(DB.Model):  # type: ignore
            """Pet model class."""

            __tablename__ = "pet"

            id = DB.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
            name = DB.Column(DB.String(length=NAME_MAX_LENGTH), nullable=False)
            description = DB.Column(DB.Text(), nullable=False)
            created_at = DB.Column(DB.DateTime, default=DB.func.current_timestamp(), nullable=False)
            updated_at = DB.Column(
                DB.DateTime, default=DB.func.current_timestamp(), onupdate=DB.func.current_timestamp(), nullable=False
            )


Schemas
-------

Define an :class:`AutoSchema <flask_ligand.extensions.api.AutoSchema>` to expose the model.

.. code-block:: python

    class PetSchema(AutoSchema):
        """Automatically generate schema from the 'Pet' model."""

        class Meta(AutoSchema.Meta):
            model = PetModel

        id = auto_field(dump_only=True)
        name = auto_field(required=True, validate=NAME_VALIDATOR)
        description = auto_field(required=False, validate=DESCRIPTION_VALIDATOR, load_default="")
        created_at = auto_field(dump_only=True)
        updated_at = auto_field(dump_only=True)

Define a :class:`Schema <flask_ligand.extensions.api.Schema>` to validate the query arguments for a subset of fields
defined in the above :class:`AutoSchema <flask_ligand.extensions.api.AutoSchema>` for a
:class:`Flask View <flask.views.MethodView>` that will be created later.

.. code-block:: python

    class PetQueryArgsSchema(Schema):
        """A schema for filtering Pets."""

        name = field_for(PetModel, "name", required=False, validate=NAME_VALIDATOR)
        description = field_for(PetModel, "description", required=False, validate=DESCRIPTION_VALIDATOR)

.. collapse:: Click for full example...

    .. code-block:: python

        """Schemas for models and view queries."""

        # ======================================================================================================================
        # Imports
        # ======================================================================================================================
        from marshmallow.validate import Length
        from marshmallow_sqlalchemy import auto_field, field_for
        from flask_ligand.extensions.api import AutoSchema, Schema
        from flask_ligand_example.models import PetModel, NAME_MAX_LENGTH


        # ======================================================================================================================
        # Globals
        # ======================================================================================================================
        NAME_VALIDATOR: Length = Length(min=1, max=NAME_MAX_LENGTH)
        DESCRIPTION_VALIDATOR: Length = Length(max=4096)


        # ======================================================================================================================
        # Classes: Public
        # ======================================================================================================================
        class PetSchema(AutoSchema):
            """Automatically generate schema from the 'Pet' model."""

            class Meta(AutoSchema.Meta):
                model = PetModel

            id = auto_field(dump_only=True)
            name = auto_field(required=True, validate=NAME_VALIDATOR)
            description = auto_field(required=False, validate=DESCRIPTION_VALIDATOR, load_default="")
            created_at = auto_field(dump_only=True)
            updated_at = auto_field(dump_only=True)


        class PetQueryArgsSchema(Schema):
            """A schema for filtering Pets."""

            name = field_for(PetModel, "name", required=False, validate=NAME_VALIDATOR)
            description = field_for(PetModel, "description", required=False, validate=DESCRIPTION_VALIDATOR)

Endpoints
---------

Instantiate a :class:`Blueprint <flask_ligand.extensions.api.Blueprint>`.

.. code-block:: python

    BLP = Blueprint(
        "Pets",
        __name__,
        url_prefix="/pets",
        description="Information about all the pets you love!",
    )

Use :class:`MethodView <flask.views.MethodView>` classes to organize resources, and decorate view methods with
:meth:`Blueprint.arguments <flask_smorest.Blueprint.arguments>` and
:meth:`Blueprint.response <flask_smorest.Blueprint.response>` to specify request/response (de)serialization and data
validation.

Selectively secure endpoint REST verbs to require a valid
:auth0:`JWT access token <blog/id-token-access-token-what-is-the-difference/>` containing certain roles by using the
:func:`jwt_role_required decorator <flask_ligand.extensions.jwt.jwt_role_required>`. Provide a convenient "Authorize"
button in the :swagger-ui:`SwaggerUI documentation <>` by providing the  to the
:meth:`Blueprint.arguments <Blueprint.arguments>`

.. code-block:: python

    @BLP.route("/")
    @BLP.etag
    class Pets(MethodView):
        @BLP.arguments(PetQueryArgsSchema, location="query")
        @BLP.response(200, PetSchema(many=True))
        @BLP.paginate(SQLCursorPage)  # noqa
        def get(self, args: dict[str, Any]) -> list[PetModel]:
            """Get all pets or filter for a subset of pets."""

            items: list[PetModel] = PetModel.query.filter_by(**args)

            return items

        @BLP.arguments(PetSchema)
        @BLP.response(201, PetSchema)
        @BLP.doc(security=BEARER_AUTH)
        @jwt_role_required(role="user")
        def post(self, new_item: dict[str, Any]) -> PetModel:
            """Add a new pet."""

            _we_love_pets(new_item["description"])

            item = PetModel(**new_item)
            DB.session.add(item)
            DB.session.commit()

            return item

Use :func:`abort <flask_ligand.extensions.api.abort>` to return an error response.

.. code-block:: python

    def _we_love_pets(description: str) -> None:
        """
        Verify that the description doesn't include pet hate.

        Args:
            description: The pet description to validate.

        Raises:
            werkzeug.exceptions.HTTPException
        """

        if "hate" in description:
            abort(HTTPStatus(400), "No pet hatred allowed!")

.. collapse:: Click for full example...

    .. code-block:: python

        """Pet endpoints."""

        # ======================================================================================================================
        # Imports
        # ======================================================================================================================
        from __future__ import annotations
        from http import HTTPStatus
        from typing import TYPE_CHECKING
        from flask.views import MethodView
        from flask_ligand_example.models import PetModel
        from flask_ligand.extensions.database import DB
        from flask_ligand.views.common.openapi_doc import BEARER_AUTH
        from flask_ligand.extensions.jwt import jwt_role_required, abort
        from flask_ligand.extensions.api import Blueprint, SQLCursorPage
        from flask_ligand_example.schemas import PetSchema, PetQueryArgsSchema


        # ======================================================================================================================
        # Type Checking
        # ======================================================================================================================
        if TYPE_CHECKING:  # pragma: no cover
            from uuid import UUID
            from typing import Any


        # ======================================================================================================================
        # Globals
        # ======================================================================================================================
        INVALID_PET_ID = "The specified pet ID does not exist or has an invalid format!"
        BLP = Blueprint(
            "Pets",
            __name__,
            url_prefix="/pets",
            description="Information about all the pets you love!",
        )


        # ======================================================================================================================
        # Functions: Private
        # ======================================================================================================================
        def _we_love_pets(description: str) -> None:
            """
            Verify that the description doesn't include pet hate.

            Args:
                description: The pet description to validate.

            Raises:
                werkzeug.exceptions.HTTPException
            """

            if "hate" in description:
                abort(HTTPStatus(400), "No pet hatred allowed!")


        # ======================================================================================================================
        # Classes: Public
        # ======================================================================================================================
        @BLP.route("/")
        @BLP.etag
        class Pets(MethodView):
            @BLP.arguments(PetQueryArgsSchema, location="query")
            @BLP.response(200, PetSchema(many=True))
            @BLP.paginate(SQLCursorPage)  # noqa
            def get(self, args: dict[str, Any]) -> list[PetModel]:
                """Get all pets or filter for a subset of pets."""

                items: list[PetModel] = PetModel.query.filter_by(**args)

                return items

            @BLP.arguments(PetSchema)
            @BLP.response(201, PetSchema)
            @BLP.doc(security=BEARER_AUTH)
            @jwt_role_required(role="user")
            def post(self, new_item: dict[str, Any]) -> PetModel:
                """Add a new pet."""

                _we_love_pets(new_item["description"])

                item = PetModel(**new_item)
                DB.session.add(item)
                DB.session.commit()

                return item


        @BLP.route("/<uuid:item_id>")
        @BLP.etag
        class PetsById(MethodView):
            @BLP.response(200, PetSchema)
            def get(self, item_id: UUID) -> PetModel:
                """Get a pet by ID."""

                item: PetModel = PetModel.query.get_or_404(item_id, description=INVALID_PET_ID)

                return item

            @BLP.arguments(PetSchema)
            @BLP.response(200, PetSchema)
            @BLP.doc(security=BEARER_AUTH)
            @jwt_role_required(role="user")
            def put(self, new_item: dict[str, Any], item_id: UUID) -> PetModel:
                """Update an existing pet."""

                item: PetModel = PetModel.query.get_or_404(item_id, description=INVALID_PET_ID)

                _we_love_pets(new_item["description"])

                BLP.check_etag(item, PetSchema)
                PetSchema().update(item, new_item)
                DB.session.add(item)
                DB.session.commit()

                return item

            @BLP.response(204)
            @BLP.doc(security=BEARER_AUTH)
            @jwt_role_required(role="admin")
            def delete(self, item_id: UUID) -> None:
                """Delete a pet."""

                item: PetModel = PetModel.query.get_or_404(item_id, description=INVALID_PET_ID)

                BLP.check_etag(item, PetSchema)
                DB.session.delete(item)
                DB.session.commit()

Create the App
--------------

Connect the models, schemas and views together by calling :func:`create_app <flask_ligand.create_app>` followed by
registering the Blueprints for the views.

.. code-block:: python

    def create_app(
        flask_app_name: str,
        flask_env: str,
        api_title: str,
        api_version: str,
        openapi_client_name: str,
        **kwargs: Any,
    ) -> Tuple[Flask, Api]:
        """
        Create Flask application.

        Args:
            flask_app_name: This name is used to find resources on the filesystem, can be used by extensions to improve
                debugging information and a lot more. So it's important what you provide one. If you are using a
                single module, ``__name__`` is always the correct value. If you however are using a package, it's usually
                recommended to hardcode the name of your package.
            flask_env: Specify the environment to use when launching the flask app. Available environments:

                ``prod``: Configured for use in a production environment.

                ``stage``: Configured for use in a development/staging environment.

                ``local``: Configured for use with a local Flask server.

                ``testing``: Configured for use in unit testing.

                ``cli``: Configured for use in a production environment without initializing extensions. (Use for CI/CD)
            api_title: The title (name) of the API to display in the OpenAPI documentation.
            api_version: The semantic version for the OpenAPI client.
            openapi_client_name: The package name to use for generated OpenAPI clients.
            kwargs: Additional settings to add to the configuration object or overrides for unprotected settings.

        Returns:
            A tuple with a fully configured Flask application and an Api ready to register additional Blueprints.

        Raises:
            RuntimeError: Attempted to override a protected setting, specified an additional setting that was not all
                uppercase or the specified environment is invalid.
        """

        app = Flask(flask_app_name)

        CORS(app, expose_headers=["x-pagination", "etag"])  # TODO: this needs to be configurable! [271]

        flask_environment_configurator(app, flask_env, api_title, api_version, openapi_client_name, **kwargs)

        api = extensions.create_api(app, True if flask_env == "cli" else False)

        views.register_blueprints(api)

        app.cli.add_command(genclient)

        return app, api

.. collapse:: Click for full example...

    .. code-block:: python

        """flask-ligand microservice library package."""

        # ======================================================================================================================
        # Imports
        # ======================================================================================================================
        from __future__ import annotations
        from flask import Flask
        from flask_cors import CORS
        from typing import TYPE_CHECKING
        from flask_ligand.cli import genclient
        from flask_ligand import extensions, views
        from flask_ligand.default_settings import flask_environment_configurator


        # ======================================================================================================================
        # Type Checking
        # ======================================================================================================================
        if TYPE_CHECKING:  # pragma: no cover
            from typing import Any, Tuple
            from flask_ligand.extensions.api import Api


        # ======================================================================================================================
        # Globals
        # ======================================================================================================================
        __version__ = "0.6.3"


        # ======================================================================================================================
        # Functions: Public
        # ======================================================================================================================
        def create_app(
            flask_app_name: str,
            flask_env: str,
            api_title: str,
            api_version: str,
            openapi_client_name: str,
            **kwargs: Any,
        ) -> Tuple[Flask, Api]:
            """
            Create Flask application.

            Args:
                flask_app_name: This name is used to find resources on the filesystem, can be used by extensions to improve
                    debugging information and a lot more. So it's important what you provide one. If you are using a
                    single module, ``__name__`` is always the correct value. If you however are using a package, it's usually
                    recommended to hardcode the name of your package.
                flask_env: Specify the environment to use when launching the flask app. Available environments:

                    ``prod``: Configured for use in a production environment.

                    ``stage``: Configured for use in a development/staging environment.

                    ``local``: Configured for use with a local Flask server.

                    ``testing``: Configured for use in unit testing.

                    ``cli``: Configured for use in a production environment without initializing extensions. (Use for CI/CD)
                api_title: The title (name) of the API to display in the OpenAPI documentation.
                api_version: The semantic version for the OpenAPI client.
                openapi_client_name: The package name to use for generated OpenAPI clients.
                kwargs: Additional settings to add to the configuration object or overrides for unprotected settings.

            Returns:
                A tuple with a fully configured Flask application and an Api ready to register additional Blueprints.

            Raises:
                RuntimeError: Attempted to override a protected setting, specified an additional setting that was not all
                    uppercase or the specified environment is invalid.
            """

            app = Flask(flask_app_name)

            CORS(app, expose_headers=["x-pagination", "etag"])  # TODO: this needs to be configurable! [271]

            flask_environment_configurator(app, flask_env, api_title, api_version, openapi_client_name, **kwargs)

            api = extensions.create_api(app, True if app.config["ENV"] == "cli" else False)

            views.register_blueprints(api)

            app.cli.add_command(genclient)

            return app, api


Run the App
-----------

To run the app in a :doc:`Flask server <flask:quickstart>` simply create an ``app.py`` (and corresponding ``.flaskenv``
file) that calls the example projects :func:`create_app <flask_ligand_example.create_app>` and specifies the
`Flask environment settings <configuration.html#built-in-flask-environments>`_ it should launch with.

.. code-block:: python

    try:
        app = flask_ligand_example.create_app(
            getenv("FLASK_ENV", "prod"),
            "Flask Ligand Example",
            flask_ligand_example.__version__,
            "flask-ligand-example-client",
        )
    except RuntimeError as e:
        print(f"Service initialization failure!\nReason: {e}")
        exit(1)

.. collapse:: Click for full example...

    .. code-block:: python

        """Flask app flask_ligand_example service entrypoint."""

        # ==============================================================================================================
        # Imports
        # ==============================================================================================================
        from sys import exit
        from os import getenv
        import flask_ligand_example


        # ==============================================================================================================
        # Globals
        # ==============================================================================================================
        try:
            app = flask_ligand_example.create_app(
                getenv("FLASK_ENV", "prod"),
                "Flask Ligand Example",
                flask_ligand_example.__version__,
                "flask-ligand-example-client",
            )
        except RuntimeError as e:
            print(f"Service initialization failure!\nReason: {e}")
            exit(1)

Explore the App
===============

.. important:: Once again reminding you that the `example project`_ contains all the code referenced in this guide.

The `example project`_ has all the bells and whistles enabled for the ``flask-ligand`` library which can be explored by
using the included :swagger-ui:`SwaggerUI documentation <>`. Follow the instructions below to start start running a
local Flask server to serve the :swagger-ui:`SwaggerUI documentation <>`.

1. Generate a '.env' file to configure Flask server to use the included Docker environment::

    $ make gen-local-env-file

2. Initialize the database::

    $ make setup-db

3. Generate a JWT access token with admin rights for accessing the included example project endpoints::

    $ make gen-admin-access-token

4. Start the local Flask server::

    $ make run

5. Open a browser and navigate to http://localhost:5000/apidocs.
6. Click the 'Authorize' button and paste in the JWT access token you created previously.

Now go ahead and start playing around with the API!

Access Keycloak Admin Console
-----------------------------

If you would like to make changes to the `Keycloak`_ IAM clients to explore authentication then you can access the
admin console by navigating to 'http://localhost:8080/admin/master/console/'. The admin credentials can be found in the
'docker/env_files/integration.env/' file.

Flask-Migrate Auto-generation
=============================

For :doc:`Flask-Migrate <flask-migrate:index>` to work well when auto-generating migration scripts it is critical that
the ``script.py.mako`` template in the ``migrations`` folder include an import for ``sqlalchemy_utils``. The
`example project`_ already has the template updated, but if you are using the ``flask-ligand`` library without
copying the `example project`_, then it is necessary you make the appropriate update to the ``script.py.mako`` template
before using :doc:`Flask-Migrate <flask-migrate:index>`.

.. _`example project`: https://github.com/cowofevil/flask-ligand-example
.. _`Keycloak`: https://www.keycloak.org/
