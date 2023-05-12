.PHONY: migrate, run

run:
	uvicorn ask_me_anything.main:app --reload

migrate:
	alembic upgrade head
