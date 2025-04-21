from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .schemas import GameOutput, GameRequestCreate
from .database import get_db
from . import crud
from .scheduler import start_scheduler

app = FastAPI()

# start_scheduler()

@app.get("/games/", response_model=List[GameOutput])
def get_games(game: GameRequestCreate, db: Session = Depends(get_db)):
    return crud.get_matches(db=db, game=game)[game.skip:game.skip + game.limit]