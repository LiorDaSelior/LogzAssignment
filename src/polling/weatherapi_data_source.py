import os

import requests
from dotenv import load_dotenv

from src.polling.abstract_data_source import AbstractDataSource
from src.weather_data import WeatherData

load_dotenv()

class WeatherApiDataSource(AbstractDataSource):
    API_KEY = os.getenv('WEATHERAPI_API_KEY', '')
    BASE_URL = "https://" + os.getenv('WEATHERAPI_CURRENT_WEATHER_ENDPOINT', "api.weatherapi.com/v1/current.json")

    def __init__(self, cities : list[str], polling_time : int):
        super().__init__(cities, polling_time, "weather_api")

    def poll_city(self, city: str) -> WeatherData:
        params = {
            "key": self.API_KEY,
            "q": city
        }
        res = requests.get(self.BASE_URL, params=params, timeout=5)
        res.raise_for_status()
        return self.transform_raw_data_to_weather_data(res.json(), city)

    def transform_raw_data_to_weather_data(self, data, city):
        data = data["current"]
        temperature = data["temp_c"]
        description = data["condition"]["text"]

        return WeatherData(
            city = city,
            temperature_celsius = temperature,
            description = description,
            source_provider = self.source_provider_name,
        )

if __name__ == "__main__":
    temp = WeatherApiDataSource(cities=["Berlin", "Sydney"], polling_time=1)
    print(temp.poll_city("Berlin"))