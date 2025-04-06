from typing import Dict, List
from .models import (
    NatalChart, Interpretation, ContextualLayer,
    Planet, House, Aspect, PlanetaryPosition
)

class ContextualInterpreter:
    def __init__(self):
        self.psychological_archetypes = {
            Planet.SUN: "Core identity and ego",
            Planet.MOON: "Emotional self and instincts",
            Planet.MERCURY: "Communication and thought patterns",
            Planet.VENUS: "Values and relationship style",
            Planet.MARS: "Action and assertion",
            Planet.JUPITER: "Growth and expansion",
            Planet.SATURN: "Structure and limitations",
            Planet.URANUS: "Innovation and change",
            Planet.NEPTUNE: "Intuition and spirituality",
            Planet.PLUTO: "Transformation and power"
        }
        
        self.house_meanings = {
            House.FIRST: "Self and appearance",
            House.SECOND: "Values and resources",
            House.THIRD: "Communication and siblings",
            House.FOURTH: "Home and family",
            House.FIFTH: "Creativity and romance",
            House.SIXTH: "Health and service",
            House.SEVENTH: "Partnerships",
            House.EIGHTH: "Transformation and shared resources",
            House.NINTH: "Philosophy and travel",
            House.TENTH: "Career and public image",
            House.ELEVENTH: "Friends and groups",
            House.TWELFTH: "Subconscious and spirituality"
        }

    def analyze_psychological_context(self, chart: NatalChart) -> Dict[str, float]:
        """Analyze psychological patterns in the chart."""
        psychological_scores = {}
        
        # Analyze planetary positions
        for position in chart.planetary_positions:
            base_score = 1.0
            if position.retrograde:
                base_score *= 0.8  # Retrograde planets indicate internalized energy
            
            # House placement influence
            house_weight = {
                House.FIRST: 1.2,
                House.FOURTH: 1.1,
                House.SEVENTH: 1.1,
                House.TENTH: 1.1
            }.get(position.house, 1.0)
            
            psychological_scores[position.planet.value] = base_score * house_weight
        
        return psychological_scores

    def analyze_cultural_context(self, chart: NatalChart) -> Dict[str, str]:
        """Analyze cultural and societal influences in the chart."""
        cultural_insights = {}
        
        # Analyze generational planets
        for position in chart.planetary_positions:
            if position.planet in [Planet.URANUS, Planet.NEPTUNE, Planet.PLUTO]:
                cultural_insights[position.planet.value] = (
                    f"Generational influence in {position.sign.value} "
                    f"indicating {self._get_generational_theme(position)}"
                )
        
        return cultural_insights

    def analyze_temporal_context(self, chart: NatalChart) -> Dict[str, str]:
        """Analyze temporal patterns and cycles in the chart."""
        temporal_insights = {}
        
        # Analyze planetary cycles
        for position in chart.planetary_positions:
            cycle_length = self._get_planetary_cycle(position.planet)
            temporal_insights[position.planet.value] = (
                f"Current position in {cycle_length}-year cycle"
            )
        
        return temporal_insights

    def interpret_chart(self, chart: NatalChart) -> Interpretation:
        """Generate comprehensive interpretation of the natal chart."""
        psychological = self.analyze_psychological_context(chart)
        cultural = self.analyze_cultural_context(chart)
        temporal = self.analyze_temporal_context(chart)
        
        contextual_layer = ContextualLayer(
            psychological=psychological,
            cultural=cultural,
            temporal=temporal
        )
        
        # Generate interpretations
        planetary_interpretation = {
            pos.planet: self._interpret_planetary_position(pos)
            for pos in chart.planetary_positions
        }
        
        aspect_interpretation = {
            f"{asp.planet1.value}-{asp.planet2.value}": self._interpret_aspect(asp)
            for asp in chart.aspects
        }
        
        house_interpretation = {
            pos.house: self._interpret_house_position(pos)
            for pos in chart.planetary_positions
        }
        
        return Interpretation(
            planetary_interpretation=planetary_interpretation,
            aspect_interpretation=aspect_interpretation,
            house_interpretation=house_interpretation,
            contextual_insights=contextual_layer
        )

    def _get_generational_theme(self, position: PlanetaryPosition) -> str:
        """Get the generational theme for outer planets."""
        themes = {
            Planet.URANUS: "innovation and revolution",
            Planet.NEPTUNE: "collective consciousness",
            Planet.PLUTO: "transformation and power"
        }
        return themes.get(position.planet, "unknown")

    def _get_planetary_cycle(self, planet: Planet) -> int:
        """Get the typical cycle length for a planet."""
        cycles = {
            Planet.MOON: 28,
            Planet.MERCURY: 88,
            Planet.VENUS: 225,
            Planet.MARS: 687,
            Planet.JUPITER: 12,
            Planet.SATURN: 29,
            Planet.URANUS: 84,
            Planet.NEPTUNE: 165,
            Planet.PLUTO: 248
        }
        return cycles.get(planet, 0)

    def _interpret_planetary_position(self, position: PlanetaryPosition) -> str:
        """Generate interpretation for a planetary position."""
        base_meaning = self.psychological_archetypes[position.planet]
        sign_qualities = {
            "cardinal": ["Aries", "Cancer", "Libra", "Capricorn"],
            "fixed": ["Taurus", "Leo", "Scorpio", "Aquarius"],
            "mutable": ["Gemini", "Virgo", "Sagittarius", "Pisces"]
        }
        
        modality = next(
            (k for k, v in sign_qualities.items() if position.sign.value in v),
            "unknown"
        )
        
        return (
            f"{base_meaning} expressed through {position.sign.value} "
            f"({modality} modality) in the {position.house.name.lower()} house"
        )

    def _interpret_aspect(self, aspect: Aspect) -> str:
        """Generate interpretation for an aspect."""
        aspect_meanings = {
            "conjunction": "intensified and combined",
            "opposition": "polarized and balanced",
            "trine": "harmonious and flowing",
            "square": "challenging and dynamic",
            "sextile": "supportive and cooperative"
        }
        
        return (
            f"{aspect.planet1.value} and {aspect.planet2.value} are "
            f"{aspect_meanings.get(aspect.aspect_type, 'connected')} "
            f"with an orb of {aspect.orb:.1f} degrees"
        )

    def _interpret_house_position(self, position: PlanetaryPosition) -> str:
        """Generate interpretation for a house position."""
        return (
            f"{position.planet.value} in the {position.house.name.lower()} house "
            f"({self.house_meanings[position.house]})"
        ) 