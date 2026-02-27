.PHONY: setup test run-api docker-up docker-down

setup:
	./scripts/setup.sh

test:
	./scripts/test.sh

run-api:
	./scripts/run_api.sh

docker-up:
	docker compose up --build

docker-down:
	docker compose down
