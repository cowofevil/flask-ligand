"""Flask app flask_ligand service entrypoint. (Use this Flask app testing/debugging purposes only!)"""

# ======================================================================================================================
# Imports
# ======================================================================================================================
from sys import exit
from os import getenv
import flask_ligand


# ======================================================================================================================
# Globals
# ======================================================================================================================
try:
    app = flask_ligand.create_app(
        getenv("FLASK_ENV", "prod"), "Service Library", flask_ligand.__version__, "flask-ligand-client"
    )
except RuntimeError as e:
    print(f"Service initialization failure!\nReason: {e}")
    exit(1)
