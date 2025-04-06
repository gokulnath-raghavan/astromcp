# Astrology Vector Database

A vector database system for storing and retrieving astrological information using FAISS and sentence transformers.

## Features

- Vector storage of astrological interpretations
- Semantic search capabilities
- Support for planetary positions, zodiac signs, and houses
- Easy-to-use API for querying astrological information

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tests:
```bash
pytest tests/
```

## Project Structure

- `src/`: Source code
  - `embeddings.py`: Embedding generation and management
  - `database.py`: Vector database operations
  - `data_processor.py`: Data preprocessing utilities
- `data/`: Data storage
- `tests/`: Test files
- `config/`: Configuration files

## Usage

```python
from src.database import AstrologyDB

# Initialize the database
db = AstrologyDB()

# Add astrological interpretations
db.add_interpretation("Sun in Aries represents leadership and initiative")

# Search for interpretations
results = db.search("What does it mean to have Mars in Leo?")
```

## License

MIT License 