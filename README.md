# Soccer365 Parser API
A Python service that parses data from score365 every 5 minutes and provides an API to access up-to-date football match information.

## Features

- Automatic data parsing every 5 minutes
- REST API for accessing live match results
- Easy integration with other services

## Installation
1. Clone the repository:
    git clone https://github.com/Wucop228/soccer365.git
2. Navigate to the project directory: cd soccer365
3. Create and activate a virtual environment:
- On macOS/Linux:
- python3 -m venv venv; source venv/bin/activate
4. Install dependencies: make inst
5. Start the development server: make

## Using
The data will be automatically added to the database.
To get them from the database, you need to use the api.
Use this url http://127.0.0.1:8000/games/
and this queries:
1. competition
2. home_team
3. away_team
4. target_team
5. score_home_min
6. score_home_max
7. score_away_min
8. score_away_max
9. date_start
10. date_end
11. skip
12. limit
# Example
http://127.0.0.1:8000/games/?competition=19&target_team=%D0%91%D0%B0%D1%80%D1%81%D0%B5%D0%BB%D0%BE%D0%BD%D0%B0&score_home_min=0&score_home_max=15&score_away_min=0&score_away_max=15&date_start=2025-01-01&date_end=2025-06-01&skip=0&limit=100