from dataclasses import dataclass

@dataclass
class WeatherData:
    city: str
    temperature_celsius: float
    description: str
    source_provider: str