from functools import wraps
from flask import redirect, url_for, flash, current_app
from flask_login import current_user


def anonymous_user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.", "info")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)

    return decorated_function


def feature_flag_required(flag):
    def feature_flag_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_app.config["FEATURE_FLAGS"][flag]:
                flash(f"Feature not enabled: {flag}.", "danger")
                return redirect(url_for("main.index"))
            return f(*args, **kwargs)

        return decorated_function

    return feature_flag_required
