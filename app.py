from flask import Flask, render_template, request
from .parser import Parser
from .predictor import Predictor
from .config import API_KEY
from .database import database
import pyowm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clothes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_app(app)

from .cli import create_all, drop_all, populate

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["GET", "POST"])
def weather():
    if request.method == "POST":
        owm = pyowm.OWM(API_KEY)
        place = request.form["location"]
        if place:
            try:
                obs = owm.weather_at_place(place)
                parser = Parser()
                weather_data = parser.parse(obs)
                predictor = Predictor(weather_data)
                predictor.predict()
                suggestion = predictor.suggest()
                return render_template("weather.html", weather_data=weather_data, suggestion=suggestion)
            except pyowm.exceptions.api_response_error.NotFoundError:
                return render_template("error.html",
                                       error="Looks like your location doesn't exist. Maybe try again?")
        return render_template("error.html", error="Looks like you haven't selected the location. Maybe try again?")


if __name__ == "__main__":
    app.debug = True
    app.run()
