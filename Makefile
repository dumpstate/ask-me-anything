.PHONY: run

run:
	uvicorn ama.main:app --reload
