import os
import re
import json
import csv
from tkinter import Tk, Label, Entry, Button, filedialog, IntVar, Checkbutton, Toplevel, messagebox, Text

HISTORIAL_FILE = "historial.json"

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def guardar_historial(historial):
    with open(HISTORIAL_FILE, 'w', encoding='utf-8') as file:
        json.dump(historial, file, ensure_ascii=False, indent=4)

def mostrar_vista_previa_navegable(archivos, reemplazos):
    """
    Muestra una ventana emergente con la vista previa de los archivos procesados.
    Navegación: Siguiente, Anterior, Ejecutar.
    """
    if not archivos:
        messagebox.showinfo("Vista previa", "No se encontraron archivos con coincidencias.")
        return

    indice = [0]  # Mutable para ser actualizado por botones

    def actualizar_vista():
        archivo = archivos[indice[0]]
        with open(archivo, 'r', encoding='utf-8') as file:
            contenido = file.read()

        nuevo_contenido = contenido
        for patron, reemplazo in reemplazos:
            nuevo_contenido = re.sub(patron, reemplazo, nuevo_contenido)

        text_antes.config(state="normal")
        text_antes.delete("1.0", "end")
        text_antes.insert("1.0", contenido)
        text_antes.config(state="disabled")

        text_despues.config(state="normal")
        text_despues.delete("1.0", "end")
        text_despues.insert("1.0", nuevo_contenido)
        text_despues.config(state="disabled")

        label_archivo.config(text=f"Archivo: {archivo}")

    def siguiente():
        if indice[0] < len(archivos) - 1:
            indice[0] += 1
            actualizar_vista()

    def anterior():
        if indice[0] > 0:
            indice[0] -= 1
            actualizar_vista()

    def ejecutar_actual():
        archivo = archivos[indice[0]]
        with open(archivo, 'r', encoding='utf-8') as file:
            contenido = file.read()

        nuevo_contenido = contenido
        for patron, reemplazo in reemplazos:
            nuevo_contenido = re.sub(patron, reemplazo, nuevo_contenido)

        with open(archivo, 'w', encoding='utf-8') as file:
            file.write(nuevo_contenido)

        messagebox.showinfo("Ejecutado", f"Reemplazos aplicados en: {archivo}")
        actualizar_vista()

    # Crear la ventana de vista previa
    ventana_previa = Toplevel()
    ventana_previa.title("Vista previa navegable")

    label_archivo = Label(ventana_previa, text="")
    label_archivo.pack()

    Label(ventana_previa, text="Antes:").pack(anchor="w")
    text_antes = Text(ventana_previa, wrap="word", height=10, width=80)
    text_antes.pack()

    Label(ventana_previa, text="Después:").pack(anchor="w")
    text_despues = Text(ventana_previa, wrap="word", height=10, width=80)
    text_despues.pack()

    Button(ventana_previa, text="Anterior", command=anterior).pack(side="left", padx=10)
    Button(ventana_previa, text="Siguiente", command=siguiente).pack(side="left", padx=10)
    Button(ventana_previa, text="Ejecutar en este archivo", command=ejecutar_actual).pack(side="left", padx=10)
    Button(ventana_previa, text="Cerrar", command=ventana_previa.destroy).pack(side="left", padx=10)

    actualizar_vista()

def buscar_y_reemplazar(directorio, reemplazos, incluir_formatos, excluir_formatos, backup, exportar):
    resultados = []
    archivos_con_coincidencias = []

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
                    archivos_con_coincidencias.append(ruta_archivo)
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

    return archivos_con_coincidencias

def mostrar_historial():
    """
    Muestra el historial de expresiones regulares en una ventana emergente.
    """
    ventana_historial = Toplevel()
    ventana_historial.title("Historial de Expresiones Regulares")

    Label(ventana_historial, text="Historial de expresiones regulares:").pack()
    text_historial = Text(ventana_historial, wrap="word", height=15, width=50)
    text_historial.pack()

    for item in historial:
        text_historial.insert("end", f"Expresión: {item['patron']} -> Reemplazo: {item['reemplazo']}\n")

    Button(ventana_historial, text="Cerrar", command=ventana_historial.destroy).pack(pady=5)

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

Button(ventana, text="Vista Previa", command=lambda: mostrar_vista_previa_navegable(
    buscar_y_reemplazar(
        entrada_directorio.get(), reemplazos, [], [], backup_var.get(), False
    ),
    reemplazos
)).grid(row=3, column=1)

Button(ventana, text="Historial", command=mostrar_historial).grid(row=4, column=1)

reemplazos = []
backup_var = IntVar()
Checkbutton(ventana, text="Crear respaldos", variable=backup_var).grid(row=5, column=1, sticky="w")

ventana.mainloop()
