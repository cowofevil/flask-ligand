Integration Testing
===================

This repo contains Docker_ compose scripts and associated ``make`` targets for setting up and executing integration
tests against a PostgreSQL + Keycloak environment.

Utilize Docker Environment
--------------------------

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

.. _Docker: https://www.docker.com/products/docker-desktop/
.. _SwaggerUI: https://swagger.io/tools/swagger-ui/
