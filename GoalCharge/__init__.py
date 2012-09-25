from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_DB"] = "goalcharge"
app.config["SECRET_KEY"] = "WhatEverYouW4ntTh1sT0B3"

db = MongoEngine(app)

def register_blueprints(app):
    #app.register_blueprint(model)
    return True

register_blueprints(app)

if __name__ == "__main__":
    app.run()
