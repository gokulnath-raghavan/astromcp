from datetime import datetime
from typing import List, Dict, Tuple, Any
from .models import Planet, Sign, House, PlanetaryPosition, Aspect, NatalChart
from .swiss_ephemeris_calculator import SwissEphemerisCalculator

class AstroCalculator:
    def __init__(self):
        """Initialize the astrological calculator."""
        self.calculator = SwissEphemerisCalculator()

    def calculate_planetary_positions(self, birth_time: datetime, latitude: float, longitude: float) -> List[PlanetaryPosition]:
        """Calculate planetary positions for the given birth time and location."""
        return self.calculator.calculate_planetary_positions(birth_time, latitude, longitude)

    def calculate_aspects(self, positions: List[PlanetaryPosition]) -> List[Aspect]:
        """Calculate aspects between planets."""
        return self.calculator.calculate_aspects(positions)

    def generate_natal_chart(self, birth_time: datetime, latitude: float, longitude: float) -> NatalChart:
        """Generate a complete natal chart."""
        positions = self.calculate_planetary_positions(birth_time, latitude, longitude)
        aspects = self.calculate_aspects(positions)
        ascendant = self.calculator.calculate_ascendant(birth_time, latitude, longitude)
        midheaven = self.calculator.calculate_midheaven(birth_time, latitude, longitude)
        
        return NatalChart(
            planetary_positions=positions,
            aspects=aspects,
            ascendant=ascendant,
            midheaven=midheaven
        )

    def get_tamil_horoscope(self, chart: NatalChart) -> Dict[str, Any]:
        """Generate Tamil horoscope details from the natal chart."""
        return {
            "planets": [
                {
                    "name": pos.planet.value,
                    "sign": pos.sign.value,
                    "degree": pos.degree,
                    "house": pos.house.value,
                    "retrograde": pos.retrograde
                }
                for pos in chart.planetary_positions
            ],
            "ascendant": chart.ascendant.value,
            "midheaven": chart.midheaven.value,
            "aspects": [
                {
                    "planet1": aspect.planet1.value,
                    "planet2": aspect.planet2.value,
                    "type": aspect.aspect_type.value,
                    "orb": aspect.orb,
                    "degree": aspect.degree
                }
                for aspect in chart.aspects
            ]
        }

    def get_nakshatra_details(self, chart: NatalChart) -> Dict[str, Any]:
        """Get Nakshatra details from the chart."""
        moon_position = next(pos for pos in chart.planetary_positions if pos.planet == Planet.MOON)
        nakshatra = self.calculator.get_nakshatra(moon_position.degree)
        pada = self.calculator.get_nakshatra_pada(moon_position.degree)
        
        return {
            "nakshatra": nakshatra,
            "pada": pada,
            "moon_degree": moon_position.degree,
            "moon_sign": moon_position.sign.value
        } 