from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Planet(Enum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"

class ZodiacSign(Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

class House(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
    ELEVENTH = 11
    TWELFTH = 12

class PlanetaryPosition(BaseModel):
    planet: Planet
    sign: ZodiacSign
    degree: float
    house: House
    retrograde: bool = False

class Aspect(BaseModel):
    planet1: Planet
    planet2: Planet
    aspect_type: str  # conjunction, opposition, trine, etc.
    orb: float
    exact_degree: float

class NatalChart(BaseModel):
    birth_time: datetime
    birth_location: Dict[str, float]  # latitude, longitude
    planetary_positions: List[PlanetaryPosition]
    aspects: List[Aspect]
    ascendant: ZodiacSign
    midheaven: ZodiacSign
    additional_context: Optional[Dict[str, Any]] = None

class ContextualLayer(BaseModel):
    psychological: Optional[Dict[str, float]] = None
    cultural: Optional[Dict[str, str]] = None
    temporal: Optional[Dict[str, datetime]] = None

class Interpretation(BaseModel):
    planetary_interpretation: Dict[Planet, str]
    aspect_interpretation: Dict[str, str]
    house_interpretation: Dict[House, str]
    contextual_insights: ContextualLayer 