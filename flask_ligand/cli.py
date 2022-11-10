"""Custom Flask Commands for Ligand."""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import annotations
import click
from flask import current_app
from flask_ligand.controllers import gen_typescript_dl_link, gen_python_dl_link


# ======================================================================================================================
# Functions: Public
# ======================================================================================================================
@click.group()
@click.option(
    "--private/--public",
    default=False,
    show_default=True,
    help="Generate an OpenAPI download link for the SERVICE_PRIVATE_URL or SERVICE_PUBLIC_URL",
)
@click.pass_context
def genclient(ctx: click.Context, private: bool) -> None:
    """Generate download links for supported OpenAPI clients."""

    # ensure that ctx.obj exists and is a dict to handle "--help" correctly for sub-commands
    ctx.ensure_object(dict)

    ctx.obj["PRIVATE"] = private


@genclient.command()
@click.pass_context
def typescript(ctx: click.Context) -> None:
    """Generate a download link for the TypeScript OpenAPI client."""

    private: bool = ctx.obj["PRIVATE"]

    print(gen_typescript_dl_link(current_app, private)["link"])  # pragma: no cover


@genclient.command()
@click.pass_context
def python(ctx: click.Context) -> None:
    """Generate a download link for the Python OpenAPI client."""

    private: bool = ctx.obj["PRIVATE"]

    print(gen_python_dl_link(current_app, private)["link"])  # pragma: no cover
