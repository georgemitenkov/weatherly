from random import choice, choices
from ..models.clothes import Clothes


class Suggestion:

    def __init__(self, suggestion):
        self.suggestion = suggestion


class Predictor:

    def __init__(self, weather_data):
        self.clothes = None
        self.weather_data = weather_data

    def filter_by_status(self):
        c = Clothes.query.filter(
            Clothes.min_temp <= self.weather_data.temperature.current,
            self.weather_data.temperature.current <= Clothes.max_temp
        )

        # printing queries
        print(c)

        status = self.weather_data.status.lower()
        filters = {
            "clear sky":
                 c.filter(Clothes.when_rain.is_(False), Clothes.when_snow.is_(False)),
            "few clouds":
                 c.filter(Clothes.when_rain.is_(False)),
            "overcast clouds":
                 c.filter(Clothes.when_rain.is_(False)),
            "scattered clouds":
                 c.filter(Clothes.when_rain.is_(False), Clothes.when_wind.is_(False), Clothes.when_snow.is_(False)),
            "broken clouds":
                 c.filter(Clothes.when_rain.is_(False)),
            "shower rain":
                c.filter(Clothes.when_rain.is_(True), Clothes.when_wind.is_(True)),
            "rain":
                 c.filter(Clothes.when_rain.is_(True)),
            "thunderstorm":
                 c.filter(Clothes.when_rain.is_(True), Clothes.when_wind.is_(True)),
            "snow":
                 c.filter(Clothes.when_snow.is_(True)),
            "mist":
                 c.filter(Clothes.when_rain.is_(False), Clothes.when_wind.is_(False), Clothes.when_snow.is_(False))
        }
        if status in filters:
            return filters[status]
        else:
            return c

    def predict(self):
        clothes = self.filter_by_status()
        if clothes.all():
            self.clothes = clothes.all()

    def suggest(self):

        def get_sentence(item):
            if item.when_snow:
                return "it's freezing"
            elif item.when_rain:
                return "it's  raining"
            elif item.when_wind:
                return "it's windy! {} m/s is not a joke".format(self.weather_data.wind.speed)
            else:
                return "and have a nice day!"

        if self.clothes is None:
            outfit = "Sorry, but it seems like your wardrobe doesn't have anything suitable for this weather." \
                     "Maybe you you should buy some new clothes?"
        else:
            accessoires = [p.name for p in self.clothes if p.is_accessoire]
            clothes = [p.name for p in self.clothes if not p.is_accessoire]
            if accessoires:
                item = choice(accessoires)
                answer = get_sentence(item)
                accs = "Lastly, do not forget your {}, {}!".format(item.name, answer)
            else:
                accs = "And last thing. Maybe it is better to stay at home these days?"

            if clothes:
                n = len(clothes)
                if n == 1:
                    ops = "You have a great option! Wear a {} to look cool " \
                          "and feel comfortable in this weather.".format(clothes[0])
                else:
                    outfits = ", ".join(choices(clothes, k=n))
                    ops = "Wow, you have {} options! You can wear {}. What will you pick?".format(n, outfits)
                cl = "{}".format(ops)
            else:
                cl = "Oops, looks like you don't have suitable clothes for this weather. But don't worry," \
                     " maybe you can buy some today?"
            outfit = "{} {}".format(cl, accs)
        return Suggestion(outfit)
