from datetime import date, timedelta
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .models import Results
from .schemas import GameCreate, GameRequestOutput, GameOutput

def is_match_exists(db: Session, home_team: str, away_team: str, match_date: date) -> bool:
    existing_match = db.query(Results).filter(
        Results.home_team == home_team,
        Results.away_team == away_team,
        Results.date.in_([match_date, match_date - timedelta(days=1)])
    ).first()
    return existing_match is not None

def create_match(db: Session, game: GameCreate) -> GameOutput:
    if is_match_exists(db, game.home_team, game.away_team, game.date):
        return None

    db_game = Results(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    print(game.model_dump())
    return GameOutput.model_validate(db_game)

def get_matches(db: Session, game: GameRequestOutput) -> List[GameOutput]:
    query = db.query(Results)
    filters = []

    if game.competition is not None:
        filters.append(Results.competition == game.competition)

    if game.home_team is not None:
        filters.append(Results.home_team == game.home_team)
    if game.away_team is not None:
        filters.append(Results.away_team == game.away_team)

    if game.target_team is not None:
        filters.append(or_(
            Results.home_team == game.target_team,
            Results.away_team == game.target_team
        ))

    if game.score_home_min is not None:
        filters.append(Results.score_home >= game.score_home_min)
    if game.score_home_max is not None:
        filters.append(Results.score_home <= game.score_home_max)
    if game.score_away_min is not None:
        filters.append(Results.score_away >= game.score_away_min)
    if game.score_away_max is not None:
        filters.append(Results.score_away <= game.score_away_max)

    if game.date_start is not None and game.date_end is not None:
        filters.append(Results.date.between(game.date_start, game.date_end))
    elif game.date_start is not None:
        filters.append(Results.date >= game.date_start)
    elif game.date_end is not None:
        filters.append(Results.date <= game.date_end)

    if filters:
        query = query.filter(and_(*filters))

    return query.all()