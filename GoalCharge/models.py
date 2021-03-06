import datetime
from flask import url_for
from flask.ext.mongorest.resources import Resource
from GoalCharge import db

class User(db.Document):
    username = db.StringField(required=True, max_length=30, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    display_name = db.StringField(max_length=75)
    register_date= db.DateTimeField(default=datetime.datetime.now, required=True)
    charge = db.IntField()
    is_admin = db.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    def is_authenticated(self):
        if (id == None or id == ""):
            return False
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def self(self):
        return self

class UserResource(Resource):
    document = User

class Goal(db.Document):
    title = db.StringField(required=True, max_length=150)
    user = db.ReferenceField(User, required=True)
    charge = db.IntField()
    description = db.StringField()
    original = db.ReferenceField("Goal")
    status = db.StringField(required=True, default='not_started')
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    completed_at = db.DateTimeField()
    views = db.IntField(default=0)
    #date comparator
    #charge comparator

    def __unicode__(self):
        return self.title

    def gettitle(self):
        return self.title

class GoalResource(Resource):
    document = Goal

class Comment(db.Document):
    user = db.ReferenceField(User, required=True)
    message = db.StringField(required=True, max_length=255)
    goal = db.ReferenceField(Goal, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def __unicode__(self):
        return "%s Comment: %s" % (goal.title, message)

class CommentResource(Resource):
    document = Comment

class Milestone(db.Document):
    goal = db.ReferenceField(Goal, required=True)
    message = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    begin_at = db.DateTimeField()
    finished_at = db.DateTimeField()
    status = db.StringField(required=True, default='not_started')
    period = db.StringField(default="daily")

    def __unicode__(self):
        return "%s Milestone: %s" % (goal.title, message)

class MilestoneResource(Resource):
    document = Milestone
