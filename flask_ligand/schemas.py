"""OpenAPI Schemas."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
# noinspection PyPackageRequirements
from marshmallow import fields
from flask_ligand.extensions.api import Schema


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
class OpenApiClientDownloadRespSchema(Schema):
    """A schema defining where to download pre-configured OpenAPI clients for this service."""

    code = fields.UUID(required=True)
    link = fields.Url(required=True, schemes=("http", "https"))


class OpenApiClientDownloadQueryArgsSchema(Schema):
    """A schema for specifying whether to use a public or private URL for the generated OpenAPI client."""

    use_private_url = fields.Boolean(dump_default=True)
