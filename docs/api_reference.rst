.. module:: flask_ligand

.. rstcheck: ignore-roles=sqlalchemy,swagger-ui
.. rstcheck: ignore-directives=autoclass,autofunction,autodata

=============
API Reference
=============

The :func:`create_app <flask_ligand.create_app>` function is the main entrypoint for creating
``flask_ligand`` Flask APIs. (See the for :doc:`Quickstart Guide <flask-ligand:quickstart>` for a full example of usage)

|

.. autofunction:: flask_ligand.create_app

Extensions
==========

The ``flask_ligand.extensions`` module provides extensions (overrides) to
:doc:`flask-sqlalchemy <flask-sqlalchemy:index>`, :doc:`marshmallow-sqlalchemy <marshmallow-sqlalchemy:index>`,
:doc:`flask-smorest <flask-smorest:api_reference>`, :sqlalchemy:`SQLAlchemy<index.html>` and
:doc:`flask-jwt-extended <flask-jwt-extended:api>` classes and functions used to construct
:doc:`Flask <flask:index>` REST applications.

Api
---
.. autofunction:: flask_ligand.extensions.api.abort

|

.. autoclass:: flask_ligand.extensions.api.Blueprint

|

.. autoclass:: flask_ligand.extensions.api.Api

|

.. autoclass:: flask_ligand.extensions.api.Schema

|

.. autoclass:: flask_ligand.extensions.api.AutoSchema

|

.. autoclass:: flask_ligand.extensions.api.SQLCursorPage

|

.. autoclass:: flask_ligand.extensions.api.BaseQuery
    :members:

|

Database
--------

.. autodata:: flask_ligand.extensions.database.DB
    :no-value:

|

Authentication (JWT)
--------------------

.. autoclass:: flask_ligand.extensions.jwt.User

|

.. autofunction:: flask_ligand.extensions.jwt.jwt_role_required

|

Default Settings
================

The ``flask_ligand.default_settings`` module defines default settings for the ``prod``, ``stage``, ``local``, and
``testing`` `environments <configuration.html#built-in-flask-environments>`_.

.. autoclass:: flask_ligand.default_settings.ProdConfig

|

.. autoclass:: flask_ligand.default_settings.StagingConfig

|

.. autoclass:: flask_ligand.default_settings.FlaskLocalConfig

|

.. autoclass:: flask_ligand.default_settings.TestingConfig

|

.. autofunction:: flask_ligand.default_settings.flask_environment_configurator

|

Views
=====

The ``flask_ligand.default_settings`` module contains built-in endpoints
(a.k.a. :class:`Flask View <flask.views.MethodView>`) for `generating OpenAPI clients`_ for TypeScript and Python. Also,
a global variable is provided that will add an "Authorize" button to the :swagger-ui:`SwaggerUI documentation <>`.

.. autoclass:: flask_ligand.views.openapi.OpenApiTypescriptAxios
    :members:  get

|

.. autoclass:: flask_ligand.views.openapi.OpenApiPython
    :members: get

|

.. autodata:: flask_ligand.views.common.openapi_doc.BEARER_AUTH
    :no-value:

|

.. _`generating OpenAPI clients`: https://openapi-generator.tech/
