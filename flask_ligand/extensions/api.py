"""Api extension initialization

Override base classes here to allow painless customization in the future.
"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import flask

# noinspection PyPackageRequirements
import marshmallow as ma
from http import HTTPStatus
from typing import TYPE_CHECKING

# noinspection PyPackageRequirements
from flask_sqlalchemy import BaseQuery as BaseQueryOrig
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_smorest import Api as ApiOrig, Blueprint as BlueprintOrig, Page


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional, Any


# ======================================================================================================================
# Globals
# ======================================================================================================================
ISO_8601_DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"  # This is acceptable in ISO 8601 and RFC 3339


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def abort(http_status: HTTPStatus, message: Optional[str] = None) -> None:
    """Raise a HTTPException for the given http_status_code. Attach any keyword arguments to the exception for later
    processing.

    Args:
        http_status: A valid HTTPStatus enum which will be used for reporting the HTTP response status and code.
        message: Custom message to return within the body or a default HTTP status message will be returned instead.
    """

    message = message if message else http_status.phrase

    flask.abort(
        flask.make_response(
            flask.jsonify(
                code=http_status.value,
                status=http_status.name,
                message=message,
            ),
            http_status,
        )
    )


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
class Blueprint(BlueprintOrig):
    """Blueprint override"""


# Define custom converter to schema function
# def customconverter2paramschema(converter):
#     return {'type': 'custom_type', 'format': 'custom_format'}


class Api(ApiOrig):
    """Api override"""

    def __init__(self, app: Optional[flask.Flask] = None, *, spec_kwargs: Optional[dict[str, Any]] = None):
        super().__init__(app, spec_kwargs=spec_kwargs)

        # This adds an "Authorize" button to the SwaggerUI docs configured for custom "bearerAuth" doc decorators.
        self.spec.components.security_scheme("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})


class Schema(ma.Schema):
    """Schema override"""

    class Meta(ma.Schema.Meta):
        unknown = ma.EXCLUDE
        ordered = True


class AutoSchema(SQLAlchemyAutoSchema):
    """SQLAlchemyAutoSchema override"""

    class Meta(SQLAlchemyAutoSchema.Meta):
        include_fk = True
        unknown = ma.RAISE
        ordered = True
        datetimeformat = ISO_8601_DATETIME_FMT

    def update(self, obj: Any, data: Any) -> None:
        """Update object nullifying missing data"""

        loadable_fields = [k for k, v in self.fields.items() if not v.dump_only]

        for name in loadable_fields:
            setattr(obj, name, data.get(name))

    # FIXME: This does not respect allow_none fields
    @ma.post_dump
    def remove_none_values(self, data: dict[Any, Any], **_: dict[Any, Any]) -> dict[Any, Any]:
        return {key: value for key, value in data.items() if value is not None}


class SQLCursorPage(Page):
    """SQL cursor pager"""

    # https://flask-smorest.readthedocs.io/en/latest/pagination.html
    @property
    def item_count(self) -> int:
        return self.collection.count()  # type: ignore


class BaseQuery(BaseQueryOrig):  # type: ignore
    """Enable customized REST JSON error messages for 'get_or_404' and 'first_or_404' methods."""

    def get_or_404(self, ident: object, description: Optional[str] = None) -> Any:
        """Like `get` but aborts with 404 if not found instead of returning ``None``.

        Args:
            ident: A scalar, tuple, or dictionary representing the primary key.  For a composite (e.g. multiple column)
                primary key, a tuple or dictionary should be passed.
            description: Override default 404 status code message with a custom message instead.
        """

        rv = self.get(ident)
        if rv is None:
            abort(HTTPStatus(404), message=description)
        return rv

    def first_or_404(self, description: Optional[str] = None) -> Any:
        """Like 'first' but aborts with 404 if not found instead of returning ``None``.

        Args:
            description: Override default 404 status code message with a custom message instead.
        """

        rv = self.first()
        if rv is None:
            abort(HTTPStatus(404), message=description)
        return rv
