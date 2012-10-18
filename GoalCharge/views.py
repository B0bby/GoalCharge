from flask import (current_app, render_template, request)
#from GoalCharge.models import (User, Goal)

def init(app):
    @app.route("/")
    def index():
        # TODO: Generate logic for homepage data, whatever it may be
        return render_template("index.html")

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        # TODO: WTForm
        login_status = "form"
        if request.method == "POST":
            login_status = "success"
        return render_template("login.html", login_status=login_status)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        # TODO: WTForm
        register_status = "form"
        if request.method == "POST":
            register_status = "success"
        return render_template("register.html", register_status=register_status)

    @app.route("/explore")
    def explore():
        # TODO: Generate logic to grab some popular goals
        return render_template("explore.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/user/account", methods=['GET', 'POST'])
    #@login_required
    def user_account():
        # TODO: Edit user account stuff
        return render_template("user/account.html")

    @app.route("/user/<username>")
    def user_user(username):
        # TODO: Logic to grab user info and add push to profile page
        """user = User(username)"""
        return render_template("user/user.html")

