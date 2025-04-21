all: run

run:
	uvicorn app.main:app --reload

inst:
	pip install -r requirements.txt