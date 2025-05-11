from datetime import datetime

from app.parsers.site_parser import parse_all_competition
from app.api_v1.schemas import GameCreate
from app.api_v1.crud import create_match
from app.database import SessionLocal
import app.cmp.competition_loader

def convert_score(score: str):
    return map(int, score.split(":"))

def process_matches(parse_date: str | None = None):
    db = SessionLocal()
    print("Start parsing")
    try:
        all_matches = parse_all_competition(parse_date)
        for competition_id, matches in all_matches.items():
            if not competition_id in app.cmp.competition_loader.competitions["cmp_id"]:
                continue
            for match in matches:
                try:
                    score_home, score_away = convert_score(match["score"])
                    match_date = datetime.strptime(match["date"], "%d.%m.%Y").date()

                    game = GameCreate(
                        competition=int(competition_id[3:]),
                        home_team=match["home_team"],
                        away_team=match["away_team"],
                        score_home=score_home,
                        score_away=score_away,
                        date=match_date
                    )

                    create_match(db, game)
                except Exception as e:
                    print(f"Error when adding a match: {e}")
        print(all_matches)
        print("End parsing")
    finally:
        db.close()