# Weatherly

Weatherly is a smart weather forecast web application.
It allows user to find out the current weather conditions at specified location,
and suggests what to wear to feel comfortable outside. At the moment the available weather features are:
- Overall weather discription (e.g. Rain, Clear sky, etc.)
- Current temperature (average, minimum, maximum)
- Wind speed
The location search is based on the city, state or country. (ZIPs and coordinates are currently unsupported).

## Stack
- Python 3
- Javascript
- [W3CSS](https://www.w3schools.com/w3css) for styling
- [SQLite](https://www.sqlite.org/index.html) for in memory data storage

## APIs and libraries
This service uses [pyowm](https://pyowm.readthedocs.io/en/latest/) - a Python wrapper around
[OpenWeatherMap](https://openweathermap.org/current) APIs to get the weather data at specific locations.
[Click](https://click.palletsprojects.com/en/7.x/) is used to create a simple command line interface, so 
that it is easier to interact with the application.

## How it works
### Workflow
The workflow of the application is simple. 
1. User enters a location at which s/he wants to find out the current weather conditions.
2. Location is interpreted via `pyowm` to return an Observation object
3. Observation object is parsed to extract useful data via `Parser` class
4. `Predictor` class makes suggestions based on the weather data.
5. Weather information and suggestions are passed to the rendered page.

### Prediction algorithm
`Predict` class uses a simple suggestion algorithm. In database, it searches clothes and accessoires that
mach the current temperature and are suitable for current weather conditions(i.e. rain, snow, etc.)

## Prerquisites
Make sure you have Python 3 installed on your machine

## Running the app
First, clone the repository to your machine. To use the service you will
need to get an API key from [OpenWeatherMap](https://openweathermap.org/current),
and place it in app.py instead of API_KEY.
```Python
owm = pyowm.OWM(API_KEY)
```
To run the app, first run
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask create_all # Create database and tables inside it
```
Additionally, you may want to populate the database with some random initial data. Then run
```bash
flask populate
```
To insert your own piece of clothes in the database, run
```bash
flask insert -- NAME MIN_TEMP MAX_TEMP WHEN_RAIN WHEN_SNOW WHEN_WIND IS_ACCESSOIRE
```
Note that `--` option is important for parsing negative numbers. See more info by running
```bash
flask insert --help
```
Finally, run
```bash
flask run        # Run the server
```
Then browse to `<http://localhost:5000>`.

## Example
[Here](https://youtu.be/RtpOirGGQPU) is the video example
