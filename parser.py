from weather_data import Location, Temperature, Wind, WeatherData


class Parser:

    def parse(self, observation):
        weather_data = observation.get_weather()
        location = observation.get_location()
        loc = Location(location.get_name())
        main = weather_data.get_temperature(unit='celsius')
        temperature = Temperature(float(main["temp"]), float(main["temp_min"]),
                                  float(main["temp_max"]),
                                  "Celsius")
        wind = Wind(float(weather_data.get_wind()["speed"]))
        return WeatherData(loc, temperature, wind)
