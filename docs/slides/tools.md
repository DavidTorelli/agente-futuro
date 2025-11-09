---
title: Herramientas para agentes — Guía práctica
theme: black
separator: '^---$'
verticalSeparator: '^--$'
revealOptions:
  margin: 0.04
  minScale: 0.4
  maxScale: 1.6
  slideNumber: 'c/t'
---

<style>
.reveal section {
  text-align: left;
}
.reveal section h1,
.reveal section h2,
.reveal section h3 {
  text-align: center;
}
</style>

# Herramientas para agentes

Cómo extender Open WebUI + Ollama para que los agentes ejecuten acciones reales.

---

## Accediendo a datos meteorológicos

1. Preguntar que tiempo hará mañana en nuestra ciudad. Que ocurre? 
2. Navegar a la web de herramientas de OpenWebUI: http://localhost:3000/workspace/tools
3. Instalar keyless_weather: https://openwebui.com/t/spyci/keyless_weather
4. Activar la herramienta para que el agente tenga acceso.
5. Volver a preguntar. Que ha ocurrido ahora?

---

## Open WebUI - Workspace
- 🤖 [Modelos](https://docs.openwebui.com/features/workspace/models):  
Crea y gestiona modelos personalizados para propósitos específicos.
- 🧠 [Conocimiento](https://docs.openwebui.com/features/workspace/knowledge):  
Gestiona las bases de conocimiento necesarias para tu caso de usa aplicando RAG.
- 📚 [Prompts](https://docs.openwebui.com/features/workspace/prompts):  
Crea y organiza prompts reutilizables.

---

## Paso 2 — Define el contrato de la herramienta

Describe qué hace y qué parámetros recibe.

```json
{
  "name": "buscar_doc",
  "description": "Busca fragmentos en la base documental",
  "schema": {
    "query": "string",
    "max_results": "integer"
  }
}
```

-- 

Tips:
- Usa nombres descriptivos.
- Documenta formatos esperados (ej. fechas, IDs).
- Mantén los contratos pequeños y reutilizables.

---

## Paso 3 — Implementa el handler

```python
# tools/buscar_doc.py
from typing import List

def run(query: str, max_results: int = 3) -> List[str]:
    """Devuelve fragmentos relevantes desde la colección local."""
    if not query:
        raise ValueError("El parámetro 'query' es obligatorio")

    # TODO: conectar con vector DB o índice local
    hits = [
        {"title": "Manual DevContainer", "snippet": "Para abrir el contenedor..."},
        {"title": "Guía Ollama", "snippet": "Usa `ollama pull` para descargar..."},
    ]
    return hits[:max_results]
```

-- 

Buenas prácticas:
- Valida entradas antes de ejecutar lógica costosa.
- Lanza errores explícitos (ValueError, RuntimeError).
- Usa logs (`logging.getLogger(__name__)`) para diagnósticos.

---

## Paso 4 — Registra la herramienta

Actualiza `tools.json` (archivo global) o el registro equivalente en tu stack.

```json
[
  {
    "name": "buscar_doc",
    "description": "Busca fragmentos en la base documental",
    "schema": {
      "query": "string",
      "max_results": {
        "type": "integer",
        "default": 3
      }
    },
    "handler": "tools.buscar_doc:run"
  }
]
```

- Usa rutas `package.module:function`.
- Define valores por defecto para parámetros opcionales.
- Mantén comentarios fuera de JSON (Reveal no los soporta).

---

## Paso 5 — Probar en Open WebUI

1. Reinicia Open WebUI si la herramienta no aparece.
2. Crea un nuevo chat y selecciona el modelo (ej. `gemma3:1b`).
3. Pide explícitamente usar la herramienta:  
   > "Busca documentación sobre devcontainers usando la herramienta `buscar_doc`."
4. Revisa la consola de Open WebUI para ver la ejecución y los `observations`.

-- 

Si falla:
- Inspecciona los logs del contenedor (`docker logs` o `make logs` si existe).
- Comprueba el nombre del handler y dependencias importadas.
- Asegura que la función devuelve JSON serializable.

---

## Depuración y observabilidad

- **Timeouts**: limita ejecuciones largas (`asyncio.wait_for` o `signal`).
- **Retornos**: formatea datos amigables para el LLM (listas cortas, texto conciso).
- **Reintentos**: implementa retries con backoff cuando llamas APIs externas.
- **Testing**: agrega pruebas unitarias a cada tool para validarla en aislamiento.

---

## Extender a MCP (opcional)

- Implementa un servidor MCP (`fastmcp`, `node-mcp`, etc.).
- Expone herramientas similares a las locales pero vía protocolo MCP.
- Configura Open WebUI: `Settings → MCP Servers → añadir endpoint`.
- Ventaja: reutilizas las mismas herramientas desde otros agentes o plataformas.

---

# Checklist final

- [ ] Contrato definido y documentado.
- [ ] Handler validado con pruebas manuales/automáticas.
- [ ] Registro actualizado (`tools.json` o MCP server).
- [ ] Logs verificados en Open WebUI.
- [ ] Demo lista con prompt de ejemplo.

¡Listo! El agente ya puede ejecutar acciones usando tus herramientas.
