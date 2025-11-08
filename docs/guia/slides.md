---
title: Clase 1 — Agentes de IA
theme: black
revealOptions:
  transition: slide
  slideNumber: 'c/t'
---

# AI - Agentes  
#### Open WebUI + Ollama + Models + MCP Tools

Note:
- Presentación de la serie y objetivos del taller.
- Enfatizar: enfoque práctico con stack local y privado.

---

## Agenda

1. ¿Qué es un agente?  
2. LLM vs Asistentes vs Agentes  
3. Herramientas: extendiendo capacidades  
4. Frameworks para agentes  
5. Stack: Open WebUI + Ollama + Tools  
6. Open WebUI Tools vs MCP Tools  
7. Extender Open WebUI

Note:
- Recalcar que hoy es visión general + fundamento para construir en la siguiente clase.

---

## ¿Qué es un agente?

Un **agente** es un sistema que percibe, razona y actúa para lograr un objetivo en su entorno.

**Tipos:**
- Reactivo: responde a estímulos.
- Deliberativo: planifica y evalúa.
- Colaborativo / Multiagente: coordina con otros agentes.

```text
Percepción → Razonamiento → Acción → Evaluación → (loop)
```

Ejemplo: un agente que revisa emails, extrae facturas y actualiza una base de datos.

Note:
- Dar un ejemplo cercano a la práctica del curso (OCR de facturas, MinIO/S3, etc.).

---

## LLM vs Asistentes vs Agentes

| Concepto | Qué hace | Ejemplo |
|-----------|-----------|----------|
| **LLM** | Genera texto | Llama, Gemma, Mistral |
| **Asistente** | Gestiona contexto limitado | Chat assistants |
| **Agente** | Planifica, decide y actúa | CrewAI, AutoGen |

**Salto clave:**
- Del *prompt* → al **plan**
- Del texto → a la **acción**
- Del contexto estático → a **memoria y herramientas**

Note:
- Diferenciar claramente “asistente” (reactivo) vs “agente” (proactivo con herramientas).

---

## RAG y KAG: dando memoria y conocimiento a los agentes

### 🔍 RAG — *Retrieval-Augmented Generation*
**Idea:** combinar un modelo LLM con un motor de búsqueda o base de conocimiento **externa y actualizada**.

**Cómo funciona:**
1. El usuario hace una pregunta.  
2. El agente busca información relevante (en vector DB, documentos, etc.).  
3. El contexto encontrado se añade al *prompt* del modelo.  
4. El modelo genera una respuesta más precisa y contextual.

**Aplicaciones:**
- Chatbots corporativos (manuales, documentación, FAQs)  
- Asistentes legales, técnicos o médicos  
- Consulta de datos empresariales sin exponer la base completa

💡 *Ejemplo:*  
Un agente que consulta políticas internas de una empresa antes de responder al usuario.

---

### 🧠 KAG — *Knowledge-Augmented Generation*
**Idea:** el agente integra **estructuras de conocimiento preprocesadas** (ontologías, grafos, embeddings, relaciones semánticas).

**Diferencias con RAG:**
| Aspecto | RAG | KAG |
|----------|-----|-----|
| Fuente de información | Documentos recuperados | Conocimiento estructurado (grafo, triples, JSON-LD...) |
| Enfoque | Búsqueda + contexto | Razonamiento sobre relaciones |
| Ejemplo | Buscador de documentos | Asistente que infiere relaciones entre conceptos |

**Aplicaciones:**
- Sistemas expertos  
- Asistentes educativos o científicos  
- Agentes que deben inferir o razonar más allá del texto literal

---

### 🧩 RAG + KAG en agentes

**RAG** aporta *actualidad y contexto*.  
**KAG** aporta *razonamiento y estructura*.  

Juntos permiten construir agentes con:  
- Contexto dinámico (RAG)  
- Razonamiento simbólico (KAG)  
- Memoria persistente y conocimiento vivo  

---

## Herramientas (Tools)

Una **herramienta** es una interfaz (función, API o servicio) que el agente invoca para interactuar con datos o realizar acciones.

Ejemplos:  
🧩 `Search`, `Database`, `Email`, `OCR`, `S3/MinIO`, `HTTP APIs`

```
Usuario → Agente ↔ LLM Core ↔ Tools ↔ Mundo real
```

Note:
- Comentar validación, errores, y observabilidad al llamar herramientas.

---

## Frameworks para agentes

- **LangChain** (Py/JS): pipelines + tools  
- **CrewAI** (Py): multiagente colaborativo  
- **LlamaIndex** (Py): RAG + memoria  
- **AutoGen** (Py): patrones multiagente  
- **MCP** (Py/Go): protocolo universal de tools

| Framework | Foco | Nivel |
|------------|------|-------|
| LangChain | Pipelines | Medio |
| CrewAI | Multiagente | Avanzado |
| LlamaIndex | RAG | Medio |
| MCP | Integración universal | Avanzado |

Note:
- Recalcar que elegimos stack local reproducible: Open WebUI + Ollama + Tools/MCP.

---

## Nuestro Stack

```
Usuario → Open WebUI (frontend)
             ↓
         Ollama (LLM local)
             ↓
    Tools (Open WebUI / MCP)
             ↓
    Datos y Servicios (DB, S3, Email, HTTP)
```

- **Open WebUI:** interfaz moderna  
- **Ollama:** motor local (Llama, Mistral, Gemma)  
- **Tools:** acceso al mundo real

Note:
- Mencionar devcontainer para estandarizar entorno.

---

## Interacción agente–usuario–tool

```
┌────────┐    Prompt/Respuesta    ┌─────────────┐
│ Usuario│ ─────────────────────► │ Open WebUI  │
└────────┘ ◄───────────────────── │ (Agente)    │
                                  └──────┬──────┘
                                         │ Solicita contexto
                                         ▼
                                   ┌──────────┐
                                   │ Ollama   │
                                   │ (LLM)    │
                                   └─────┬────┘
                                         │ Decide usar tool
                                         ▼
                               ┌────────────────────┐
                               │ Tool: `buscar_doc` │
                               │ (HTTP / DB)        │
                               └────────┬───────────┘
                                        │ Resultados
                                        ▼
                                   ┌─────────────┐
                                   │ Observación │
                                   └─────┬───────┘
                                         │
                                         ▼
                                   ┌──────────┐
                                   │ Respuesta│
                                   └─────┬────┘
                                         │
                                         ▼
┌────────┐  Entrega final contextual ┌─────────────┐
│ Usuario│ ◄──────────────────────── │ Open WebUI  │
└────────┘                           └─────────────┘
```

Note:
- Explicar cómo el agente usa el LLM para razonar y decide cuándo invocar la tool.
- Ejemplificar con tool concreta: `buscar_doc` que devuelve contexto antes de responder.

---

## Open WebUI Tools vs MCP Tools

| Aspecto | Open WebUI Tool | MCP Tool |
|----------|----------------|-----------|
| Modelo | Función local | Servicio MCP |
| Ejecución | Dentro de WebUI | Servidor MCP externo |
| Interoperabilidad | Local | Entre agentes y plataformas |
| Seguridad | Local | Aislamiento por proceso/servidor |
| Reuso | Orientado a proyecto | Orientado a ecosistema |

**Idea clave:** MCP conecta agentes con herramientas de forma **segura, portable y reutilizable**.

Note:
- Cuando usar WebUI Tools (rápido/local) vs MCP (escalable/reutilizable).

---

## Extender Open WebUI

Pasos típicos:
1. Definir la herramienta (`tools/`)
2. Describir el contrato (inputs/outputs)
3. Registrar en `tools.json`
4. Probar en WebUI

Ejemplo:

```json
{
  "name": "ocr_image_tool",
  "description": "Extrae texto de imágenes",
  "schema": {"path": "string"},
  "handler": "tools.ocr_image:run"
}
```

Note:
- Buenas prácticas: logs, validación, timeouts y tests.

---

### Ejemplo conceptual — MCP server mínimo

```python
from fastmcp import MCPServer, tool

app = MCPServer("demo-mcp")

@tool()
def email_count(inbox: str) -> int:
    "Devuelve el número de emails en un buzón"
    return 42

if __name__ == "__main__":
    app.run()
```

Note:
- Explicar descubrimiento de tools via MCP y consumo desde Open WebUI.

---

## Roadmap del taller

- Instalar Open WebUI + Ollama (devcontainers)
- Crear el primer agente con una Tool
- Conectar un MCP server (correo / S3 / DB)
- Memoria y planificación (prompting + patterns)
- Logs, trazas, tests y buenas prácticas

Note:
- Reforzar que veremos ejemplos reales conectados a datos locales.

---

## ¡Listos para construir!

👉 Próxima sesión: entorno listo + primer agente funcional.  
🎯 Objetivo: agente que usa una Tool real y ejecuta una acción medible.

Note:
- Dejar 5' para preguntas y setup de la siguiente clase.
