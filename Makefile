
up:
	docker compose -f .devcontainer/compose.yaml up -d

pull-models-small:
	docker exec -it ollama bash -lc "ollama pull gemma3:1b"

pull-models:
	docker exec -it ollama bash -lc "ollama pull gemma3:latest"

down:
	- docker compose -f .devcontainer/docker-compose.full.yml down
	- docker compose -f .devcontainer/docker-compose.ollama.yml down

test:
	pytest -q

slides:
	reveal-md docs/guia/slides.md --watch
