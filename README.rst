============
flask-ligand
============

.. excerpt-start

|docs-status| |build-status| |pypi-status| |codecov-status| |pre-commit-status|

A simple Flask library for building microservices with RBAC JWT security, OpenAPI client and SQLAlchemy database
support.

Install
=======

.. code-block:: bash

    $ pip install flask-ligand

Resources
=========

- `Documentation`_
- `Changelog`_
- `Contributing`_
- `License`_

Why Use this Library?
=====================

Using `Flask`_ to create a REST based microservice is a daunting process which will definitely require the use of
many different `Flask extensions`_ which will really slow down the process of actually writing a functional REST
microservice that can be used safely in a production environment. This library seeks to use the best
`Flask extensions`_ loosely combined together to deliver a delightful developer experience by providing the following
functionality out-of-the-box:

- Create database models using the industry standard `SQLAlchemy ORM`_
- Leverage those same database models to create schemas for marshalling data in and out of your `Flask`_ endpoints
  defined via Blueprints
- Provide automatic `SwaggerUI`_ docs for quickly developing and testing your `Flask`_ application without the need
  of external tools like curl, Postman or Hoppscotch
- `Generate OpenAPI clients`_ for a variety of languages

    - Endpoints for generating Python and Typescript clients already included!

- Protect endpoints with JWT security with a `OpenID Connect`_ IAM like `Auth0`_ or `Keycloak`_

    - Optionally control access to endpoints using `RBAC`_

- Easily manage database migrations using Alembic through the fantastic Flask-Migrate library and command-line tools

.. _`Flask`: https://flask.palletsprojects.com/en/2.2.x/
.. _`Flask extensions`: https://flask.palletsprojects.com/en/2.2.x/extensions/
.. _`SQLAlchemy ORM`: https://www.sqlalchemy.org/
.. _`SwaggerUI`: https://swagger.io/tools/swagger-ui/
.. _`Generate OpenAPI clients`: https://openapi-generator.tech/
.. _`Auth0`: https://auth0.com/
.. _`Keycloak`: https://www.keycloak.org/
.. _`RBAC`: https://en.wikipedia.org/wiki/Role-based_access_control
.. _`OpenID Connect`: https://openid.net/connect/
.. _`Documentation`: https://flask-ligand.readthedocs.io/en/stable/
.. _`Changelog`: ./CHANGELOG.md
.. _`Contributing`: ./CONTRIBUTING.rst
.. _`License`: ./LICENSE

.. |docs-status| image:: https://img.shields.io/readthedocs/flask-ligand/stable?logo=readthedocs
   :target: https://flask-ligand.readthedocs.io/en/stable/
   :alt: Docs
.. |build-status| image:: https://img.shields.io/github/workflow/status/cowofevil/flask-ligand/Build?logo=github
   :target: https://github.com/cowofevil/flask-ligand/actions/workflows/bump_and_publish_release.yml
   :alt: Build
.. |pypi-status| image:: https://img.shields.io/pypi/v/flask-ligand?color=blue&logo=pypi
   :target: https://pypi.org/project/flask-ligand/
   :alt: PyPI
.. |codecov-status| image:: https://img.shields.io/codecov/c/gh/cowofevil/flask-ligand?color=teal&logo=codecov
   :target: https://app.codecov.io/gh/cowofevil/flask-ligand
   :alt: Codecov
.. |pre-commit-status| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
