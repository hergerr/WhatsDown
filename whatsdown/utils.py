from flask import session, redirect, url_for
from functools import wraps


def check_logged_in_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged' in session and 'user' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
