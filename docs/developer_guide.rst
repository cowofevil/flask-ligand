.. excerpt-start

Developer Quick Start Guide
===========================

Follow the instructions below to get a ``flask-ligand`` development environment up and running quickly!

Prerequisites
-------------

- Python 3.10+
- virtualenvwrapper_
- Docker_ (with `Compose V2`_)

Make Targets
------------

Execute the following command to get a full list of ``make`` targets::

    $ make help

Setup Python Environment
------------------------

1. Create a Python virtual environment::

    $ mkvirtualenv -p py310 flask-ligand

2. Setup develop environment::

    $ make develop-venv

3. Setup git pre-commit hooks::

    $ make setup-pre-commit

4. Verify that environment is ready for development::

    $ make test-tox

Configuration Settings
~~~~~~~~~~~~~~~~~~~~~~

The following environment variables are available to configure behavior of services that use this library when utilizing
the built-in 'local' and 'dev' and 'prod' Flask environments. (See `flask_environments.rst`_ for more details about the
available built-in Flask environments)

(**Note**: this project does support the use of '.env' files for loading environment variables)

.. list-table:: **Environment Variable Settings**
   :widths: 25 35 50
   :header-rows: 1

   * - ENV
     - Default Value for 'local' Flask Environment
     - Description
   * - ``SERVICE_PUBLIC_URL``
     - ``http://localhost:5000``
     - The public URL for this service. (Also used for generating OpenAPI clients)
   * - ``SERVICE_PRIVATE_URL``
     - ``http://localhost:5000``
     - The private URL for this service. (Also used for generating OpenAPI clients)
   * - ``ALLOWED_ROLES``
     - ``user,admin``
     - A comma separated list of user roles that are allowed for endpoint protection. (e.g. 'user,admin')
   * - ``OIDC_ISSUER_URL``
     - *Not set* (must be provided)
     - The OpenID Connect IAM URL to use for authentication.
   * - ``OIDC_REALM``
     - *Not set* (must be provided)
     - The OpenID Connect IAM realm to use for authentication.
   * - ``SQLALCHEMY_DATABASE_URI``
     - ``sqlite:///:memory:``
     - The URI for a PostgreSQL database to use for persistent storage. (See `database_configuration.rst`_ for more
       information)
   * - ``OPENAPI_GEN_SERVER_URL``
     - ``http://api.openapi-generator.tech``
     - The OpenAPI online generator server URL to use for creating clients.

Python Black Support
--------------------

This repo utilizes `Python Black`_ for automatic code formatting using the ``make format`` task. However, this is not
very convenient to use on a regular basis and instead it is recommended to integrate Python Black into your IDE
workflow. Checkout these `editor integration`_ guides for integrating `Python Black`_ with popular IDEs and text
editors.

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _Docker: https://www.docker.com/products/docker-desktop/
.. _Compose V2: https://docs.master.dockerproject.org/compose/#compose-v2-and-the-new-docker-compose-command
.. _flask_environments.rst: docs/flask_environments.rst
.. _database_configuration.rst: docs/database_configuration.rst
.. _Python Black: https://black.readthedocs.io/en/stable/
.. _editor integration: https://black.readthedocs.io/en/stable/integrations/editors.html

.. excerpt-end

Integration Testing
-------------------

See `integration_testing.rst`_ for more details on how to setup and run the integration tests for the ``flask-ligand``
project.

Contributing
------------

See `CONTRIBUTING.rst`_ for more details on developing for the ``flask-ligand`` project.

Release Process
---------------

See `release_process.rst`_ for information on the release process for the ``flask-ligand`` project.

.. _integration_testing.rst: integration_testing.rst
.. _CONTRIBUTING.rst: ../CONTRIBUTING.rst
.. _release_process.rst: release_process.rst
