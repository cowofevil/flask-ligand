.. rstcheck: ignore-roles=sqlalchemy,swagger-ui
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

Selectively secure endpoint REST verbs to require a valid `JWT access token`_ containing certain roles by using the
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


.. _`example project`: https://github.com/cowofevil/flask-ligand-example
.. _`JWT access token`: https://auth0.com/blog/id-token-access-token-what-is-the-difference/
