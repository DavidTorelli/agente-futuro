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
## Knowledge Base + Tools

---

## Agenda

1. Configurar y usar **Knowledge** (base de conocimiento) en OpenWebUI.
2. Instalar y habilitar **Tools** desde la librería comunitaria.
3. **Crear** Tools propias en Python (3 ejemplos):

  - Número aleatorio,
  - Clima simple por ciudad (argumentos sencillos),
  - Argumentos anidados/avanzados.

---

## Requisitos previos

* OpenWebUI funcionando con **Ollama** (o API OpenAI-compatible).
* Usuario con permisos para **Workspace** y **Tools**.
* Editor integrado de OpenWebUI o acceso para importar herramientas.

---

## 🧠 Knowledge (Base de conocimiento)

- Como se usan?  
Puedes invocarlos en chat con `#nombre`.

- Pasos rápidos

1. **Workspace → Knowledge → New Knowledge** (pon un nombre claro, p. ej. `taller_agentes`).
2. **Upload** documentos (PDF, MD, TXT, etc.).
3. Opcional: añade **tags** y descripciones.
4. En un chat: escribe `#` para seleccionar entradas.

--

### Consejos prácticos

* **Estructura** por colecciones (p. ej. `kb_proyecto`, `kb_legal`, `kb_marketing`).
* **Nombres cortos** y únicos para invocar con `#`.
* Prefiere **TXT/MD** cuando puedas (menos ruido que PDF escaneado).
* Sube documentos **versionados** (añade fecha en el nombre: `guia_facturas_2025-11-01.md`).
* Revisa de vez en cuando el tamaño/duplicados; divide PDFs grandes.

---

## Instalar y habilitar Tools

Instalar desde la librería comunitaria

1. **openwebui.com → Tools** y elige una herramienta.
2. Clic en **Get** → introduce la **URL/IP** de tu OpenWebUI.
3. **Import to WebUI**.
4. Otra opcion es explorar [herramienta](https://openwebui.com/tools) y clicar para importar directamente.

---

## Habilitar bases de conocimiento / tools en un modelo

1. **Workspace → Models**.
2. Edita el modelo (✏️) → sección **Tools**.
3. Marca las Tools que quieras **por defecto** → **Save**.

---

## Crear tu propia Tool

En OpenWebUI, una [Tool](https://docs.openwebui.com/features/plugin/tools/) es un **archivo Python** con:

* **Docstring** superior con metadatos.
* Clase **`Tools`** con métodos (cada método = una tool).
* **Type hints** obligatorios para generar el esquema JSON.

--

## Cómo añadir tu Tool

**Opción A (Marketplace):**

* Sube tu archivo a un repo público y publícalo en la comunidad (opcional). Luego **Get → Import to WebUI**.

**Opción B (desde OpenWebUI):**

1. Ve a **Workspace → Tools**.
2. Clic **+ New Tool** (o **Import** si tienes un JSON/paquete).
3. Pega el **código Python** de arriba y **Save**.
4. Activa la Tool en tu **modelo** (ver sección anterior).

> Nota: asegúrate de que cada función tenga **type hints** y una docstring clara; así el modelo generará el esquema correctamente y sabrá cómo llamarla.

--

### Generemos una herramienta

#### Numeros aleatorios

Usa `random.randint` para generar los numeros y no te olvides de comprobar el rango!

--

```python
import random

class Tools:
    def random_int(self, min_value: int = 0, max_value: int = 100) -> int:
        """
        Devuelve un número entero aleatorio entre min_value y max_value (ambos incluidos).
        :param min_value: límite inferior
        :param max_value: límite superior
        """
        if min_value > max_value:
            raise ValueError("min_value no puede ser mayor que max_value")
        return random.randint(min_value, max_value)
```

--

#### Valves y User Valves

Usando [Valves](https://docs.openwebui.com/features/plugin/valves/)

- Valves expone los parametros de tu herramienta accesible desde openweb ui.
- Valves son globales, mientras que UserValves son especificas para cada usuario.  

--

* Ejercicio: Crea 2 valvulas para controlar el rango [minimo, máximo].

--

```python
class Tools:
    class Valves(BaseModel):
        # Configurables desde la UI si los declaras aquí
        default_min: int = Field(0, description="Mínimo numero a generar en el rango aleatorio")
        default_max: int = Field(100, description="Máximo numero a generar en el rango aleatorio")

    def __init__(self):
        self.valves = self.Valves()

    def random_int(self, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        # Estos logs los veras en el container de openweb ui
        min_value = min_value or self.valves.default_min
        max_value = max_value or self.valves.default_min
        ...
```

--

#### Usando logs

--

```python
    def random_int(self, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        """
        Devuelve un número entero aleatorio. Si no se da un rango lo toma de los valores por defecto, en caso contrario lo genera entre min_value y max_value (ambos incluidos).
        :param min_value: límite inferior
        :param max_value: límite superior
        """
        # Estos logs los veras en el container de openweb ui
        print(f"[random_int] usando rango {min_value}-{max_value} (valves {self.valves.default_min}-{self.valves.default_max})")
        ...
```
--

#### Usando logs como es debido

Usa python logs con el modulo logging.

Y busca las diferencias ...

--

```python
import logging

def _init_logger():
    logger = logging.getLogger('random_tool')
    logger.setLevel(logging.INFO) 

_init_logger()
_logger = logging.getLogger('random_tool')

    def random_int(self, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        # Estos logs los veras en el container ... busca las diferencias
        _logger.info(f"[random_int] usando rango {min_value}-{max_value} (valves {self.valves.default_min}-{self.valves.default_max})")
        print(f"[random_int] usando rango {min_value}-{max_value} (valves {self.valves.default_min}-{self.valves.default_max})")
        ...
```

--

## Buenas prácticas

* **Idempotencia**: que repetir la llamada no rompa nada.
* **Validación**: comprueba/normaliza argumentos; devuelve errores útiles.
* **Tiempos de espera**: usa timeouts en peticiones HTTP.
* **Determinismo** (si aplica): loguea semillas en aleatorios cuando quieras reproducibilidad.
* **Seguridad**: no ejecutes comandos del sistema; valida URLs/inputs si haces fetch.

---

## Extra

* Integra tu **KB** con Tools (p. ej., buscar en KB y luego llamar a otra Tool con el resultado).
