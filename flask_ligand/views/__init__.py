"""View modules initialization."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from typing import TYPE_CHECKING
from flask_ligand.views import openapi


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:
    from flask_ligand.extensions.api import Api


# ======================================================================================================================
# Globals
# ======================================================================================================================
MODULES = (openapi,)


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def register_blueprints(api: Api) -> None:
    """Initialize application with all modules"""

    for module in MODULES:
        api.register_blueprint(module.BLP)  # type: ignore
