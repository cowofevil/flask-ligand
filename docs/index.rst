============
flask-ligand
============

.. rstcheck: ignore-substitutions=version

Release v\ |version| (:ref:`Changelog <changelog>`)

.. include:: ../README.rst
   :start-after: excerpt-start
   :end-before: excerpt-end

Why not Use FastAPI Instead?
----------------------------

This library mimics many of the features of `FastAPI`_, well, because `FastAPI`_ is really good! However, the
:doc:`Flask <flask:index>` ecosystem is much larger than `FastAPI`_ giving many more options when it comes to high
quality extensions. The one large advantage `FastAPI`_ has over :doc:`Flask <flask:index>` currently is support for
asynchronous I/O via `Starlette`_ which can improve performance dramatically.

:doc:`Flask's asyncio journey <flask:async-await>` has just started and :doc:`Quart <quart:index>` most likely being the
future for asyncio in the :doc:`Flask <flask:index>` ecosystem. This library was inspired by FastAPI and I think anyone
considering starting a greenfield microservice should give serious consideration to using `FastAPI`_.

However, if you have an existing :doc:`Flask <flask:index>` microservice needing an upgrade in feature set then this
library brings together the best extensions that the :doc:`Flask <flask:index>` ecosystem has to offer! If you're
creating a greenfield microservice then this library lets you tap into a wide range of other
:doc:`Flask extensions <flask:extensions>` that will help you solve your problem(s) faster.

Guides
======

.. toctree::
    :maxdepth: 3

    quickstart
    configuration
    development

Powered By
==========

This library is powered by the following awesome projects:

- :doc:`flask-smorest <flask-smorest:index>`
    - :doc:`apispec <apispec:index>`
    - :doc:`marshmallow <marshmallow:index>`
    - :doc:`webargs <webargs:index>`
- :doc:`flask-sqlalchemy <flask-sqlalchemy:index>`
- :doc:`flask-jwt-extended <flask-jwt-extended:index>`
- :doc:`flask-cors <flask-cors:index>`
- :doc:`flask-migrate <flask-migrate:index>`
- :doc:`marshmallow-sqlalchemy <marshmallow-sqlalchemy:index>`
    - :sqlalchemy:`SQLAlchemy <index.html>`
- :doc:`sqlalchemy-utils <sqlalchemy-utils:index>`

.. toctree::
    :hidden:
    :maxdepth: 3

    api_reference

.. toctree::
    :hidden:
    :maxdepth: 1

    changelog
    license
    authors

.. _`FastAPI`: https://fastapi.tiangolo.com/
.. _`Starlette`: https://www.starlette.io/
