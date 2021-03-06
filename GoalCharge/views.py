import datetime
from flask import (abort, current_app, render_template, request, redirect, url_for)
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest import methods
from flask.ext.login import (login_required, current_user, login_user,
        logout_user)
from mongoengine.queryset import DoesNotExist, NotUniqueError
from GoalCharge import (api, login_manager)
from GoalCharge.forms import (LoginForm, RegisterForm, NewGoalForm, NewMilestoneForm)
from GoalCharge.helpers import EncryptPassword

def init(app):
    @app.route("/")
    def index():
        from models import User, Goal
        goals_most_views = Goal.objects.order_by("-views")
        goals_most_charge = Goal.objects.order_by("-charge")
        goals_newest = Goal.objects.order_by("-created_at")
        return render_template("index.html", goals_most_views=goals_most_views, goals_most_charge=goals_most_charge, goals_newest=goals_newest)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        from GoalCharge.models import User
        form = LoginForm(request.form)
        login_status = "form"
        if request.method == "POST":
            try:
                password = EncryptPassword(request.form['password'])
                user = User.objects.get(username=request.form['username'],
                        password=password)
                login_user(user)
                login_status = "success"
                return redirect(url_for("index"))
            except DoesNotExist:
                login_status = "fail"
        return render_template("login.html", login_status=login_status, form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        from models import User
        form = RegisterForm(request.form)
        register_status = "form"
        if request.method == "POST":
            if request.form['password'] == request.form['password_confirm']:
                try:
                    password = EncryptPassword(request.form['password'])
                    new_user = User(username=request.form['username'],email=request.form['email'],password=password, display_name=request.form['username'])
                    new_user.save()
                    register_status = "success"
                except NotUniqueError:
                    register_status = "fail"
            else:
                register_status = "form_password"
        return render_template("register.html", register_status=register_status, form=form)

    @app.route("/user/<user_id>")
    def user(user_id):
        from models import User, Goal
        user = User.objects.get_or_404(id=user_id)
        goals = Goal.objects(user=user)
        return render_template("user/profile.html", user=user, goals=goals)

    @app.route("/user/<user_id>/edit", methods=['GET', 'POST'])
    @login_required
    def user_edit(user_id):
        from models import User
        user = User.objects.get_or_404(id=user_id)
        edit_status = "unauth"
        if current_user.get_id() == user.id or current_user.is_admin:
            edit_status = "form"
            if request.method == "POST":
                user.display_name = request.form['display_name']
                user.email = request.form['email']
                if request.form['password'] != "":
                    if request.form['password'] == request.form['password_confirm']:
                        user.password = EncryptPassword(request.form['password'])
                        user.save()
                        edit_status = "success"
                    else:
                        edit_status = "fail"
                else:
                    user.save()
                    edit_status = "success"
        return render_template("user/edit.html", user=user, edit_status=edit_status)

    @app.route("/goal/<goal_id>")
    def goal(goal_id):
        from models import Goal, Milestone
        goal = Goal.objects.get_or_404(id=goal_id)
        milestones = Milestone.objects(goal=goal)
        goal.views = goal.views + 1
        goal.save()
        return render_template("goal/goal.html", goal=goal, milestones=milestones)

    @app.route("/goal/<goal_id>/milestone/new", methods=['GET', 'POST'])
    def milestone_new(goal_id):
        from models import Goal, Milestone
        form = NewGoalForm(request.form)
        goal = Goal.objects.get_or_404(id=goal_id)
        form = NewMilestoneForm(request.form)
        new_status = "form"
        if request.method == "POST":
            if (current_user.get_id() == goal.user.id):
                try:
                    new_milestone = Milestone(message=form.message.data, goal=goal)
                    new_milestone.save()
                    new_status = "success"
                except OperationError:
                    new_status = "fail"
            else:
                new_status = "fail"
        return render_template("milestone/new.html", goal=goal, form=form, new_status=new_status)

    @app.route("/goal/<goal_id>/edit", methods=['GET', 'POST'])
    @login_required
    def goal_edit(goal_id):
        from models import Goal
        goal = Goal.objects.get_or_404(id=goal_id)
        edit_status = "unauth"
        if current_user.get_id() == goal.user.id:
            edit_status = "form"
            if request.method == "POST":
                goal.title = request.form['title']
                goal.description = request.form['description']
                goal.save()
                edit_status = "success"
        return render_template("goal/edit.html", goal=goal, edit_status=edit_status)

    @app.route("/goal/<goal_id>/copy")
    @login_required
    def goal_copy(goal_id):
        from models import Goal, Milestone
        goal = Goal.objects.get_or_404(id=goal_id)
        if (goal.user.id == current_user.get_id()):
            abort(410)
        else:
            new_goal = Goal(title=goal.title, description=goal.description, user=current_user.self(), original=goal)
            new_goal.save()
            milestones = Milestone.objects(goal=goal.id)
            for milestone in milestones:
                new_milestone = Milestone(goal=new_goal, message=milestone.message)
                new_milestone.save()
            return redirect("/goal/%s" % new_goal.id)

    @app.route("/goal/<goal_id>/change_status")
    @login_required
    def goal_completed(goal_id):
        from models import Goal
        goal = Goal.objects.get_or_404(id=goal_id)
        if goal.user.id != goal.user.id or current_user.is_admin:
            abort(405)
        else:
            goal.status = request.args.get("status")
            if request.args.get("status") == "completed":
                goal.completed_at = datetime.datetime.now()
            goal.save()
            return redirect("/goal/%s" % goal_id)

    @app.route("/goal/new", methods=['GET', 'POST'])
    @login_required
    def goal_new():
        from models import Goal
        form = NewGoalForm(request.form)
        new_status = "form"
        if request.method == "POST":
            try:
                new_goal = Goal(title=form.title.data, user=current_user.self(), description=form.description.data)
                new_goal.save()
                new_status = "success"
            except OperationError:
                new_status = "fail"
        return render_template("goal/new.html", form=form, new_status=new_status)

    @app.route("/explore")
    def explore():
        # TODO: Generate logic to grab some popular goals
        return render_template("explore.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @api.register(name='users', url='/users/')
    class UserView(ResourceView):
        from models import UserResource
        resource = UserResource
        methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

    @api.register(name='goals', url='/goals/')
    class GoalView(ResourceView):
        from models import GoalResource
        resource = GoalResource
        methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

    @api.register(name='milestones', url='/milestones/')
    class MilestoneView(ResourceView):
        from models import MilestoneResource
        resource = MilestoneResource
        methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404
