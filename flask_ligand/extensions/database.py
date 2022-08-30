"""Relational database."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from typing import TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy_utils import force_auto_coercion
from flask_ligand.extensions.api import BaseQuery


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from flask import Flask


# ======================================================================================================================
# Globals
# ======================================================================================================================
DB = SQLAlchemy(query_class=BaseQuery)  # pylint: disable=invalid-name
MIGRATE = Migrate()


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def init_app(app: Flask) -> None:
    """Initialize relational database extension.

    Args:
        app: The root Flask app to configure with the given extension.
    """

    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    if app.config["DB_AUTO_UPGRADE"]:  # pragma: no cover (Covered by integration tests)
        with app.app_context():
            upgrade(directory=app.config["DB_MIGRATION_DIR"])

    # See https://sqlalchemy-utils.readthedocs.io/en/latest/listeners.html?highlight=force#automatic-data-coercion
    force_auto_coercion()
