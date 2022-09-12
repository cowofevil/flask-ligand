"""OpenAPI client generator proxy."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
from json import dumps
from flask import Flask
from requests import post
from http import HTTPStatus
from typing import TYPE_CHECKING
from urljoin import url_path_join
from requests.exceptions import RequestException
from flask_ligand.extensions.api import abort


# ======================================================================================================================
# Type Checking
# ======================================================================================================================
if TYPE_CHECKING:  # pragma: no cover
    from typing import Any


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
def get_openapi_client_dl_link(  # type: ignore
    current_app_context: Flask,
    use_private_url: bool,
    gen_lang: str,
    options: dict[str, str],
) -> dict[Any, Any]:
    """Get a download link URL from an OpenAPI online generator for a given language.

    See for more details: https://openapi-generator.tech/docs/generators

    Args:
        current_app_context: The current Flask app context.
        use_private_url: Specify whether to use a public or private URL for the generated OpenAPI client.
        gen_lang: The target generator language for the client.
        options: A dictionary of options for the particular generator language.

    Returns:
        A dictionary containing the UUID of the client along with download URL for the client.

    Raises:
        werkzeug.exceptions.HTTPException
    """

    verify_ssl_cert: bool = current_app_context.config["VERIFY_SSL_CERT"]
    open_api_gen_server_url: str = current_app_context.config["OPENAPI_GEN_SERVER_URL"]

    # Grab the OpenAPI spec from the view function directly to guarantee it is constructed correctly.
    api_spec: dict[str, Any] = current_app_context.view_functions["api-docs.openapi_json"]().json

    if use_private_url:
        api_spec["servers"][0] = {"url": current_app_context.config["SERVICE_PRIVATE_URL"]}
    else:
        api_spec["servers"][0] = {"url": current_app_context.config["SERVICE_PUBLIC_URL"]}

    try:
        return post(  # type: ignore
            url_path_join(open_api_gen_server_url, "/api/gen/clients/", gen_lang),
            headers={"Content-Type": "application/json"},
            data=dumps({"spec": api_spec, "options": options}),
            verify=verify_ssl_cert,
            timeout=(3.05, 10),  # Set timeout for slow connections
        ).json()
    except RequestException:
        abort(
            HTTPStatus(500),
            message=f"The request to the '{open_api_gen_server_url}' server failed!",
        )
