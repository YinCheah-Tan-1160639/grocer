from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(*roles):
    """Decorator to require specific roles to access a view."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('user_role')  # Get user type from session
            if user_role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))  # Redirect to the index or login page
            return f(*args, **kwargs)
        return decorated_function
    return decorator