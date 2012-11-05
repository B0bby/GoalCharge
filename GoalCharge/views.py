from flask import (current_app, render_template, request)
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest import methods
from GoalCharge import api
from GoalCharge.forms import (LoginForm, RegisterForm)

def init(app):
    @app.route("/")
    def index():
        # TODO: Generate logic for homepage data, whatever it may be
        return render_template("index.html")

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        # TODO: WTForm
        form = LoginForm(request.form)
        login_status = "form"
        if request.method == "POST":
            if form.validate():
                login_status = "success"
            else:
                login_statue = "fail"
        return render_template("login.html", login_status=login_status, form=form)

    @app.route("/logout")
    def logout():
        # TODO: Logout logic
        # Send back to the page the user was at? Just back to index for now
        return index()

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        register_status = "form"
        if request.method == "POST":
            if form.validated():
                register_status = "success"
            else:
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

