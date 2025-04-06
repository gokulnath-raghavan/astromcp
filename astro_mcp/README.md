# Astrology Model Context Protocol (MCP)

A comprehensive framework for astrological analysis that integrates traditional astrological systems with modern contextual analysis through multiple lenses.

## Features

- **Multi-layered Analysis**: Combines traditional astrological calculations with psychological, cultural, and temporal contexts
- **Precise Calculations**: Uses Swiss Ephemeris for accurate planetary positions and aspects
- **Contextual Interpretation**: Provides rich interpretations through multiple analytical lenses
- **Modern API**: RESTful API for integration with other systems
- **User-friendly Interface**: Streamlit-based web interface for easy access
- **Extensible Architecture**: Modular design for easy extension and customization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/astro-mcp.git
cd astro-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download Swiss Ephemeris files:
```bash
mkdir ephe
# Download ephemeris files from https://www.astro.com/ftp/swisseph/ephe/
```

## Usage

### API Server

Start the FastAPI server:
```bash
uvicorn astro_mcp.api.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

### Web Interface

Start the Streamlit interface:
```bash
streamlit run astro_mcp/ui/app.py
```

The web interface will be available at `http://localhost:8501`.

## Architecture

The framework is organized into several key components:

1. **Core Models** (`core/models.py`):
   - Data structures for planetary positions, aspects, and charts
   - Type definitions for astrological entities

2. **Calculator** (`core/calculator.py`):
   - Astronomical calculations using Swiss Ephemeris
   - Chart generation and aspect calculation

3. **Interpreter** (`core/interpreter.py`):
   - Contextual analysis through multiple lenses
   - Psychological, cultural, and temporal interpretations

4. **API** (`api/main.py`):
   - RESTful endpoints for chart generation and analysis
   - Integration points for other systems

5. **UI** (`ui/app.py`):
   - Streamlit-based web interface
   - Interactive chart generation and interpretation

## API Endpoints

- `POST /generate-chart`: Generate a natal chart with optional contextual analysis
- `GET /planetary-positions/{planet}`: Get planetary positions over time
- `GET /aspects/{planet1}/{planet2}`: Calculate aspects between planets
- `GET /contextual-analysis/{chart_id}`: Get contextual analysis for a chart

## Integration Examples

### Python Integration

```python
from astro_mcp.core.calculator import AstroCalculator
from astro_mcp.core.interpreter import ContextualInterpreter
from datetime import datetime

# Generate a chart
calculator = AstroCalculator()
chart = calculator.generate_natal_chart(
    datetime(1990, 1, 1, 12, 0),
    0.0,  # latitude
    0.0   # longitude
)

# Get contextual interpretation
interpreter = ContextualInterpreter()
interpretation = interpreter.interpret_chart(chart)
```

### API Integration

```python
import requests

# Generate a chart
response = requests.post(
    "http://localhost:8000/generate-chart",
    json={
        "birth_data": {
            "birth_time": "1990-01-01T12:00:00",
            "latitude": 0.0,
            "longitude": 0.0
        },
        "include_contextual": True
    }
)
chart_data = response.json()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Swiss Ephemeris for precise astronomical calculations
- FastAPI for the API framework
- Streamlit for the web interface
- The astrological community for their insights and knowledge 