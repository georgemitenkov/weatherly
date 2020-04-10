from flask import Flask, render_template, request
from parser import Parser
from predictor import Predictor
from models.clothes import Clothes
from database import database
import pyowm
import config


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clothes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database.init_app(app)


@app.route("/")
def index():
    create_all()
    populate()
    return render_template("index.html")


@app.route("/weather", methods=["GET", "POST"])
def weather():
    if request.method == "POST":
        owm = pyowm.OWM(config.API_KEY)
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


def create_all():
    database.create_all()


def populate():
    initial_clothes = [
        Clothes(
            name="t-shirt",
            min_temp=0,
            max_temp=40
        ),
        Clothes(
            name="sweater",
            min_temp=-20,
            max_temp=10
        ),
        Clothes(
            name="shirt",
            min_temp=-10,
            max_temp=20
        ),
        Clothes(
            name="raincoat",
            min_temp=0,
            max_temp=10,
            when_rain=True,
            when_wind=True
        ),
        Clothes(
            name="overcoat",
            min_temp=-5,
            max_temp=10,
            when_rain=True,
            when_wind=True
        ),
        Clothes(
            name="denim jacket",
            min_temp=10,
            max_temp=20
        ),
        Clothes(
            name="hoodie",
            min_temp=5,
            max_temp=15,
            when_wind=True
        ),
        Clothes(
            name="winter coat",
            min_temp=-20,
            max_temp=0,
            when_snow=True,
            when_wind=True
        ),
        Clothes(
            name="umbrella",
            when_rain=True,
            when_snow=False,
            when_wind=False,
            is_accessoire=True
        ),
        Clothes(
            name="gloves",
            min_temp=-20,
            max_temp=0,
            when_rain=False,
            when_snow=True,
            when_wind=False,
            is_accessoire=True
        ),
        Clothes(
            name="hat",
            when_rain=True,
            when_snow=True,
            when_wind=False,
            is_accessoire=True
        )
    ]
    for clothes in initial_clothes:
        database.session.add(clothes)
    database.session.commit()

if __name__ == "__main__":
    app.debug = True
    app.run()
