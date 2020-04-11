from random import choice
from .models.clothes import Clothes


class Suggestion:

    def __init__(self, clothes, accessoire):
        self.clothes = clothes
        self.accessoire = accessoire


class Predictor:

    def __init__(self, weather_data):
        self.clothes = None
        self.accessoire = None
        self.weather_data = weather_data

    def filter_by_status(self):
        a = Clothes.query.filter(
            Clothes.min_temp <= 15,
            15 <= Clothes.max_temp,
            Clothes.is_accessoire.is_(True)
        )
        c = Clothes.query.filter(
            Clothes.min_temp <= self.weather_data.temperature.current,
            self.weather_data.temperature.current <= Clothes.max_temp,
            Clothes.is_accessoire.is_(False)
        )

        # printing queries
        print(c)
        print(self.weather_data.temperature.current)
        print(a)

        status = self.weather_data.status.lower()
        filters = {
            "clear sky":
                (a.filter(Clothes.when_rain.is_(False), Clothes.when_snow.is_(False)),
                 c.filter(Clothes.when_rain.is_(False), Clothes.when_snow.is_(False))
                 ),
            "few clouds":
                (a.filter(Clothes.when_rain.is_(False)),
                 c.filter(Clothes.when_rain.is_(False))
                 ),
            "overcast clouds":
                (a.filter(Clothes.when_rain.is_(False)),
                 c.filter(Clothes.when_rain.is_(False))
                 ),
            "scattered clouds":
                (a.filter(Clothes.when_rain.is_(False), Clothes.when_wind.is_(False), Clothes.when_snow.is_(False)),
                 c.filter(Clothes.when_rain.is_(False), Clothes.when_wind.is_(False), Clothes.when_snow.is_(False))
                 ),
            "broken clouds":
                (a.filter(Clothes.when_rain.is_(False)),
                 c.filter(Clothes.when_rain.is_(False))
                 ),
            "shower rain":
                (a.filter(Clothes.when_rain.is_(True), Clothes.when_wind.is_(True)),
                 c.filter(Clothes.when_rain.is_(True), Clothes.when_wind.is_(True))
                 ),
            "rain":
                (a.filter(Clothes.when_rain.is_(True)),
                 c.filter(Clothes.when_rain.is_(True))
                 ),
            "thunderstorm":
                (a.filter(Clothes.when_rain.is_(True), Clothes.when_wind.is_(True)),
                 c.filter(Clothes.when_rain.is_(True), Clothes.when_wind.is_(True))
                 ),
            "snow":
                (a.filter(Clothes.when_snow.is_(True)),
                 c.filter(Clothes.when_snow.is_(True))
                 ),
            "mist":
                (a.filter(Clothes.when_rain.is_(False), Clothes.when_wind.is_(False), Clothes.when_snow.is_(False)),
                 c.filter(Clothes.when_rain.is_(False), Clothes.when_wind.is_(False), Clothes.when_snow.is_(False))
                 )
        }
        if status in filters:
            return filters[status]
        else:
            return a, c

    def predict(self):
        accessoires, clothes = self.filter_by_status()
        if clothes.all():
            self.clothes = choice(clothes.all()).name
        if accessoires.all():
            self.accessoire = choice(accessoires.all()).name

    def suggest(self):
        if self.clothes is None:
            return Suggestion(
                "There are so many things you can wear on this day! Have a think yourself :)",
                "Don't forget to take yor pet with you!"
            )
        else:
            if self.accessoire is None:
                return Suggestion(
                    "Today is perfect for a {}, try it!".format(self.clothes),
                    "Maybe it is time to look closely at your wardrobe?"
                )
            else:
                return Suggestion(
                    "Maybe wear a {}?".format(self.clothes),
                    "Obviously do not forget your {}!".format(self.accessoire)
                )

