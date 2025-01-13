import os
import re
import json
import csv
from tkinter import Tk, Label, Entry, Button, filedialog, IntVar, Checkbutton, Toplevel, messagebox, Text
from shutil import copy2

HISTORIAL_FILE = "historial.json"

def cargar_historial():
    """
    Carga el historial de expresiones regulares desde un archivo JSON.
    """
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def guardar_historial(historial):
    """
    Guarda el historial de expresiones regulares en un archivo JSON.
    """
    with open(HISTORIAL_FILE, 'w', encoding='utf-8') as file:
        json.dump(historial, file, ensure_ascii=False, indent=4)

def mostrar_vista_previa(directorio, patron, reemplazo, incluir_formatos, excluir_formatos):
    """
    Muestra una ventana emergente con la vista previa del primer archivo procesado correctamente.
    """
    try:
        patron_compilado = re.compile(patron)
    except re.error as e:
        messagebox.showinfo("Error", f"Expresión regular inválida: {e}")
        return

    for root, _, files in os.walk(directorio):
        for archivo in files:
            if incluir_formatos and not any(archivo.endswith(ext) for ext in incluir_formatos):
                continue
            if excluir_formatos and any(archivo.endswith(ext) for ext in excluir_formatos):
                continue

            ruta_archivo = os.path.join(root, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    contenido = file.read()

                if re.search(patron_compilado, contenido):
                    nuevo_contenido = re.sub(patron_compilado, reemplazo, contenido)

                    ventana_previa = Toplevel()
                    ventana_previa.title(f"Vista previa: {archivo}")

                    Label(ventana_previa, text="Antes:").pack(anchor="w")
                    text_antes = Text(ventana_previa, wrap="word", height=10, width=80)
                    text_antes.insert("1.0", contenido)
                    text_antes.config(state="disabled")
                    text_antes.pack()

                    Label(ventana_previa, text="Después:").pack(anchor="w")
                    text_despues = Text(ventana_previa, wrap="word", height=10, width=80)
                    text_despues.insert("1.0", nuevo_contenido)
                    text_despues.config(state="disabled")
                    text_despues.pack()

                    Button(ventana_previa, text="Cerrar", command=ventana_previa.destroy).pack(pady=5)
                    return
            except Exception as e:
                print(f"Error al procesar {ruta_archivo}: {e}")

    messagebox.showinfo("Vista previa", "No se encontraron archivos con coincidencias.")

def buscar_y_reemplazar(directorio, reemplazos, incluir_formatos, excluir_formatos, backup, exportar):
    """
    Busca y reemplaza texto en los archivos de un directorio para múltiples expresiones regulares.
    """
    resultados = []

    for root, _, files in os.walk(directorio):
        for archivo in files:
            if incluir_formatos and not any(archivo.endswith(ext) for ext in incluir_formatos):
                continue
            if excluir_formatos and any(archivo.endswith(ext) for ext in excluir_formatos):
                continue

            ruta_archivo = os.path.join(root, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    contenido = file.read()

                cambios_realizados = 0
                nuevo_contenido = contenido
                for patron, reemplazo in reemplazos:
                    nuevo_contenido, cantidad = re.subn(patron, reemplazo, nuevo_contenido)
                    cambios_realizados += cantidad

                if cambios_realizados > 0:
                    if backup:
                        respaldo = ruta_archivo + '.bak'
                        copy2(ruta_archivo, respaldo)

                    with open(ruta_archivo, 'w', encoding='utf-8') as file:
                        file.write(nuevo_contenido)

                    resultados.append((ruta_archivo, cambios_realizados))

            except Exception as e:
                print(f"Error al procesar {ruta_archivo}: {e}")

    if exportar:
        with open("resultados.csv", 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Archivo", "Cambios realizados"])
            writer.writerows(resultados)

    messagebox.showinfo("Completado", f"Reemplazo completado en {len(resultados)} archivo(s).")

def agregar_reemplazo():
    """
    Agrega una nueva expresión regular y su reemplazo a la lista de reemplazos.
    """
    patron = entrada_patron.get()
    reemplazo = entrada_reemplazo.get()
    if patron and reemplazo:
        reemplazos.append((patron, reemplazo))
        historial.append({"patron": patron, "reemplazo": reemplazo})
        guardar_historial(historial)
        messagebox.showinfo("Agregado", f"Expresión '{patron}' -> '{reemplazo}' añadida.")
    else:
        messagebox.showinfo("Error", "Por favor, completa ambos campos.")

# Cargar historial
historial = cargar_historial()

# Crear la interfaz gráfica
ventana = Tk()
ventana.title("Buscar y Reemplazar en Archivos")

Label(ventana, text="Directorio:").grid(row=0, column=0, sticky="w")
entrada_directorio = Entry(ventana, width=50)
entrada_directorio.grid(row=0, column=1)
Button(ventana, text="Seleccionar", command=lambda: entrada_directorio.insert(0, filedialog.askdirectory())).grid(row=0, column=2)

Label(ventana, text="Expresión Regular:").grid(row=1, column=0, sticky="w")
entrada_patron = Entry(ventana, width=50)
entrada_patron.grid(row=1, column=1)

Label(ventana, text="Reemplazo:").grid(row=2, column=0, sticky="w")
entrada_reemplazo = Entry(ventana, width=50)
entrada_reemplazo.grid(row=2, column=1)

Button(ventana, text="Agregar Reemplazo", command=agregar_reemplazo).grid(row=3, column=1, pady=5)

Button(ventana, text="Vista Previa", command=lambda: mostrar_vista_previa(
    entrada_directorio.get(),
    entrada_patron.get(),
    entrada_reemplazo.get(),
    [],
    []
)).grid(row=4, column=1, pady=5)

Button(ventana, text="Ejecutar", command=lambda: buscar_y_reemplazar(
    entrada_directorio.get(),
    reemplazos,
    [],
    [],
    backup_var.get(),
    exportar_var.get()
)).grid(row=5, column=1, pady=10)

backup_var = IntVar()
Checkbutton(ventana, text="Crear respaldos", variable=backup_var).grid(row=6, column=1, sticky="w")

exportar_var = IntVar()
Checkbutton(ventana, text="Exportar resultados", variable=exportar_var).grid(row=7, column=1, sticky="w")

reemplazos = []

ventana.mainloop()
