.PHONY: migrate, run

run:
	uvicorn ama.main:app --reload

migrate:
	alembic upgrade head
