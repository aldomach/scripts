import os
import platform
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
import subprocess

def ajustar_ruta(ruta):
    # Normaliza la ruta y cambia las barras según el sistema operativo
    ruta = os.path.normpath(ruta)
    if platform.system() == "Windows":
        return ruta.replace('\\', '/')
    return ruta

def seleccionar_directorio_origen():
    directorio = filedialog.askdirectory()
    entrada_origen.delete(0, tk.END)
    entrada_origen.insert(0, directorio)

def seleccionar_directorio_destino():
    directorio = filedialog.askdirectory()
    entrada_destino.delete(0, tk.END)
    entrada_destino.insert(0, directorio)

def generar_nombre_unico(ruta):
    """
    Genera un nombre único para un archivo si ya existe en la ruta especificada.
    Agrega un sufijo numérico antes de la extensión del archivo.
    """
    base, extension = os.path.splitext(ruta)
    contador = 1
    while os.path.exists(ruta):
        ruta = f"{base}_{contador}{extension}"
        contador += 1
    return ruta

def generar_script():
    origen = entrada_origen.get()
    destino = entrada_destino.get()
    calidad = calidad_combobox.get()
    software = entrada_software.get()

    # Generar el nombre del archivo con la fecha y hora actual
    archivo_bat = datetime.now().strftime('script_%Y%m%d_%H%M%S.bat')

    # Generar el archivo .bat
    with open(archivo_bat, 'w') as f:
        for root, dirs, files in os.walk(origen):
            for file in files:
                # Filtrar solo los archivos .pdf
                if file.lower().endswith('.pdf'):
                    ruta_completa = ajustar_ruta(os.path.join(root, file))

                    # Obtener la ruta relativa del archivo respecto al directorio de origen
                    ruta_relativa = os.path.relpath(ruta_completa, origen)

                    # Crear la ruta de salida completa, replicando la estructura de carpetas
                    archivo_salida = ajustar_ruta(os.path.join(destino, ruta_relativa))

                    # Crear los directorios necesarios en el destino
                    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

                    # Verificar si el archivo ya existe y generar un nombre único si es necesario
                    archivo_salida = generar_nombre_unico(archivo_salida)

                    # Escribir el comando en el archivo .bat
                    comando = f'"{ajustar_ruta(software)}" "{ruta_completa}" -applyProfile -profile "{calidad}" -outputFile "{archivo_salida}"\n'
                    f.write(comando)

    print(f'Se ha generado el archivo .bat: {archivo_bat}')
    return archivo_bat


def generar_y_ejecutar_script():
    archivo_bat = generar_script()
    subprocess.call([archivo_bat], shell=True)

ventana = tk.Tk()
ventana.title("Generador de PDF")

# Descripción al usuario sobre la función de la aplicación
descripcion = "Esta aplicación genera un archivo de script .bat que comprime\n" \
              "archivos PDF utilizando el software PDF24, copiándolos a\n" \
              "un directorio de destino. Mantiene la estructura de carpetas\n" \
              "original y asegura que no se sobrescriban archivos existentes."

tk.Label(ventana, text=descripcion, wraplength=400, justify="left").grid(row=0, column=0, columnspan=3, padx=10, pady=10)

tk.Label(ventana, text="Directorio de Origen:").grid(row=1, column=0, padx=10, pady=5)
entrada_origen = tk.Entry(ventana, width=50)
entrada_origen.grid(row=1, column=1, padx=10, pady=5)
tk.Button(ventana, text="Seleccionar", command=seleccionar_directorio_origen).grid(row=1, column=2, padx=10, pady=5)

tk.Label(ventana, text="Directorio de Destino:").grid(row=2, column=0, padx=10, pady=5)
entrada_destino = tk.Entry(ventana, width=50)
entrada_destino.grid(row=2, column=1, padx=10, pady=5)
tk.Button(ventana, text="Seleccionar", command=seleccionar_directorio_destino).grid(row=2, column=2, padx=10, pady=5)

tk.Label(ventana, text="Ruta del Software:").grid(row=3, column=0, padx=10, pady=5)
entrada_software = tk.Entry(ventana, width=50)
entrada_software.grid(row=3, column=1, padx=10, pady=5)
entrada_software.insert(0, "c:\\Program Files\\PDF24\\pdf24-DocTool.exe")

tk.Label(ventana, text="Calidad:").grid(row=4, column=0, padx=10, pady=5)
calidades = ["default/good", "default/high", "default/best", "default/medium", "default/low", "default/fax"]
calidad_combobox = ttk.Combobox(ventana, values=calidades, state="readonly")
calidad_combobox.grid(row=4, column=1, padx=10, pady=5)
calidad_combobox.set("default/medium")

tk.Button(ventana, text="Generar Script", command=generar_script).grid(row=5, column=0, padx=10, pady=20)
tk.Button(ventana, text="Generar y Ejecutar Script", command=generar_y_ejecutar_script).grid(row=5, column=1, padx=10, pady=20)

ventana.mainloop()
