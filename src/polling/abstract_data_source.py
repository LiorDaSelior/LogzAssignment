from abc import ABC, abstractmethod
from typing import Any, Generator

from src.weather_data import WeatherData


class AbstractDataSource(ABC):
    def __init__(self, cities : list[str], polling_time : float, source_provider_name : str):
        self.source_provider_name = source_provider_name
        self.cities = cities
        self.polling_time = polling_time

    @abstractmethod
    def poll_city(self, city : str) -> WeatherData:
        pass

    def poll(self) -> Generator[WeatherData, Any, None]:
        for city in self.cities:
            yield self.poll_city(city)
