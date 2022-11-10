.. rstcheck: ignore-roles=swagger-ui,openapi-gen

===============
OpenAPI Support
===============

The ``flask_ligand.views.openapi`` module contains built-in endpoints for :openapi-gen:`generating OpenAPI clients <>`
for :class:`TypeScript <flask_ligand.views.openapi.OpenApiTypescriptAxios>` and
:class:`Python <flask_ligand.views.openapi.OpenApiPython>`.

For OpenAPI client generation to work properly your ``flask-ligand`` based microservice must have the
``OPENAPI_GEN_SERVER_URL`` `setting configured`_ to a valid :openapi-gen:`OpenAPI Generator Server URL <>`. The
public OpenAPI generator server URL located at http://api.openapi-generator.tech is also available, but since it is not
a secure endpoint, it is recommended for use only in testing.

Online Generation
=================

Any microservice built with ``flask-ligand`` will have the following built-in endpoints for
:openapi-gen:`generating OpenAPI clients <>`:

* ``/openapi/typescript-axios/``: Generate a TypeScript client download link.
* ``/openapi/python/``: Generate a Python client download link.

For more details about the endpoint, use the included :swagger-ui:`SwaggerUI documentation <>`  with your
``flask-ligand`` based microservice running locally by opening a browser and navigating to
http://localhost:5000/apidocs.

Online Example
--------------

Generate a Python client download link with your ``flask-ligand`` based microservice running locally::

    curl -X 'GET' \
      'http://localhost:5000/openapi/python/' \
      -H 'accept: application/json'

Offline Generation
==================

The ``genclient`` and ``openapi`` :doc:`Flask sub-commands <flask:cli>` are provided for
:openapi-gen:`offline generation of OpenAPI clients <>` for your ``flask-ligand`` based microservice CI/CD pipelines.
Use ``flask genclient --help`` or ``flask openapi --help`` to get more details about the functionality that the
sub-commands provide.

.. important:: In order to fully utilize offline generation the ``FLASK_ENV`` environment variable should be set to
    ``cli`` which will prevent ``flask-ligand`` from initializing Flask extensions. However, **all settings
    required** by the `production environment`_ still need to be set to successfully generate an OpenAPI client.

Offline Example
---------------

Generate a Python client download link with your ``flask-ligand`` based microservice in offline mode::

    FLASK_ENV=cli flask genclient python

.. _`setting configured`: configuration.html#prod
.. _`production environment`: configuration.html#prod
