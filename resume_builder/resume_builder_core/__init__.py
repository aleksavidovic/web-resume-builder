from flask import Blueprint

resume_bp = Blueprint("resume", __name__)

from . import routes
