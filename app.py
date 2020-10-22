from flask import Flask
from flask import request, jsonify, render_template
from flask_wtf.csrf import CSRFProtect

from setup import DevelopmentConfig, ProductionConfig
from connection import config

import os



app = Flask(__name__)
csrf = CSRFProtect(app)

if os.environ.get("mode", "development") == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


@app.errorhandler(400)
def handler_400(error):
    return jsonify({
        "succes": False,
        "code": 400,
        "msg": error.description,
        "data": []
    })


@app.errorhandler(401)
def handler_401(error):
    return jsonify({
        "success": False,
        "code": 401,
        "message": error.description,
        "data": []
    })


@app.errorhandler(403)
def handler_403(error):
    return jsonify({
        "success": False,
        "code": 403,
        "message": error.description,
        "data": []
    })


@app.errorhandler(404)
def handler_404(error):
    return render_template("content/notfound.html")


if __name__ == "__main__":
    app.run()