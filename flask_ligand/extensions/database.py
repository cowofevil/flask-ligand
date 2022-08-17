"""Relational database."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from typing import TYPE_CHECKING
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_auto_coercion
from flask_ligand.extensions.api import BaseQuery


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from flask import Flask


# ======================================================================================================================
# Globals
# ======================================================================================================================
DB = SQLAlchemy(query_class=BaseQuery)  # pylint: disable=invalid-name


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def init_app(app: Flask) -> None:
    """Initialize relational database extension.

    Args:
        app: The root Flask app to configure with the given extension.
    """

    DB.init_app(app)
    DB.create_all(app=app)

    # See https://sqlalchemy-utils.readthedocs.io/en/latest/listeners.html?highlight=force#automatic-data-coercion
    force_auto_coercion()
