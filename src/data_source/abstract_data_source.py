import time
from abc import ABC, abstractmethod
from typing import Any, Generator

from src.weather_data import WeatherData

class PollingError(Exception):
    """Custom exception for invalid polling."""
    pass

class AbstractDataSource(ABC):
    SOURCE_PROVIDER_NAME = "undefined"

    def __init__(self, cities : list[str], polling_time : float):
        self.cities = cities
        self.polling_time = polling_time

    @abstractmethod
    def poll_city(self, city : str) -> WeatherData:
        pass

    def poll(self) -> Generator[WeatherData, Any, None]:
        while True:
            for city in self.cities:
                try:
                    yield self.poll_city(city)
                except PollingError as e:
                    print(f"PollingError: {e}")
                    continue
            time.sleep(self.polling_time)