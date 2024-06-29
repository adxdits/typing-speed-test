from flask import Blueprint, render_template, session, request, redirect, url_for
from src.models import User, Score
from src.decorators import login_required, not_login_required

template_bp = Blueprint('template', __name__)

@template_bp.route('/')
@login_required
def home():

    user = User.get(User.username == session["username"])

    return render_template("dashboard.html", user=user)

@template_bp.route('/type/')
@login_required
def type():

    user = User.get(User.username == session["username"])

    return render_template("type.html", user=user)


@template_bp.route('/history/', methods=["GET", "POST"])
@login_required
def history():

    user = User.get(User.username == session["username"])

    if request.method == "POST":

        if request.form.get("score"):

            score = int(request.form.get("score"))


            Score.create(user=user, value=score)

    history = Score.select().where(Score.user == user).order_by(Score.date.desc())

    return render_template("history.html", user=user, history=history)



@template_bp.route('/register/', methods=["GET", "POST"])
@not_login_required
def register():

    """
    On check d'abord
    """

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        is_created = User.create_user(username, password)

        if is_created:

            print("User created")
            session["username"] = username

            return redirect(url_for("template.home"))

        else:
            print("User not created")

    return render_template("register.html")


@template_bp.route('/login/', methods=["GET", "POST"])
@not_login_required
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.get_or_none(User.username == username)

        if user:

            if user.check_password(password):

                session["username"] = username

                return redirect(url_for("template.home"))
            else:
                return render_template("login.html", error="Mot de passe incorrect")
        else:
            return render_template("login.html", error="Utilisateur non trouvé")

    return render_template("login.html", error=None)