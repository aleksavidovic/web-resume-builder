from flask import Blueprint

job_app_tracker_bp = Blueprint("job_app_tracker", __name__)

from . import routes
