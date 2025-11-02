import os

import requests
from dotenv import load_dotenv

from src.data_source.abstract_data_source import AbstractDataSource
from src.weather_data import WeatherData

load_dotenv()

class OpenWeatherDataSource(AbstractDataSource):
    API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    BASE_URL = "https://" + os.getenv('OPENWEATHER_CURRENT_WEATHER_ENDPOINT', "https://api.openweathermap.org/data/2.5/weather")
    SOURCE_PROVIDER_NAME = "open_weather"

    def __init__(self, cities : list[str], polling_time : int):
        super().__init__(cities, polling_time)

    def poll_city(self, city: str) -> WeatherData:
        params = {
            "appid": self.API_KEY,
            "q": city,
            "units": "metric"
        }
        res = requests.get(self.BASE_URL, params=params, timeout=5)
        res.raise_for_status()
        return self.transform_raw_data_to_weather_data(res.json(), city)

    def transform_raw_data_to_weather_data(self, data, city):
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        return WeatherData(
            city = city,
            temperature_celsius = temperature,
            description = description,
            source_provider = self.SOURCE_PROVIDER_NAME,
        )

if __name__ == "__main__":
    temp = OpenWeatherDataSource(cities=["Berlin", "Sydney"], polling_time=1)
    print(temp.poll_city("Berlin"))