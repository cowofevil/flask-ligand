===================
Integration Testing
===================

This repo contains Docker_ compose scripts and associated ``make`` targets for setting up and executing integration
tests against a PostgreSQL + Keycloak environment.

Prerequisites
=============

- Python 3.10+
- virtualenvwrapper_
- Docker_

Getting Help with Make Tasks
============================

Execute the following command to get a full list of ``make`` targets::

    $ make help

Setup Integration Environment
=============================

1. Create a Python virtual environment::

    $ mkvirtualenv -p py310 flask-ligand

2. Setup develop environment::

    $ make develop-venv

3. Setup Docker_ environment::

    $ make setup-integration

4. Verify that environment is ready for testing::

    $ make check-integration

5. Execute integration tests::

    $ make test-integration

Utilize Integration Environment for Exploratory Testing
=======================================================

It can be quite useful to experiment while developing new features by manually exploring with a production like
environment. This can be easily accomplished by leveraging the integration testing environment!

Simply execute steps 1-4 from the following section to get an operational integration test environment then execute
the ``make`` target::

    $ make gen-local-env-file

The ``make gen-local-env-file`` will create a new ``.env`` file that contains the environment variables necessary to
access the integration environment.

Once the ``.env`` file has been generated you can start a local Flask server by executing the ``make`` target::

    $ make run

Simple navigate to http:://localhost:5000/apidocs to access the local environment via `SwaggerUI`_.

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _Docker: https://www.docker.com/products/docker-desktop/
.. _SwaggerUI: https://swagger.io/tools/swagger-ui/
