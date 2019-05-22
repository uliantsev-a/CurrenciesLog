from flask import request, make_response
from functools import wraps
from werkzeug.security import check_password_hash

from project.models.auth import User


def auth_required(f):
    """
    Wrapper for the required authentication
    :return: decorator function with pass check
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            user = User.query.filter_by(username=auth.username).first()
            if user and check_password_hash(user.password, auth.password):
                return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated
