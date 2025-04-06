import requests
from typing import Dict, Any
from datetime import datetime
from .models import NatalChart, PlanetaryPosition, Aspect, ZodiacSign, House, Planet

class ProkeralaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.prokerala.com/v2/astrology"
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to Prokerala API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=headers,
            json=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_natal_chart(self, 
                       birth_time: datetime,
                       latitude: float,
                       longitude: float,
                       timezone: str = "UTC") -> NatalChart:
        """Get natal chart data from Prokerala API."""
        params = {
            "datetime": birth_time.isoformat(),
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": timezone
        }
        
        response = self._make_request("natal-chart", params)
        data = response["data"]
        
        # Convert Prokerala response to our NatalChart model
        planetary_positions = []
        for planet_data in data["planets"]:
            position = PlanetaryPosition(
                planet=Planet[planet_data["name"].upper()],
                sign=ZodiacSign[planet_data["sign"].upper()],
                degree=float(planet_data["degree"]),
                house=House(int(planet_data["house"])),
                retrograde=planet_data.get("retrograde", False)
            )
            planetary_positions.append(position)
        
        # Convert aspects
        aspects = []
        for aspect_data in data.get("aspects", []):
            aspect = Aspect(
                planet1=Planet[aspect_data["planet1"].upper()],
                planet2=Planet[aspect_data["planet2"].upper()],
                aspect_type=aspect_data["type"].lower(),
                orb=float(aspect_data["orb"]),
                exact_degree=float(aspect_data["degree"])
            )
            aspects.append(aspect)
        
        return NatalChart(
            birth_time=birth_time,
            birth_location={"latitude": latitude, "longitude": longitude},
            planetary_positions=planetary_positions,
            aspects=aspects,
            ascendant=ZodiacSign[data["ascendant"]["sign"].upper()],
            midheaven=ZodiacSign[data["midheaven"]["sign"].upper()]
        )
    
    def get_planetary_positions(self,
                              start_time: datetime,
                              end_time: datetime,
                              interval_hours: int = 24,
                              latitude: float = 0.0,
                              longitude: float = 0.0) -> Dict[str, Any]:
        """Get planetary positions over a time period."""
        params = {
            "start_datetime": start_time.isoformat(),
            "end_datetime": end_time.isoformat(),
            "interval": f"{interval_hours}h",
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            }
        }
        
        return self._make_request("planetary-positions", params)
    
    def get_aspects(self,
                   planet1: str,
                   planet2: str,
                   start_time: datetime,
                   end_time: datetime,
                   orb: float = 8.0) -> Dict[str, Any]:
        """Get aspects between two planets over a time period."""
        params = {
            "planet1": planet1,
            "planet2": planet2,
            "start_datetime": start_time.isoformat(),
            "end_datetime": end_time.isoformat(),
            "orb": orb
        }
        
        return self._make_request("aspects", params) 