class Metric:
    pass


class WeatherData:

    def __init__(self, location, temperature, wind):
        self.location = location
        self.temperature = temperature
        self.wind = wind


class Location:

    def __init__(self, name):
        self.name = name


class Temperature(Metric):

    def __init__(self, current, min, max, unit):
        self.current = current
        self.min = min
        self.max = max
        self.unit = unit


class Wind(Metric):

    def __init__(self, speed):
        self.speed = speed
