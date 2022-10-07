.. rstcheck: ignore-roles=sqlalchemy

Database Configuration
======================

The ``flask-ligand`` library uses the excellent :doc:`Flask-SQLAlchemy <flask-sqlalchemy:index>` project under the hood
for database management and access. The :doc:`Flask-SQLAlchemy <flask-sqlalchemy:index>` project in turn utilizes the
equally excellent :sqlalchemy:`SQLAlchemy <index.html>` for direct communication to the underlying database.

This document covers how to configure ``flask-ligand`` to utilize the many different databases supported by
:sqlalchemy:`SQLAlchemy <index.html>` and :doc:`Flask-SQLAlchemy <flask-sqlalchemy:index>`.

Configure Database URI
----------------------

The ``flask-ligand`` library utilizes the ``SQLALCHEMY_DATABASE_URI``
:doc:`environment variable <flask-sqlalchemy:config>` for configuring the connection to a
:sqlalchemy:`SQLAlchemy supported databases <core/engines.html#supported-databases>`. The ``SQLALCHEMY_DATABASE_URI``
:doc:`environment variable <flask-sqlalchemy:config>` requires that the URI begins with a
``dialect+driver`` :sqlalchemy:`identifier <dialects/index.html>` that specifies the database type and the associated
driver to use for communication.

**Example URI**

As an example, let's consider the following database infrastructure we want to use for persistent storage:

.. list-table:: **Database Infrastructure**
   :widths: 60 100

   * - **Database Type** (a.k.a :sqlalchemy:`dialect <dialects/index.html>`)
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

:sqlalchemy:`SQLAlchemy <index.html>` supports many different Python drivers for each supported database type. It can be
quite overwhelming when first using :sqlalchemy:`SQLAlchemy <index.html>` to know which driver to use for your desired
database infrastructure (:sqlalchemy:`dialect <dialects/index.html>`). A rule of thumb for which driver to use is
to consider the following constraints:

- Do you need async support?
- Does your build environment have GCC and all necessary headers available for compiling Python packages?
- Are you using the standard CPtyhon interpreter?
- Do you need Unicode support?
- Which version of your desired database are you using?
