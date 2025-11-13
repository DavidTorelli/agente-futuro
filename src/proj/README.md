# Proyectos

## Guia autismo
Descripcion: Realizar un agente que guie a las familias que tienen personas con autismo a su cargo.
* Requisitos: Definir las bases de conocimiento.

## Agricultura:
* Base de conocimientos de cultivos por temporada.
* Herramientas
    * Clima: Acceso a condiciones meteorologicas y alertas
    * Notificacion: Enviar notificaciones de prevision segun las alertas detectadas.

## Planificacion de eventos:
Descripcion: Herramienta que se conecta a un correo, escanea los que son relacionados con eventos y extrae la informacion necesaria para dar una propuesta, preparando un borrador de un correo.
* Base de conocimiento: Salas, tipos de eventos, clientes/ponentes potenciales, caledario
* Herramientas:
    * Acceso a correo electronico
    * Planificar la seleccion de clientes con la base de conocimientos 
    * Acceso a hoja de calculos

## Seguimiento de matriculas de contenedores del puerto
Descripcion: Subir fotografias de contenedores. Detectar matriculas y generar una hoja excel con las matriculas detectadas.
* Herramientas:
    * Procesamiento de imagenes:
        * Deteccion de matriculas con recorte de foto.
        * OCR: Extraccion de letras y numeros a partir de una imagen (teseract)
    * Generador de excel