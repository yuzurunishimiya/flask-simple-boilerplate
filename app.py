from flask import Flask
from flask import request, jsonify

from setup import DevelopmentConfig, ProductionConfig
from connection import config

import os

app = Flask(__name__)

if os.environ.get("mode", "development") == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


@app.errorhandler(400)
def handler_400(error):
    return jsonify({
        "succes": False,
        "code": 400,
        "msg": error.description.get("message", "Bad request, 400"),
        "data": []
    })


@app.errorhandler(401)
def handler_401(error):
    return jsonify({
        "success": False,
        "code": 401,
        "message": error.description.get("message", "You are unatuhorize, 401"),
        "data": []
    })


@app.errorhandler(403)
def handler_403(error):
    return jsonify({
        "success": False,
        "code": 403,
        "message": error.description.get("message", "Forbidden access! You are unauthenticate, 403"),
        "data": []
    })


if __name__ == "__main__":
    app.run()