import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
import subprocess
import logging

def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    return directorio

def seleccionar_directorio_origen():
    directorio = seleccionar_directorio()
    entrada_origen.delete(0, tk.END)
    entrada_origen.insert(0, directorio)

def seleccionar_directorio_destino():
    directorio = seleccionar_directorio()
    entrada_destino.delete(0, tk.END)
    entrada_destino.insert(0, directorio)

def seleccionar_directorio_libreoffice():
    directorio = seleccionar_directorio()
    entrada_libreoffice.delete(0, tk.END)
    entrada_libreoffice.insert(0, directorio)

def generar_log():
    nombre_log = datetime.now().strftime('log_%Y%m%d_%H%M%S.txt')
    logging.basicConfig(filename=nombre_log, level=logging.INFO)
    return nombre_log

def convertir_archivo(ruta_completa, archivo_salida, libreoffice_path):
    comando = f'"{libreoffice_path}" --headless --convert-to pdf "{ruta_completa}" --outdir "{os.path.dirname(archivo_salida)}"'
    subprocess.call(comando, shell=True)
    shutil.move(os.path.join(os.path.dirname(ruta_completa), os.path.basename(archivo_salida)), archivo_salida)
    shutil.copystat(ruta_completa, archivo_salida)

def analizar_carpeta(origen, destino, libreoffice_path, extensiones):
    log_file = generar_log()
    logging.info(f"Conversión iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for root, _, files in os.walk(origen):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensiones):
                ruta_completa = os.path.join(root, file)
                estructura_relativa = os.path.relpath(root, origen)
                carpeta_destino = os.path.join(destino, estructura_relativa)
                os.makedirs(carpeta_destino, exist_ok=True)
                archivo_salida = os.path.join(carpeta_destino, f"{os.path.splitext(file)[0]}.pdf")
                try:
                    convertir_archivo(ruta_completa, archivo_salida, libreoffice_path)
                    logging.info(f"Convertido: {ruta_completa} -> {archivo_salida}")
                except Exception as e:
                    logging.error(f"Error al convertir {ruta_completa}: {str(e)}")
    logging.info(f"Conversión finalizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def convertir():
    origen = entrada_origen.get()
    destino = entrada_destino.get()
    libreoffice_path = os.path.join(entrada_libreoffice.get(), 'program\\soffice.exe')
    guardar_otra_ubicacion = chk_estado.get()
    extensiones = [ext for ext, var in extension_vars.items() if var.get()]
    if guardar_otra_ubicacion:
        destino = entrada_destino.get()
    else:
        destino = origen
    analizar_carpeta(origen, destino, libreoffice_path, extensiones)

ventana = tk.Tk()
ventana.title("Conversor de Archivos a PDF usando LibreOffice")

descripcion = tk.Label(ventana, text="Esta aplicación convierte archivos a PDF utilizando LibreOffice. Puedes seleccionar las extensiones de los archivos a convertir, la carpeta de origen y destino, y otras opciones.")
descripcion.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

tk.Label(ventana, text="Directorio de Origen:").grid(row=1, column=0, padx=10, pady=5)
entrada_origen = tk.Entry(ventana, width=50)
entrada_origen.grid(row=1, column=1, padx=10, pady=5)
tk.Button(ventana, text="Seleccionar", command=seleccionar_directorio_origen).grid(row=1, column=2, padx=10, pady=5)

tk.Label(ventana, text="Directorio de Destino:").grid(row=2, column=0, padx=10, pady=5)
entrada_destino = tk.Entry(ventana, width=50)
entrada_destino.grid(row=2, column=1, padx=10, pady=5)
tk.Button(ventana, text="Seleccionar", command=seleccionar_directorio_destino).grid(row=2, column=2, padx=10, pady=5)

tk.Label(ventana, text="Ruta de LibreOffice:").grid(row=3, column=0, padx=10, pady=5)
entrada_libreoffice = tk.Entry(ventana, width=50)
entrada_libreoffice.grid(row=3, column=1, padx=10, pady=5)
entrada_libreoffice.insert(0, "c:\\Program Files\\LibreOffice")
tk.Button(ventana, text="Seleccionar", command=seleccionar_directorio_libreoffice).grid(row=3, column=2, padx=10, pady=5)

tk.Label(ventana, text="Extensiones a convertir:").grid(row=4, column=0, padx=10, pady=5, sticky="nw")
extension_vars = {
    '.doc': tk.IntVar(),
    '.docx': tk.IntVar(),
    '.xls': tk.IntVar(),
    '.xlsx': tk.IntVar(),
    '.ppt': tk.IntVar(),
    '.pptx': tk.IntVar()
}
for i, ext in enumerate(extension_vars.keys(), 1):
    tk.Checkbutton(ventana, text=ext, variable=extension_vars[ext]).grid(row=i + 4, column=0, padx=10, pady=2, sticky="w")

chk_estado = tk.IntVar()
chk_guardar = tk.Checkbutton(ventana, text="Guardar en otra ubicación", variable=chk_estado)
chk_guardar.grid(row=4, column=1, padx=10, pady=5, sticky="w")

tk.Button(ventana, text="Convertir", command=convertir).grid(row=6, column=1, padx=10, pady=20)

ventana.mainloop()
