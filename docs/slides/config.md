---
title: Configuración del entorno — Clase 1
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

# Guía rápida de configuración

Cada paso incluye el enlace directo y un código QR listo para proyectar durante la sesión.

---

## 1. Descarga Visual Studio Code

- Visita la página oficial y elige el instalador según tu sistema operativo.
- Enlace: [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)
- Código QR:  
  ![QR VS Code](https://quickchart.io/qr?text=https%3A%2F%2Fcode.visualstudio.com%2FDownload&size=200)

---

## 2. Instala la extensión *Dev Containers*

- Abre VS Code → pestaña **Extensions** → busca `Dev Containers` (ID: `ms-vscode-remote.remote-containers`).
- Enlace: [https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  

--

- Código QR:  
  ![QR Dev Containers](https://quickchart.io/qr?text=https%3A%2F%2Fmarketplace.visualstudio.com%2Fitems%3FitemName%3Dms-vscode-remote.remote-containers&size=200)

---

## 3. Construir y abrir el contenedor

1. Clona el repositorio del taller:  
   ```bash
   git clone https://github.com/DavidTorelli/agente-futuro.git
   cd agent-workshop
   ```
2. Abre la carpeta en VS Code.
3. Ejecuta el comando `Dev Containers: Rebuild and Reopen in Container` desde la paleta (`Ctrl` + `Shift` + `P` / `Cmd` + `Shift` + `P`).

--

4. Espera a que finalice la construcción; VS Code se conectará automáticamente al contenedor.

- Documentación oficial: [https://code.visualstudio.com/docs/devcontainers/containers](https://code.visualstudio.com/docs/devcontainers/containers)
- Código QR:  
  ![QR Docs Dev Containers](https://quickchart.io/qr?text=https%3A%2F%2Fcode.visualstudio.com%2Fdocs%2Fdevcontainers%2Fcontainers&size=200)

---

## 4. Descargar un modelo en Open WebUI

Usa el comando ollama pull desde el contenedor para descargar modelos.
```
docker exec -it ollama bash -lc "ollama pull gemma3:latest
docker exec -it ollama bash -lc "ollama pull gemma3:1b
```
Encontraras los modelos disponibles en la biblioteca de ollama: https://ollama.com/library

O desde la interfaz de usuario: http://localhost:3000/admin/settings/connections 

---

## 5. Crear un chat y realizar el primer prompt

1. En Open WebUI, abre **New Chat**: http://localhost:3000/#/chat
2. Selecciona el modelo descargado desde el desplegable en la parte superior izquierda.
3. Escribe un prompt de prueba, por ejemplo:  
   > "Que tiempo hace hoy en mi ciudad?"
4. Envía el mensaje y verifica la respuesta.
