from abc import ABC, abstractmethod
from typing import Any, Generator

from src.weather_data import WeatherData


class AbstractDataSource(ABC):
    SOURCE_PROVIDER_NAME = "undefined"

    def __init__(self, cities : list[str], polling_time : float):
        self.cities = cities
        self.polling_time = polling_time

    @abstractmethod
    def poll_city(self, city : str) -> WeatherData:
        pass

    def poll(self) -> Generator[WeatherData, Any, None]:
        for city in self.cities:
            yield self.poll_city(city)
