"""Extensions initialization."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from typing import TYPE_CHECKING
from flask_ligand.extensions.api import Api
from flask_ligand.extensions import database, jwt


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from flask import Flask


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def create_api(app: Flask) -> Api:
    """Initialize the underlying API, extensions and databases.

    Args:
        app: The root Flask app to configure with the given extensions.
    """

    flask_ligand_api = Api(app)

    for extension in (database, jwt):
        extension.init_app(app)  # type: ignore

    return flask_ligand_api
