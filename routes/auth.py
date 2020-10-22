from flask import Blueprint
from flask import render_template, request, redirect

import bcrypt
import json
import time
import uuid

from connection import session, db_users
from routes.helper import LoginForm, RegisterForm
from routes.structure import user_structure

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        remember = form.remember_me.data
        user = db_users.find_one({"username": username})
        if user:
            is_match = bcrypt.checkpw(password.encode(), user["password"].encode())
            if is_match:
                expire = 60*60*2
                if remember:
                    expire += 60*60*7
                token = str(uuid.uuid4()) + str(uuid.uuid4().hex)
                session.set(token, json.dumps({"username": user["username"], "role": user["role"]}), expire)
                return redirect("/")
            else:
                form.password.errors = ["Password is wrong."]
        else:
            form.username.errors = ["Cannot find user with username: {}.".format(form.username.data)]

    return render_template("content/login.html", form=form)


@auth_bp.route("/register")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = user_structure.copy()
            user["username"] = form.username.data
            user["password"] = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt()).decode()
            user["email"] = form.email.data
            user["user_id"] = form.username.data + "_" + str(uuid.uuid4())
            user["created_at"] = int(time.time())
            return redirect("content/login.html")
        except:
            return render_template("content/register.html", form=form, error="Something is Wrong! Try Again!")
    return render_template("content/register.html", form=form, error=None)
