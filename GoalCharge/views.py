from flask import (current_app, render_template, request, redirect, url_for)
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest import methods
from flask.ext.login import (login_required, current_user, login_user,
        logout_user)
from mongoengine.queryset import DoesNotExist, NotUniqueError
from GoalCharge import (api, login_manager)
from GoalCharge.forms import (LoginForm, RegisterForm)

def init(app):
    @app.route("/")
    def index():
        # TODO: Generate logic for homepage data, whatever it may be
        return render_template("index.html")

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        from GoalCharge.models import User
        form = LoginForm(request.form)
        login_status = "form"
        if request.method == "POST":
            #if form.validate_on_submit():
                try:
                    user = User.objects.get(username=form.username.data,
                            password=form.password.data)
                    login_user(user)
                    login_status = "success"
                    return redirect(url_for("index"))
                except DoesNotExist:
                    login_status = "fail"
            #else:
                #login_status = "fail"
        return render_template("login.html", login_status=login_status, form=form)

    @app.route("/logout")
    def logout():
        # TODO: Logout logic
        # Send back to the page the user was at? Just back to index for now
        logout_user()
        return redirect(url_for("index"))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        from models import User
        form = RegisterForm(request.form)
        register_status = "form"
        if request.method == "POST":
            try:
                new_user = User(username=form.username.data,email=form.email.data,password=form.password.data)
                new_user.save()
                register_status = "success"
            except NotUniqueError:
                register_status = "fail"
        return render_template("register.html", register_status=register_status, form=form)

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

#    @app.route("/user/account", methods=['GET', 'POST'])
    #@login_required
#    def user_account():
        # TODO: Edit user account stuff
#        return render_template("user/account.html")

#    @app.route("/user/<username>")
#    def user_user(username):
        # TODO: Logic to grab user info and add push to profile page
#        from GoalCharge.models import User
#        user = User.objects.get_or_404(username=username)
#        return render_template("user/user.html", user=user)

