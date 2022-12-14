"""Common OpenAPI documentation specs for endpoints."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from typing import TYPE_CHECKING

# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


# ======================================================================================================================
# Globals
# ======================================================================================================================
BEARER_AUTH: Any = [{"bearerAuth": []}]  #: Enable bearer authentication for Swagger-UI docs
