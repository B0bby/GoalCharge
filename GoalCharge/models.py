import datetime
from flask import url_for
from GoalCharge import db

class User(db.Document):
    username = db.StringField(required=True, max_length=30)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    display_name = db.StringField(max_length=75)
    register_date= db.DateTimeField(default=datetime.datetime.now, required=True)
    charge = db.IntField()
    is_admin = db.BooleanField(default=False)

    def __unicode__(self):
        return self.email

class Goal(db.Document):
    title = db.StringField(required=True, max_length=150)
    user = db.ReferenceField(User, required=True)
    charge = db.IntField()
    original = db.ReferenceField(self)
    status = db.StringField(required=True, default='not_started')
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    #date comparator
    #charge comparator

    def __unicode__(self):
        return self.title

class Comment(db.Document):
    user = db.ReferenceField(User, required=True)
    message = db.StringField(required=True, max_length=255)
    goal = db.ReferenceField(Goal, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def __unicode__(self):
        return "%s Comment: %s" % (goal.title, message)

class Milestone(db.Document):
    goal = db.ReferenceField(Goal, required=True)
    message = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    finished_at = db.DateTimeField()
    period = db.StringField()

    def __unicode__(self):
        return "%s Milestone: %s" % (goal.title, message)
