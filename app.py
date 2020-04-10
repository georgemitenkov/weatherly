from flask import Flask, render_template
from parser import Parser
import pyowm, config


app = Flask(__name__)
API_KEY = "db3ea29ae4e03bea2930bc2588a77e6b"


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/weather", methods=["GET"])
def weather():
    owm = pyowm.OWM(config.API_KEY)
    obs = owm.weather_at_place('London,GB')
    parser = Parser()
    weather_data = parser.parse(obs)
    return render_template("weather.html", weather_data=weather_data)


if __name__ == "__main__":
    app.debug = True
    app.run()
