======================
Database Configuration
======================

The ``flask-ligand`` library uses the excellent `flask-sqlalchemy`_ project under the hood for database management and
access. The `flask-sqlalchemy`_ project in turn utilizes the equally excellent `SQLAlchemy`_ for direct communication to
the underlying database.

This document covers how to configure ``flask-ligand`` to utilize the many different databases supported by
`SQLAlchemy`_ and `flask-sqlalchemy`_.

Configure Database URI
----------------------

The ``flask-ligand`` library utilizes the ``SQLALCHEMY_DATABASE_URI`` `environment variable`_ for configuring the
connection to a `SQLAlchemy`_ `supported databases`_. The ``SQLALCHEMY_DATABASE_URI`` `environment variable`_
requires that the URI begins with a ``dialect+driver`` `identifier`_ that specifies the database type and the associated
driver to use for communication.

**Example URI**

As an example, let's consider the following database infrastructure we want to use for persistent storage:

.. list-table:: **Database Infrastructure**
   :widths: 60 100

   * - **Database Type** (a.k.a `dialect`_)
     - PostgreSQL
   * - **Database Driver**
     - ``pg8000``
   * - **Database Hostname**
     - ``localhost``
   * - **Database Port**
     - ``5432``
   * - **Database User**
     - ``admin``
   * - **Database Password**
     - ``password``
   * - **Database Name**
     - ``testdb``

The ``SQLALCHEMY_DATABASE_URI`` should be set to::

    postgresql+pg8000://admin:password@localhost:5432/testdb

Database Drivers
----------------

`SQLAlchemy`_ supports many different Python drivers for each supported database type. It can be quite overwhelming when
first using `SQLAlchemy`_ to know which driver to use for your desired database infrastructure (`dialect`_). A rule of
thumb for which driver to use is to consider the following constraints:

- Do you need async support?
- Does your build environment have GCC and all necessary headers available for compiling Python packages?
- Are you using the standard CPtyhon interpreter?
- Do you need Unicode support?
- Which version of your desired database are you using?

.. _flask-sqlalchemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _environment variable: https://docs.sqlalchemy.org/en/14/core/engines.html
.. _supported databases: https://docs.sqlalchemy.org/en/14/core/engines.html
.. _identifier: https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
.. _dialect: https://docs.sqlalchemy.org/en/14/dialects/index.html
