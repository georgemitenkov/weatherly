# Weatherly

Weatherly is a smart weather forecasst web application.
It allows user to find out the current weather conditions at specified location,
and suggests what to wear to feel comfortable outside. At the moment the available weather features are:
- Overall weather discription (e.g. Rain, Clear sky, etc.)
- Current temperature (average, minimum, maximum)
- Wind speed

## Stack
- Python 3
- Javascript
- [W3CSS](https://www.w3schools.com/w3css) for styling
- [SQLite](https://www.sqlite.org/index.html) for in memory data storage

## How it works

## Prerquisites
Make sure you have Python 3 installed on your machine

## Running the app
First, clone the repository to your machine. To use the service you will
need to get an API key from [OpenWeatherMap](https://openweathermap.org/current),
and place it app.py instead of API_KEY
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
Note that -- option is important for parsing negative numbers. See more info by running
```bash
flask insert --help
```
Finally, run
flask run        # Run the server
```
Then browse to <http://localhost:5000>.