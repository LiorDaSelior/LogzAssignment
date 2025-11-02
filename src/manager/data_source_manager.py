import json
import os

import requests
from dotenv import load_dotenv

from src.data_source import DATA_SOURCE_CLASSES, AbstractDataSource
from typing import Generator, Dict, List

from src.weather_data import WeatherData

load_dotenv()

class DataSourceManager:
    LOGZ_API_ENDPOINT = os.getenv("LOGZ_API_ENDPOINT")
    LOGZ_TOKEN = os.getenv("LOGZ_API_TOKEN")

    def __init__(self, source_city_map: Dict[str, List[str]], polling_time: int = 60):
        self.filtered_map = self._filter_sources(source_city_map)
        self.polling_time = polling_time
        self.sources: List[AbstractDataSource] = []

    def _filter_sources(self, source_city_map) -> Dict[str, List[str]]:
        self.filtered_map = {
            provider: cities
            for provider, cities in source_city_map.items()
            if provider in DATA_SOURCE_CLASSES
        }
        return self.filtered_map

    def _create_sources(self) -> List[AbstractDataSource]:
        self.sources = [
            DATA_SOURCE_CLASSES[provider](cities, self.polling_time)
            for provider, cities in self.filtered_map.items()
        ]
        return self.sources

    def _poll_all(self) -> Generator:
        for source in self.sources:
            yield from source.poll()

    def start(self):
        self._create_sources()
        for weather_data in self._poll_all():
            self._send_to_endpoint(weather_data)

    def _send_to_endpoint(self, weather_data : WeatherData):
        headers = {"Content-Type": "application/json"}
        json_str = json.dumps(weather_data.__dict__)
        try:
            response = requests.post(
                f"https://{self.LOGZ_API_ENDPOINT}?token={self.LOGZ_TOKEN}",
                headers=headers,
                data=json_str + "\n"  # newline-delimited per spec
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send data for {weather_data.city}: {e}")