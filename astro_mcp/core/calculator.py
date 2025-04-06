from datetime import datetime
from typing import List, Dict, Tuple, Any
from .models import Planet, ZodiacSign, House, PlanetaryPosition, Aspect, NatalChart
from .astrologyapi_client import AstrologyAPIClient

class AstroCalculator:
    def __init__(self, user_id: str, api_key: str):
        self.client = AstrologyAPIClient(user_id, api_key)
        self.planets = {
            Planet.SUN: "sun",
            Planet.MOON: "moon",
            Planet.MERCURY: "mercury",
            Planet.VENUS: "venus",
            Planet.MARS: "mars",
            Planet.JUPITER: "jupiter",
            Planet.SATURN: "saturn",
            Planet.URANUS: "uranus",
            Planet.NEPTUNE: "neptune",
            Planet.PLUTO: "pluto"
        }

    def calculate_planetary_positions(self, 
                                   birth_time: datetime,
                                   latitude: float,
                                   longitude: float) -> List[PlanetaryPosition]:
        """Calculate planetary positions using AstrologyAPI."""
        chart = self.client.get_natal_chart(birth_time, latitude, longitude)
        return chart.planetary_positions

    def calculate_aspects(self, positions: List[PlanetaryPosition]) -> List[Aspect]:
        """Calculate aspects between planets using AstrologyAPI."""
        chart = self.client.get_natal_chart(
            positions[0].birth_time,
            positions[0].birth_location["latitude"],
            positions[0].birth_location["longitude"]
        )
        return chart.aspects

    def generate_natal_chart(self,
                           birth_time: datetime,
                           latitude: float,
                           longitude: float) -> NatalChart:
        """Generate a complete natal chart using AstrologyAPI."""
        return self.client.get_natal_chart(birth_time, latitude, longitude)
    
    def get_tamil_horoscope(self,
                          birth_time: datetime,
                          latitude: float,
                          longitude: float) -> Dict[str, Any]:
        """Get Tamil horoscope details."""
        return self.client.get_tamil_horoscope(birth_time, latitude, longitude)
    
    def get_nakshatra_details(self,
                            birth_time: datetime,
                            latitude: float,
                            longitude: float) -> Dict[str, Any]:
        """Get Nakshatra details."""
        return self.client.get_nakshatra_details(birth_time, latitude, longitude) 