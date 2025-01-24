import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import shutil

# Función para convertir archivos a PDF
def convertir_archivos():
    # Obtengo la ruta donde está instalado LibreOffice
    libreoffice_path = libreoffice_entry.get()
    
    if not os.path.exists(libreoffice_path):
        messagebox.showerror("Error", "La ruta de LibreOffice no es válida.")
        return
    
    # Obtengo la carpeta de origen
    carpeta_origen = origen_entry.get()
    
    if not os.path.exists(carpeta_origen):
        messagebox.showerror("Error", "La carpeta de origen no es válida.")
        return
    
    # Si es necesario, obtengo la carpeta de destino
    carpeta_destino = destino_entry.get()
    if guardar_en_otra_var.get() and not os.path.exists(carpeta_destino):
        messagebox.showerror("Error", "La carpeta de destino no es válida.")
        return
    
    # Generar un log único basado en la fecha y hora actual
    log_name = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_name, 'w') as log_file:
        log_file.write(f"Log de conversión - {datetime.now()}\n\n")
        
        # Función recursiva para recorrer directorios
        def procesar_directorio(directorio):
            for root, dirs, files in os.walk(directorio):
                for file in files:
                    archivo_path = os.path.join(root, file)
                    if file.endswith(tuple(extensiones_tildadas)):
                        try:
                            # Definir el comando para LibreOffice
                            output_path = archivo_path.replace(carpeta_origen, carpeta_destino, 1) + ".pdf"
                            # Crear directorio destino si no existe
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                            
                            # Comando de LibreOffice para la conversión
                            command = [libreoffice_path, '--headless', '--convert-to', 'pdf', archivo_path, '--outdir', os.path.dirname(output_path)]
                            subprocess.run(command, check=True)
                            
                            # Copiar la fecha original del archivo
                            timestamp = os.path.getmtime(archivo_path)
                            os.utime(output_path, (timestamp, timestamp))
                            
                            log_file.write(f"Convertido: {archivo_path} -> {output_path}\n")
                        except Exception as e:
                            log_file.write(f"Error en {archivo_path}: {str(e)}\n")
        
        # Procesar la carpeta de origen
        procesar_directorio(carpeta_origen)
    
    messagebox.showinfo("Finalizado", "Conversión completada. Ver log para más detalles.")

# Función para seleccionar carpeta de origen
def seleccionar_origen():
    carpeta = filedialog.askdirectory(initialdir=libreoffice_entry.get())
    if carpeta:
        origen_entry.delete(0, tk.END)
        origen_entry.insert(0, carpeta)

# Función para seleccionar carpeta de destino
def seleccionar_destino():
    carpeta = filedialog.askdirectory()
    if carpeta:
        destino_entry.delete(0, tk.END)
        destino_entry.insert(0, carpeta)

# Función para habilitar o deshabilitar la opción de "Guardar en otra ubicación"
def habilitar_destino(*args):
    if guardar_en_otra_var.get():
        destino_entry.config(state="normal")  # Habilitar campo de texto
        destino_button.config(state="normal")  # Habilitar botón
    else:
        destino_entry.config(state="disabled")  # Deshabilitar campo de texto
        destino_button.config(state="disabled")  # Deshabilitar botón

# Crear la ventana principal
root = tk.Tk()
root.title("Convertidor de Archivos a PDF")

# Descripción del software
descripcion_label = tk.Label(root, text="Este software convierte archivos seleccionados a PDF utilizando LibreOffice.\nEl programa puede convertir archivos en carpetas seleccionadas, manteniendo la estructura original y fechas.")
descripcion_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Ruta de LibreOffice
libreoffice_label = tk.Label(root, text="Ruta de LibreOffice:")
libreoffice_label.grid(row=1, column=0, padx=10, pady=5)
libreoffice_entry = tk.Entry(root, width=40)
libreoffice_entry.insert(0, "C:/Program Files/LibreOffice/program/soffice.exe")  # Ruta por defecto
libreoffice_entry.grid(row=1, column=1, padx=10, pady=5)

# Carpeta de origen
origen_label = tk.Label(root, text="Carpeta de origen:")
origen_label.grid(row=2, column=0, padx=10, pady=5)
origen_entry = tk.Entry(root, width=40)
origen_entry.insert(0, os.getcwd())  # Carpeta actual por defecto
origen_entry.grid(row=2, column=1, padx=10, pady=5)
origen_button = tk.Button(root, text="Seleccionar", command=seleccionar_origen)
origen_button.grid(row=2, column=2, padx=10, pady=5)

# Extensiones de archivos a convertir (Disposición Horizontal)
extensiones_label = tk.Label(root, text="Extensiones a convertir:")
extensiones_label.grid(row=3, column=0, padx=10, pady=5)
extensiones_frame = tk.Frame(root)  # Frame para los checkboxes
extensiones_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

extensiones_tildadas = []
for idx, ext in enumerate(['.docx', '.xlsx', '.pptx', '.odt', '.ods', '.odp']):
    var = tk.BooleanVar(value=True)
    checkbox = tk.Checkbutton(extensiones_frame, text=ext, variable=var)
    checkbox.grid(row=0, column=idx, padx=5)  # Distribuir los checkboxes en una fila
    extensiones_tildadas.append((ext, var))

# Guardar en otra ubicación
guardar_en_otra_var = tk.BooleanVar(value=False)
guardar_en_otra_checkbox = tk.Checkbutton(root, text="Guardar en otra ubicación", variable=guardar_en_otra_var)
guardar_en_otra_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="w")

# Carpeta de destino
destino_label = tk.Label(root, text="Carpeta de destino:")
destino_label.grid(row=5, column=0, padx=10, pady=5)
destino_entry = tk.Entry(root, width=40, state="disabled")  # Inicialmente deshabilitado
destino_entry.grid(row=5, column=1, padx=10, pady=5)
destino_button = tk.Button(root, text="Seleccionar", command=seleccionar_destino, state="disabled")  # Inicialmente deshabilitado
destino_button.grid(row=5, column=2, padx=10, pady=5)

# Vincular la función de habilitación de destino al cambio de la variable BooleanVar
guardar_en_otra_var.trace("w", habilitar_destino)

# Botón para convertir
convertir_button = tk.Button(root, text="Convertir", command=convertir_archivos)
convertir_button.grid(row=6, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()
