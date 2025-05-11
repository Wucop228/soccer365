from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api_v1 import crud
from app.api_v1.schemas import GameOutput, get_game_filters, GameRequestCreate

router_v1 = APIRouter()

@router_v1.get("/games/", response_model=List[GameOutput])
def get_games(
    filters: GameRequestCreate = Depends(get_game_filters),
    db: Session = Depends(get_db)
):
    return crud.get_matches(db, filters)[filters.skip: filters.skip + filters.limit]