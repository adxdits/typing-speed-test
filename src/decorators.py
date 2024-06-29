from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("template.login"))
        return f(*args, **kwargs)
    return decorated_function


def not_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username"):
            return redirect(url_for("template.home"))  # Remplacez "home" par la route appropriée
        return f(*args, **kwargs)
    return decorated_function
