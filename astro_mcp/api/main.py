from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from ..core.calculator import AstroCalculator
from ..core.interpreter import ContextualInterpreter
from ..core.models import NatalChart, Interpretation

app = FastAPI(
    title="Astrology Model Context Protocol",
    description="A comprehensive framework for astrological analysis with contextual interpretation",
    version="1.0.0"
)

class BirthData(BaseModel):
    birth_time: datetime
    latitude: float
    longitude: float
    timezone: Optional[str] = None

class ChartRequest(BaseModel):
    birth_data: BirthData
    include_contextual: bool = True

class ChartResponse(BaseModel):
    chart: NatalChart
    interpretation: Optional[Interpretation] = None

@app.post("/generate-chart", response_model=ChartResponse)
async def generate_chart(request: ChartRequest):
    try:
        calculator = AstroCalculator()
        chart = calculator.generate_natal_chart(
            request.birth_data.birth_time,
            request.birth_data.latitude,
            request.birth_data.longitude
        )
        
        response = ChartResponse(chart=chart)
        
        if request.include_contextual:
            interpreter = ContextualInterpreter()
            response.interpretation = interpreter.interpret_chart(chart)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/planetary-positions/{planet}")
async def get_planetary_positions(
    planet: str,
    start_time: datetime,
    end_time: datetime,
    interval_hours: int = 24
):
    try:
        calculator = AstroCalculator()
        positions = []
        current_time = start_time
        
        while current_time <= end_time:
            pos = calculator.calculate_planetary_positions(
                current_time,
                0.0,  # Default to equator
                0.0   # Default to prime meridian
            )
            positions.append({
                "time": current_time,
                "position": pos
            })
            current_time = current_time + timedelta(hours=interval_hours)
        
        return positions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/aspects/{planet1}/{planet2}")
async def get_aspects(
    planet1: str,
    planet2: str,
    start_time: datetime,
    end_time: datetime,
    orb: float = 8.0
):
    try:
        calculator = AstroCalculator()
        aspects = []
        current_time = start_time
        
        while current_time <= end_time:
            pos1 = calculator.calculate_planetary_positions(
                current_time,
                0.0,
                0.0
            )
            pos2 = calculator.calculate_planetary_positions(
                current_time,
                0.0,
                0.0
            )
            
            aspect = calculator.calculate_aspects([pos1, pos2])
            if aspect:
                aspects.append({
                    "time": current_time,
                    "aspect": aspect
                })
            
            current_time = current_time + timedelta(hours=1)
        
        return aspects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contextual-analysis/{chart_id}")
async def get_contextual_analysis(chart_id: str):
    try:
        # In a real implementation, this would fetch the chart from a database
        # For now, we'll return a mock response
        interpreter = ContextualInterpreter()
        return {
            "psychological": interpreter.analyze_psychological_context(None),
            "cultural": interpreter.analyze_cultural_context(None),
            "temporal": interpreter.analyze_temporal_context(None)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 