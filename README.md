
# AI Agents Workshop — Starter Kit (Docker)

## Todo lo que necesitas es ...
- Docker: https://www.docker.com/products/docker-desktop/
- Visual Studio Code: https://code.visualstudio.com/
- Dev Container plugin: [ms-vscode-remote.vscode-remote-extensionpack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

## Estructura
- `data/images/...` imágenes sintéticas de contenedores y matrículas con groundtruth en `data/csv/*_labels.csv`.
- `data/csv/stock_supplies.csv` y `planned.csv` / `delivered.csv` para los proyectos 2 y 3.
- `tests/` plantillas `pytest` por proyecto.
- `src/` stubs: añade tu lógica en `src/_student_solutions` y módulos por proyecto.
- `compose/` docker-compose para entorno local.
- `Makefile` con atajos.

## Uso rápido
```bash
make up             # solo Ollama
make up-full        # Ollama + Open WebUI
make pull-models    # descarga modelos (ajusta a tu GPU)
make test           # ejecuta tests (algunos se marcarán como skip hasta implementar)
```

### API Gemma3 + Open WebUI
- `POST /chat`: proxy de texto plano hacia Ollama.
- `POST /agent/chat`: expone un agente CrewAI que usa Gemma3 (`ollama`) y las herramientas de `01_container_ref_extractor` para extraer códigos a partir de imágenes en `image_base64` o `image_url`.
- Variables de entorno: `OLLAMA_URL`, `OLLAMA_MODEL` (por defecto `gemma3:latest`) y `OLLAMA_TIMEOUT`.

## Tareas a implementar por los alumnos
- OCR + regex → `src/_student_solutions/ocr_stub.py`
- Reglas de stock → módulo propio en `src/02_stock`
- Fusión planned/delivered → módulo propio en `src/03_planning`
- API → ampliar `src/04_api/main.py`

## Tooling OpenAPI dentro del Dev Container
- La imagen incluye `@redocly/openapi-cli` para validar/previsualizar specs (`openapi lint docs/openapi.yaml`, `openapi preview-docs docs/openapi.yaml --port 8080`).
- Puedes generar clientes base con `openapi-python-client generate --path docs/openapi.yaml` para acelerar la creación de tools MCP.
- Ejecuta `swagger-ui-watcher docs/openapi.yaml --port 8081` para navegar la documentación Swagger localmente mientras desarrollas tus herramientas.
