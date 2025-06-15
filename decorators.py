## create the admin_required decorators to validate if a user is an admin
from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user, login_required

def admin_required(f):
    @wraps(f)
    @login_required  # Ensure user is first logued in
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('No eres administrador para acceder a esta página.', 'danger')
            return redirect(url_for('index')) # o a un abort(403)
        return f(*args, **kwargs)
    return decorated_function