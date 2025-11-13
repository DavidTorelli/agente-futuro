
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

intro-slides:
	reveal-md docs/slides/intro.md --watch

config-slides:
	reveal-md docs/slides/config.md --watch

tools-slides:
	reveal-md docs/slides/tools.md --watch

mcp-slides:
	reveal-md docs/slides/mcp.md --watch

mcp-debug-slides:
	reveal-md docs/slides/mcp-debug.md --watch
