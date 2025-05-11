from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict
from fastapi import Query

class GameRequestOutput(BaseModel):
    competition: Optional[int] = None

    home_team: Optional[str] = None
    away_team: Optional[str] = None
    target_team: Optional[str] = None

    score_home_min: Optional[int] = Field(None, ge=0)
    score_home_max: Optional[int] = Field(None, ge=0)
    score_away_min: Optional[int] = Field(None, ge=0)
    score_away_max: Optional[int] = Field(None, ge=0)

    date_start: Optional[date] = None
    date_end: Optional[date] = None

class GameRequestCreate(GameRequestOutput):
    skip: Optional[int] = 0
    limit: Optional[int] = 25

    @field_validator('score_home_max')
    def validate_home_scores(cls, v, values):
        if v is not None and (min_val := values.data.get('score_home_min')) is not None:
            if v < min_val:
                raise ValueError('score_home_max < score_home_min')
        return v

    @field_validator('score_away_max')
    def validate_away_scores(cls, v, values):
        if v is not None and (min_val := values.data.get('score_away_min')) is not None:
            if v < min_val:
                raise ValueError('score_away_max < score_away_min')
        return v

    @field_validator('date_end')
    def validate_dates(cls, v, values):
        if v is not None and (start := values.data.get('date_start')) is not None:
            if v < start:
                raise ValueError('date_end < date_start')
        return v

class GameCreate(BaseModel):
    competition: Optional[int] = None

    home_team: Optional[str] = None
    away_team: Optional[str] = None

    score_home: Optional[int] = Field(None, ge=0)
    score_away: Optional[int] = Field(None, ge=0)

    date: date

class GameOutput(GameCreate):
    id: Optional[int] = None

    class Config:
        from_attributes = True

async def get_game_filters(
    competition: Optional[int] = Query(None),
    home_team: Optional[str] = Query(None),
    away_team: Optional[str] = Query(None),
    target_team: Optional[str] = Query(None),
    score_home_min: Optional[int] = Query(None, ge=0),
    score_home_max: Optional[int] = Query(None, ge=0),
    score_away_min: Optional[int] = Query(None, ge=0),
    score_away_max: Optional[int] = Query(None, ge=0),
    date_start: Optional[date] = Query(None),
    date_end: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100)
) -> GameRequestCreate:
    return GameRequestCreate(
        competition=competition,
        home_team=home_team,
        away_team=away_team,
        target_team=target_team,
        score_home_min=score_home_min,
        score_home_max=score_home_max,
        score_away_min=score_away_min,
        score_away_max=score_away_max,
        date_start=date_start,
        date_end=date_end,
        skip=skip,
        limit=limit
    )

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True