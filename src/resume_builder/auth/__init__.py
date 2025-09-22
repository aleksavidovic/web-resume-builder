from flask import Blueprint

auth_bp = Blueprint("auth", import_name=__name__, template_folder="templates", url_prefix="/auth")

from . import routes
