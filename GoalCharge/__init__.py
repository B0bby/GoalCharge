from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from . import views

app = Flask(__name__)
app.config["MONGODB_DB"] = "goalcharge"
app.config["SECRET_KEY"] = "WhatEverYouW4ntTh1sT0B3"

db = MongoEngine(app)

api = MongoRest(app)

views.init(app)

if __name__ == "__main__":
    app.run()
