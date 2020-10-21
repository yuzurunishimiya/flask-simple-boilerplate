from connection import session
from flask import request, abort
from functools import wraps
import json


class User():

    access = {
        "": 0,
        "guest": 0,
        "user": 1,
        "admin": 2,
        "super_admin": 3
    }

    def __init__(self, guid):
        success, user = self.get_data_from_guid(guid)
        if success:
            self.username = user.get("username")
            self.role = user.get("role")
        else:
            self.username = ""
            self.role = "guest"

    def get_data_from_guid(self, guid):
        try:
            user = session.get(guid)
            user = json.loads(user)
            return True, user
        except:
            return False, {}

    
    def is_allowed(self, access_level):
        if  self.access.get(self.role) >= self.access[access_level]:
            return True
        else:
            return False


def required_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            guid = request.cookies.get("guid")
            user = User(guid)
            if not user.is_allowed(access_level):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator