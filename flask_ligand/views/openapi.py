"""OpenAPI helper resources."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from flask import current_app
from typing import TYPE_CHECKING
from flask.views import MethodView
from flask_ligand.extensions.api import Blueprint
from flask_ligand.controllers import gen_python_dl_link, gen_typescript_dl_link
from flask_ligand.schemas import OpenApiClientDownloadRespSchema, OpenApiClientDownloadQueryArgsSchema


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from typing import Mapping, Any


# ======================================================================================================================
# Globals
# ======================================================================================================================
BLP = Blueprint(
    "OpenAPI Client Generator",
    __name__,
    url_prefix="/openapi",
    description="Provides download links to pre-configured OpenAPI clients for this service.",
)


# ======================================================================================================================
# Classes: Public
# ======================================================================================================================
@BLP.route("/typescript-axios/")
class OpenApiTypescriptAxios(MethodView):
    @BLP.arguments(OpenApiClientDownloadQueryArgsSchema, location="query")
    @BLP.response(200, OpenApiClientDownloadRespSchema)
    def get(self, args: Mapping[str, Any]) -> Any:
        """
        Generate a 'typescript-axios' OpenAPI client for this service.

        **NOTE**: The link provided is only good for one download before it expires!

        See for more details: https://openapi-generator.tech/docs/generators
        """

        use_private_url = args.get("use_private_url", True)

        return OpenApiClientDownloadRespSchema().dump(gen_typescript_dl_link(current_app, use_private_url))


@BLP.route("/python/")
class OpenApiPython(MethodView):
    @BLP.arguments(OpenApiClientDownloadQueryArgsSchema, location="query")
    @BLP.response(200, OpenApiClientDownloadRespSchema)
    def get(self, args: Mapping[str, Any]) -> Any:
        """
        Generate a 'python' OpenAPI client for this service.

        **NOTE**: The link provided is only good for one download before it expires!

        See for more details: https://openapi-generator.tech/docs/generators
        """

        use_private_url = args.get("use_private_url", True)

        return OpenApiClientDownloadRespSchema().dump(gen_python_dl_link(current_app, use_private_url))
