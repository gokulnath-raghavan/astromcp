import swisseph as swe
from datetime import datetime
from typing import List, Dict, Tuple, Any
from .models import Planet, Sign, House, PlanetaryPosition, Aspect, AspectType

class SwissEphemerisCalculator:
    def __init__(self):
        """Initialize Swiss Ephemeris calculator."""
        swe.set_ephe_path(None)  # Use default ephemeris path
        self.planet_map = {
            Planet.SUN: swe.SUN,
            Planet.MOON: swe.MOON,
            Planet.MERCURY: swe.MERCURY,
            Planet.VENUS: swe.VENUS,
            Planet.MARS: swe.MARS,
            Planet.JUPITER: swe.JUPITER,
            Planet.SATURN: swe.SATURN,
            Planet.URANUS: swe.URANUS,
            Planet.NEPTUNE: swe.NEPTUNE,
            Planet.PLUTO: swe.PLUTO
        }
        self.sign_map = {
            0: Sign.ARIES,
            1: Sign.TAURUS,
            2: Sign.GEMINI,
            3: Sign.CANCER,
            4: Sign.LEO,
            5: Sign.VIRGO,
            6: Sign.LIBRA,
            7: Sign.SCORPIO,
            8: Sign.SAGITTARIUS,
            9: Sign.CAPRICORN,
            10: Sign.AQUARIUS,
            11: Sign.PISCES
        }

    def _datetime_to_jd(self, dt: datetime) -> float:
        """Convert datetime to Julian Day."""
        return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 + dt.second/3600.0)

    def _calculate_house_cusps(self, jd: float, latitude: float, longitude: float) -> List[float]:
        """Calculate house cusps using Placidus system."""
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
        return cusps

    def calculate_ascendant(self, birth_time: datetime, latitude: float, longitude: float) -> Sign:
        """Calculate the ascendant sign."""
        jd = self._datetime_to_jd(birth_time)
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
        asc_deg = ascmc[0]  # Ascendant is first element
        sign_num = int(asc_deg / 30)
        return self.sign_map[sign_num]

    def calculate_midheaven(self, birth_time: datetime, latitude: float, longitude: float) -> Sign:
        """Calculate the midheaven sign."""
        jd = self._datetime_to_jd(birth_time)
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
        mc_deg = ascmc[1]  # Midheaven is second element
        sign_num = int(mc_deg / 30)
        return self.sign_map[sign_num]

    def calculate_planetary_positions(self, birth_time: datetime, latitude: float, longitude: float) -> List[PlanetaryPosition]:
        """Calculate positions of all planets."""
        jd = self._datetime_to_jd(birth_time)
        cusps = self._calculate_house_cusps(jd, latitude, longitude)
        positions = []

        for planet, swe_planet in self.planet_map.items():
            try:
                xx, ret = swe.calc_ut(jd, swe_planet, flags=swe.SEFLG_SPEED)
                if not xx:  # Check if calculation failed
                    continue

                longitude = xx[0] % 360
                speed = xx[3]
                sign_num = int(longitude / 30)
                house_num = self._get_house_number(longitude, cusps)

                positions.append(PlanetaryPosition(
                    planet=planet,
                    sign=self.sign_map[sign_num],
                    degree=longitude % 30,
                    house=House(house_num),
                    retrograde=speed < 0
                ))
            except Exception as e:
                print(f"Error calculating position for {planet}: {str(e)}")
                continue

        return positions

    def _get_house_number(self, longitude: float, cusps: List[float]) -> int:
        """Determine house number based on longitude and house cusps."""
        for i in range(12):
            if cusps[i] <= longitude < cusps[(i + 1) % 12]:
                return i + 1
        return 1  # Default to first house if not found

    def calculate_aspects(self, positions: List[PlanetaryPosition]) -> List[Aspect]:
        """Calculate aspects between planets."""
        aspects = []
        orb = 8.0  # Orb of influence in degrees

        for i, pos1 in enumerate(positions):
            for pos2 in positions[i+1:]:
                angle = abs(pos1.degree - pos2.degree)
                if angle > 180:
                    angle = 360 - angle

                if angle <= orb:
                    aspects.append(Aspect(
                        planet1=pos1.planet,
                        planet2=pos2.planet,
                        aspect_type=AspectType.CONJUNCTION,
                        orb=angle,
                        degree=angle
                    ))

        return aspects

    def get_nakshatra(self, moon_degree: float) -> str:
        """Get Nakshatra name based on Moon's degree."""
        nakshatra_num = int(moon_degree / 13.333333)  # Each Nakshatra is 13°20'
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        return nakshatras[nakshatra_num]

    def get_nakshatra_pada(self, moon_degree: float) -> int:
        """Get Nakshatra pada based on Moon's degree."""
        return int((moon_degree % 13.333333) / 3.333333) + 1 