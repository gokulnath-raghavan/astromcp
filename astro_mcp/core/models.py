from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Planet(str, Enum):
    SUN = "SUN"
    MOON = "MOON"
    MERCURY = "MERCURY"
    VENUS = "VENUS"
    MARS = "MARS"
    JUPITER = "JUPITER"
    SATURN = "SATURN"
    URANUS = "URANUS"
    NEPTUNE = "NEPTUNE"
    PLUTO = "PLUTO"

class Sign(str, Enum):
    ARIES = "ARIES"
    TAURUS = "TAURUS"
    GEMINI = "GEMINI"
    CANCER = "CANCER"
    LEO = "LEO"
    VIRGO = "VIRGO"
    LIBRA = "LIBRA"
    SCORPIO = "SCORPIO"
    SAGITTARIUS = "SAGITTARIUS"
    CAPRICORN = "CAPRICORN"
    AQUARIUS = "AQUARIUS"
    PISCES = "PISCES"

class House(int, Enum):
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

class AspectType(str, Enum):
    CONJUNCTION = "conjunction"
    SEXTILE = "sextile"
    SQUARE = "square"
    TRINE = "trine"
    OPPOSITION = "opposition"

class PlanetaryPosition(BaseModel):
    planet: Planet
    sign: Sign
    degree: float
    house: House
    retrograde: bool

class Aspect(BaseModel):
    planet1: Planet
    planet2: Planet
    aspect_type: AspectType
    orb: float
    degree: float

class TemporalCycle(BaseModel):
    cycle_length: int
    current_position: str

class ContextualLayer(BaseModel):
    temporal: Dict[str, TemporalCycle]
    spiritual: Dict[str, str]
    psychological: Dict[str, str]

class NatalChart(BaseModel):
    planetary_positions: List[PlanetaryPosition]
    aspects: List[Aspect]
    ascendant: Sign
    midheaven: Sign

class Interpretation(BaseModel):
    basic: Dict[str, str]
    temporal: Dict[str, str]
    spiritual: Dict[str, str]
    psychological: Dict[str, str] 