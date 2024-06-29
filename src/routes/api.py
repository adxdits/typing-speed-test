from flask import Blueprint
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from src.models import User, Score
from src.decorators import login_required
import requests, json

api_bp = Blueprint('api', __name__)
@login_required
@api_bp.route('/api/score/', methods=['GET', 'POST'])
def score():
    if request.method == "POST":

        # Get the value from the request body (JSON)
        value = request.json.get("score")
        user = User.get(User.username == session["username"])
        Score.create(user=user, value=value)

        return {"success": True}
    else:
        scores = Score.select().where(Score.user == User.get(User.username == session["username"]))
        return jsonify([{"value": score.value, "date": score.date} for score in scores])

@login_required
@api_bp.route('/api/words/', methods=['GET'])
def get_words():

    # Liste par défaut si l'api mistral ne fonctionne pas, ou si le résultat n'est pas au bon format
    return [
        "ruby",
        "dynamic",
        "ocean",
        "lettuce",
        "collect",
        "journey",
        "despair",
        "metal",
        "together",
        "insect",
        "choose",
        "pasta",
        "elephant",
        "thrilling",
        "soldier",
        "couch",
        "laugh",
        "vapor",
        "opera",
        "raccoon",
        "collide",
        "comfort",
        "enchant",
        "cactus",
        "incredible",
        "frog",
        "nominate",
        "explode",
        "receive",
        "wander",
        "admit",
        "gender",
        "terrible",
        "cosmic",
        "kingdom",
        "salad",
        "cheese",
        "pottery",
        "atmosphere",
        "essential",
        "efficient",
        "angry",
        "observe",
        "moon",
        "squirrel",
        "revise",
        "introduce",
        "umbrella",
        "owl",
        "lizard"
    ]