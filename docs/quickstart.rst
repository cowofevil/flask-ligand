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

.. code-include :: :func:`flask_ligand_example.models.PetModel`

.. collapse:: Click for full example...

    .. code-include :: :func:`flask_ligand_example.models`

Schemas
-------

Define an :class:`AutoSchema <flask_ligand.extensions.api.AutoSchema>` to expose the model.

.. code-include :: :func:`flask_ligand_example.schemas.PetSchema`

Define a :class:`Schema <flask_ligand.extensions.api.Schema>` to validate the query arguments for a subset of fields
defined in the above :class:`AutoSchema <flask_ligand.extensions.api.AutoSchema>` for a
:class:`Flask View <flask.views.MethodView>` that will be created later.

.. code-include :: :func:`flask_ligand_example.schemas.PetQueryArgsSchema`

.. collapse:: Click for full example...

    .. code-include :: :func:`flask_ligand_example.schemas`

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

.. code-include :: :func:`flask_ligand_example.views.pet.Pets`

Use :func:`abort <flask_ligand.extensions.api.abort>` to return an error response.

.. code-include :: :func:`flask_ligand_example.views.pet._we_love_pets`

.. collapse:: Click for full example...

    .. code-include :: :func:`flask_ligand_example.views.pet`

Create the App
--------------

Connect the models, schemas and views together by calling :func:`create_app <flask_ligand.create_app>` followed by
registering the Blueprints for the views.

.. code-include :: :func:`flask_ligand_example.create_app`

.. collapse:: Click for full example...

    .. code-include :: :func:`flask_ligand_example`

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

5. Open a browser and navigate to 'http://localhost:5000/apidocs'.
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
