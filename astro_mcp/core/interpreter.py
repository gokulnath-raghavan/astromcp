from typing import Dict, List, Any
from .models import (
    NatalChart, Interpretation, ContextualLayer,
    Planet, House, Aspect, PlanetaryPosition, TemporalCycle
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

    def interpret_chart(self, chart: NatalChart) -> Interpretation:
        """Generate contextual interpretation of the natal chart."""
        return Interpretation(
            basic=self._basic_interpretation(chart),
            temporal=self._temporal_interpretation(chart),
            spiritual=self._spiritual_interpretation(chart),
            psychological=self._psychological_interpretation(chart)
        )

    def _basic_interpretation(self, chart: NatalChart) -> Dict[str, str]:
        """Generate basic astrological interpretation."""
        return {
            "ascendant": f"Your rising sign is {chart.ascendant.value}, indicating your outward personality and first impressions.",
            "midheaven": f"Your Midheaven in {chart.midheaven.value} suggests your career path and public image.",
            "planetary_positions": "\n".join([
                f"{pos.planet.value} in {pos.sign.value} (House {pos.house.value}) - "
                f"indicating {self._get_planet_meaning(pos.planet, pos.sign, pos.house)}"
                for pos in chart.planetary_positions
            ]),
            "aspects": "\n".join([
                f"{aspect.planet1.value} {aspect.aspect_type.value} {aspect.planet2.value} - "
                f"indicating {self._get_aspect_meaning(aspect)}"
                for aspect in chart.aspects
            ])
        }

    def _temporal_interpretation(self, chart: NatalChart) -> Dict[str, str]:
        """Generate temporal cycle interpretation."""
        cycles = {
            "SUN": TemporalCycle(cycle_length=0, current_position="Current position in 0-year cycle"),
            "MOON": TemporalCycle(cycle_length=28, current_position="Current position in 28-year cycle"),
            "MERCURY": TemporalCycle(cycle_length=88, current_position="Current position in 88-year cycle"),
            "VENUS": TemporalCycle(cycle_length=225, current_position="Current position in 225-year cycle"),
            "JUPITER": TemporalCycle(cycle_length=12, current_position="Current position in 12-year cycle"),
            "SATURN": TemporalCycle(cycle_length=29, current_position="Current position in 29-year cycle"),
            "URANUS": TemporalCycle(cycle_length=84, current_position="Current position in 84-year cycle"),
            "NEPTUNE": TemporalCycle(cycle_length=165, current_position="Current position in 165-year cycle"),
            "PLUTO": TemporalCycle(cycle_length=248, current_position="Current position in 248-year cycle")
        }
        return {planet: cycle.current_position for planet, cycle in cycles.items()}

    def _spiritual_interpretation(self, chart: NatalChart) -> Dict[str, str]:
        """Generate spiritual interpretation."""
        return {
            "karmic_indicators": self._identify_karmic_indicators(chart),
            "soul_purpose": self._determine_soul_purpose(chart),
            "spiritual_gifts": self._identify_spiritual_gifts(chart)
        }

    def _psychological_interpretation(self, chart: NatalChart) -> Dict[str, str]:
        """Generate psychological interpretation."""
        return {
            "personality_traits": self._identify_personality_traits(chart),
            "emotional_patterns": self._identify_emotional_patterns(chart),
            "behavioral_tendencies": self._identify_behavioral_tendencies(chart)
        }

    def _get_planet_meaning(self, planet, sign, house) -> str:
        """Get meaning of planet in sign and house."""
        meanings = {
            "SUN": "vitality and self-expression",
            "MOON": "emotions and instincts",
            "MERCURY": "communication and intellect",
            "VENUS": "love and values",
            "MARS": "action and desire",
            "JUPITER": "expansion and wisdom",
            "SATURN": "discipline and structure",
            "URANUS": "innovation and change",
            "NEPTUNE": "imagination and spirituality",
            "PLUTO": "transformation and power"
        }
        return meanings.get(planet.value, "unknown influence")

    def _get_aspect_meaning(self, aspect) -> str:
        """Get meaning of aspect between planets."""
        aspect_meanings = {
            "conjunction": "a blending of energies",
            "sextile": "harmonious opportunities",
            "square": "challenges and tension",
            "trine": "natural flow and ease",
            "opposition": "polarity and balance"
        }
        return aspect_meanings.get(aspect.aspect_type.value, "a relationship between planets")

    def _identify_karmic_indicators(self, chart: NatalChart) -> str:
        """Identify karmic indicators in the chart."""
        return "Your chart shows significant karmic patterns in the 8th and 9th houses, indicating deep spiritual transformation and wisdom."

    def _determine_soul_purpose(self, chart: NatalChart) -> str:
        """Determine soul purpose from the chart."""
        return "Your soul purpose is to learn and grow through various life experiences, particularly in the areas of transformation and wisdom."

    def _identify_spiritual_gifts(self, chart: NatalChart) -> str:
        """Identify spiritual gifts from the chart."""
        return "You have strong intuitive abilities and a natural connection to spiritual wisdom."

    def _identify_personality_traits(self, chart: NatalChart) -> str:
        """Identify personality traits from the chart."""
        return "You are analytical, intuitive, and have a strong desire for knowledge and transformation."

    def _identify_emotional_patterns(self, chart: NatalChart) -> str:
        """Identify emotional patterns from the chart."""
        return "You tend to process emotions deeply and may have strong intuitive responses to situations."

    def _identify_behavioral_tendencies(self, chart: NatalChart) -> str:
        """Identify behavioral tendencies from the chart."""
        return "You are likely to be methodical in your approach and have a strong drive for personal growth."

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
            f"{aspect_meanings.get(aspect.aspect_type.value, 'connected')} "
            f"with an orb of {aspect.orb:.1f} degrees"
        )

    def _interpret_house_position(self, position: PlanetaryPosition) -> str:
        """Generate interpretation for a house position."""
        return (
            f"{position.planet.value} in the {position.house.name.lower()} house "
            f"({self.house_meanings[position.house]})"
        ) 