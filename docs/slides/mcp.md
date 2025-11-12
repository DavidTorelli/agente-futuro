---
title: Agente Futuro - Introducción
theme: black
separator: '^---$'
verticalSeparator: '^--$'
revealOptions:
  margin: 0.04
  minScale: 0.4
  maxScale: 1.6
  transition: slide
  slideNumber: 'c/t'
---

<style>
.reveal section {
  text-align: left;
}
.reveal section h1,
.reveal section h2,
.reveal section h3,
.reveal section h4 {
  text-align: center;
}
.reveal section h5 {
  text-align: right;
}
</style>

# Agente Futuro
## MCP Tools

---

## Agenda

1. Qué es el **Model Context Protocol** y por qué usarlo.
2. Cómo conectar **MCP servers** con OpenWebUI.
3. Crear y probar **Tools MCP** (ejemplo con números aleatorios).
4. Integrar APIs existentes vía **MPCO (Open API)**.

---

## Requisitos previos

* OpenWebUI con soporte para **MCP clients**.
* Un intérprete Python 3.10+ con `fastmcp` o SDK equivalente.
* Acceso a endpoints/servicios que quieras exponer como tools.
* Opcional: contenedor o proceso supervisado (systemd, PM2) para tu server MCP.

---

## MCP en pocas palabras

- El **Model Context Protocol** define cómo un modelo LLM descubre herramientas externas, sus esquemas y cómo invocarlas.
- Separa **cliente** (p. ej. OpenWebUI) de **servidor** (tus tools), lo que facilita el versionado y el control de permisos.
- Cada servidor expone un `manifest` con metadatos, tools y recursos persistentes.

--

### Flujo de conexión

1. El **cliente MCP** (p. ej. OpenWebUI) inicia el transport (WebSocket, stdio, HTTP2) hacia tu server.
2. El cliente descarga el manifest/capabilities y pone las tools a disposición del LLM.
3. El modelo decide invocar una tool, el cliente MCP empaqueta la llamada JSON y la envía al servidor.
4. El servidor ejecuta la acción, responde con `result`/`error` y el cliente pasa la respuesta de vuelta al LLM.

---

## Conectar un MCP server a [OpenWebUI MCP](https://docs.openwebui.com/openapi-servers/mcp/)

1. Añade los servidores necesarios a tu docker compose.
2. Reinicia el dev container para tenerlos disponible.
2. **Icono de usuario → Admin Panel → Settings → External Tools**.
3. Añade la url (nombre del servicio docker compose y puerto).
4. Guarda para que OpenWebUI compruebe el manifest y registre las tools MCP.

---

## Plantilla base con FastMCP

```python
from fastmcp import MCPServer, tool

app = MCPServer(
    "demo-mcp",
    instructions="Colección de tools internas para agentes Agente Futuro",
)

@tool
def ping() -> str:
    "Verifica que el servidor esté vivo."
    return "pong"

if __name__ == "__main__":
    app.run()
```

- `@tool` registra automáticamente el esquema de entrada/salida.
- `app.run()` abre el transporte (por defecto stdio); usa `app.run_websocket()` para sockets.

---

## Generemos una tool de números aleatorios

- Idea: ofrecer un servicio `random_int` que respeta un rango configurable y loguea las peticiones.
- Reutilizaremos el patrón de válvulas (valves) para valores por defecto.

--

```python
import logging
import random
from typing import Optional
from pydantic import BaseModel, Field
from fastmcp import MCPServer, tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("random-server")

app = MCPServer("random-mcp", instructions="Tools de números aleatorios")

class RandomDefaults(BaseModel):
    default_min: int = Field(0, description="Valor mínimo global")
    default_max: int = Field(100, description="Valor máximo global")

config = RandomDefaults()

@tool
def random_int(min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    "Devuelve un entero aleatorio en el rango solicitado."
    lower = min_value if min_value is not None else config.default_min
    upper = max_value if max_value is not None else config.default_max
    if lower > upper:
        raise ValueError("min_value no puede ser mayor que max_value")
    result = random.randint(lower, upper)
    logger.info("random_int[%s,%s] -> %s", lower, upper, result)
    return result
```

--

### Ejercicio rápido

* Expone `config.default_min` y `config.default_max` como **resources persistentes** para que el cliente los pueda leer/modificar.
* Añade un tool `seed_random(seed: int)` para volver determinista el generador.
* Integra el server con OpenWebUI y ejecuta `random_int` desde el prompt (`/tool random_int {"min_value":10,"max_value":20}`).

---

## Observabilidad y seguridad

- Usa **logging estructurado** y guarda los registros en CloudWatch, Loki o el stack de tu empresa.
- Define **timeouts** en llamadas HTTP dentro de tus tools para evitar bloqueos.
- Controla el acceso con `allowed_origins`/tokens y valida inputs (nunca ejecutes shell sin sanitizar).
- Versiona tu manifest; cambia el `server_id` si rompes compatibilidad.

---

## Buenas prácticas específicas de MCP

- **Pequeñas herramientas**: cada tool debe hacer una sola cosa y describirse bien.
- **Docs inline**: docstrings = instructivo para el LLM; añade ejemplos.
- **Tests locales**: prueba tus tools como funciones Python antes de empaquetar el servidor.
- **Deployment repetible**: contenedores ligeros o scripts reproducibles (`uv run server.py`).

---

## Sección MPCO (Open API)

- [**MPCO**](https://github.com/open-webui/mcpo) actúa como puente entre descripciones **OpenAPI** y el ecosistema MCP.
- Permite registrar un manifiesto OpenAPI (YAML/JSON) y generar tools MCP automáticamente.
- Flujo sugerido:
  1. Define/recibe la especificación OpenAPI del servicio (p. ej. microservicio de pedidos).
  2. MPCO lee la spec y expone cada `operationId` como tool MCP con validación de parámetros.
  3. OpenWebUI descubre esas tools vía MCP y el modelo puede llamar endpoints REST sin código adicional.
- Recomendaciones:
  * Mantén la spec sincronizada (usa `schemathesis` o CI para validar).
  * Configura autenticación (API keys, OAuth) desde MPCO para no exponer credenciales al modelo.
  * Documenta límites y tiempos de espera dentro de la spec para guiar al LLM.

---

## Próximos pasos

* Empaqueta tus servers MCP en la carpeta `servers/` del repo y crea scripts `make run-mcp-<tool>`.
* Publica un catálogo interno (`awesome-mcp.md`) para que el resto del equipo conozca las herramientas disponibles.
* Experimenta combinando MCP servers (p. ej. `random-mcp` + `reporting-mcp`) en un mismo modelo dentro de OpenWebUI.
