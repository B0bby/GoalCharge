from flask import Flask
from flask.ext.mongoengine import MongoEngine
from mongoengine.queryset import DoesNotExist
from flask.ext.mongorest import MongoRest
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config["MONGODB_DB"] = "goalcharge"
app.config["SECRET_KEY"] = "WhatEverYouW4ntTh1sT0B3"

db = MongoEngine(app)

api = MongoRest(app)

login_manager = LoginManager()
login_manager.setup_app(app)

from . import models
from models import User
@login_manager.user_loader
def load_user(userid):
    try:
        return User.objects.get(id=userid)
    except DoesNotExist:
        return None

from . import views
views.init(app)

if __name__ == "__main__":
    app.run()
