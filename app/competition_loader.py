from typing import Dict, Any
import json
from pathlib import Path

def load_competitions() -> Dict[str, Any]:
    path = Path(__file__).parent / 'competitions.json'
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

competitions = load_competitions()