import os
import re
from tkinter import Tk, Label, Entry, Button, filedialog, IntVar, Checkbutton, messagebox
from shutil import copy2

def mostrar_ayuda():
    """
    Muestra una ventana emergente con ejemplos de expresiones regulares.
    """
    ejemplos = (
        "1. Fechas en formato DD/MM/AAAA:\n    Expresión: (\\d{2})/(\\d{2})/(\\d{4})\n    Reemplazo: [[\\3-\\2-\\1]]\n",
        "2. Correos electrónicos:\n    Expresión: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\n    Reemplazo: [REDACTED_EMAIL]\n",
        "3. URLs:\n    Expresión: https?://[^\\s]+\n    Reemplazo: [LINK]\n",
        "4. Números de teléfono:\n    Expresión: \\+?[0-9]{1,3}[-\\s]?[(]?[0-9]{1,4}[)]?[-\\s]?[0-9\\s-]{6,}\n    Reemplazo: [PHONE_NUMBER]\n",
        "5. Palabras específicas (ejemplo: 'error'):\n    Expresión: \\berror\\b\n    Reemplazo: problema\n"
    )
    messagebox.showinfo("Ayuda: Ejemplos de Expresiones Regulares", "\n".join(ejemplos))

def buscar_y_reemplazar(directorio, patron, reemplazo, incluir_formatos, excluir_formatos, backup):
    """
    Busca y reemplaza texto en los archivos de un directorio según una expresión regular.
    """
    try:
        patron_compilado = re.compile(patron)
    except re.error as e:
        messagebox.showinfo("Error", f"Expresión regular inválida: {e}")
        return

    for root, _, files in os.walk(directorio):
        for archivo in files:
            # Filtra por formatos a incluir y excluir
            if incluir_formatos and not any(archivo.endswith(ext) for ext in incluir_formatos):
                continue
            if excluir_formatos and any(archivo.endswith(ext) for ext in excluir_formatos):
                continue

            ruta_archivo = os.path.join(root, archivo)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    contenido = file.read()

                nuevo_contenido, cantidad = re.subn(patron_compilado, reemplazo, contenido)

                if cantidad > 0:
                    if backup:
                        respaldo = ruta_archivo + '.bak'
                        copy2(ruta_archivo, respaldo)

                    with open(ruta_archivo, 'w', encoding='utf-8') as file:
                        file.write(nuevo_contenido)

                    print(f"Reemplazo completado en: {ruta_archivo}, {cantidad} coincidencias.")
            except Exception as e:
                print(f"Error al procesar {ruta_archivo}: {e}")

def agregar_directorio():
    """
    Abre un cuadro de diálogo para seleccionar el directorio de trabajo.
    """
    directorio = filedialog.askdirectory(title="Selecciona una carpeta")
    entrada_directorio.delete(0, 'end')
    entrada_directorio.insert(0, directorio)

def ejecutar_reemplazo():
    """
    Ejecuta el proceso de búsqueda y reemplazo con los parámetros dados.
    """
    directorio = entrada_directorio.get()
    patron = entrada_patron.get()
    reemplazo = entrada_reemplazo.get()
    incluir_formatos = [formato.strip() for formato in entrada_incluir.get().split(',') if formato.strip()]
    excluir_formatos = [formato.strip() for formato in entrada_excluir.get().split(',') if formato.strip()]
    backup = backup_var.get()

    if not directorio or not patron:
        messagebox.showinfo("Error", "Por favor, llena todos los campos obligatorios.")
        return

    buscar_y_reemplazar(directorio, patron, reemplazo, incluir_formatos, excluir_formatos, backup)
    messagebox.showinfo("Completado", "El reemplazo se ha completado.")

# Crear la interfaz gráfica
ventana = Tk()
ventana.title("Buscar y Reemplazar en Archivos")

# Descripción corta de la aplicación
Label(ventana, text="Esta aplicación permite buscar y reemplazar texto en archivos de un directorio utilizando expresiones regulares.", wraplength=400).grid(row=0, column=0, columnspan=3, pady=10)

Label(ventana, text="Directorio:").grid(row=1, column=0, sticky="w")
entrada_directorio = Entry(ventana, width=50)
entrada_directorio.grid(row=1, column=1)
Button(ventana, text="Seleccionar", command=agregar_directorio).grid(row=1, column=2)

Label(ventana, text="Expresión Regular (buscar):").grid(row=2, column=0, sticky="w")
entrada_patron = Entry(ventana, width=50)
entrada_patron.grid(row=2, column=1, columnspan=2, sticky="w")

Label(ventana, text="Texto de Reemplazo:").grid(row=3, column=0, sticky="w")
entrada_reemplazo = Entry(ventana, width=50)
entrada_reemplazo.grid(row=3, column=1, columnspan=2, sticky="w")

Label(ventana, text="Formatos a incluir (ej.: md, txt):").grid(row=4, column=0, sticky="w")
entrada_incluir = Entry(ventana, width=50)
entrada_incluir.grid(row=4, column=1, columnspan=2, sticky="w")

Label(ventana, text="Formatos a excluir (ej.: log, bak):").grid(row=5, column=0, sticky="w")
entrada_excluir = Entry(ventana, width=50)
entrada_excluir.grid(row=5, column=1, columnspan=2, sticky="w")

backup_var = IntVar()
Checkbutton(ventana, text="Crear respaldo antes de reemplazar", variable=backup_var).grid(row=6, column=1, sticky="w")

Button(ventana, text="Ejecutar", command=ejecutar_reemplazo).grid(row=7, column=1, pady=10)
Button(ventana, text="Ayuda", command=mostrar_ayuda).grid(row=7, column=2, pady=10)

ventana.mainloop()
