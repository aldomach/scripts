# Descripción del Script: Buscar y Reemplazar en Archivos

Este script en Python permite realizar un proceso de búsqueda y reemplazo de texto en archivos de un directorio específico mediante una interfaz gráfica utilizando la librería `Tkinter`. Los elementos clave de este script son:

## 1. Interfaz Gráfica (GUI)
La interfaz está creada con `Tkinter`, permitiendo al usuario seleccionar un directorio, ingresar una expresión regular y un texto de reemplazo, y especificar formatos de archivo a incluir o excluir.
- **Campos de entrada**:
  - Directorio de trabajo
  - Expresión regular para buscar el texto
  - Texto de reemplazo
  - Formatos de archivo a incluir o excluir
- **Opción adicional**:
  - Opción para crear un respaldo de los archivos antes de realizar cualquier reemplazo.

## 2. Funciones Principales
- **`mostrar_ayuda()`**: Abre una ventana emergente que muestra ejemplos de expresiones regulares comunes (fechas, correos electrónicos, URLs, números de teléfono, palabras específicas).
- **`buscar_y_reemplazar()`**: Realiza la búsqueda y reemplazo en los archivos del directorio seleccionado, según los parámetros dados. Usa la expresión regular proporcionada para encontrar el texto y luego lo reemplaza. Además, permite excluir ciertos formatos de archivo y hacer respaldos de los archivos antes de modificar su contenido.
- **`agregar_directorio()`**: Permite al usuario seleccionar el directorio a través de un cuadro de diálogo.
- **`ejecutar_reemplazo()`**: Ejecuta el proceso de búsqueda y reemplazo usando los parámetros que el usuario ha configurado en la interfaz.

## 3. Características Adicionales
- **Soporte para respaldo**: Se puede crear una copia de seguridad de los archivos antes de realizar modificaciones (usando la opción de "Crear respaldo antes de reemplazar").
- **Filtros por formato**: El usuario puede definir qué formatos de archivo se deben incluir o excluir para la operación de búsqueda y reemplazo, como archivos `.md`, `.txt`, etc.
- **Interacción con el usuario**: El script muestra ventanas emergentes para informar sobre errores (como una expresión regular inválida) y notificaciones de éxito o finalización del proceso.

## Propósito
El propósito de este script es proporcionar una herramienta sencil
