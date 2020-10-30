from flask import request, abort
from flask_wtf import FlaskForm
from functools import wraps
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import ( 
    StringField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.fields.html5 import EmailField

from connection import session
import json


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please fill out this field"), Length(min=8, max=30)])
    password = PasswordField("Password", validators=[DataRequired(message="Please fill out this field"), Length(min=8, max=30)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username cannot be empty"), Length(min=8, max=30)])
    password = PasswordField("Password", validators=[DataRequired(message="Password cannot be empty"), Length(min=8, max=30), EqualTo("confirm", message="password must match")])
    confirm = PasswordField("Repeat Password", validators=[DataRequired("Repeat password must match with Password"), Length(min=8, max=30)])
    email = EmailField("Email address", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

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
