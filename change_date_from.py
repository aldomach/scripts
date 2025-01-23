import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def generar_nombre_log():
    # Genera un nombre único para el archivo de log basado en la fecha y hora
    return f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def seleccionar_carpeta(variable):
    # Abre el cuadro de diálogo para seleccionar una carpeta y asigna la ruta a la variable
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta")
    variable.set(carpeta)

def comparar_y_actualizar():
    if not carpeta_origen.get() or not carpeta_destino.get():
        messagebox.showerror("Error", "Por favor, ingrese ambas rutas antes de continuar.")
        return
    
    archivos_origen = obtener_archivos(carpeta_origen.get())
    archivos_destino = obtener_archivos(carpeta_destino.get())

    # Contamos cuántos archivos se van a actualizar
    archivos_a_actualizar = 0
    for archivo_relativo, ruta_origen in archivos_origen.items():
        if archivo_relativo in archivos_destino:
            archivos_a_actualizar += 1

    if archivos_a_actualizar == 0:
        messagebox.showinfo("Nada para actualizar", "No se encontraron archivos que actualizar.")
        return

    # Mensaje de confirmación con la cantidad de archivos que se van a actualizar
    confirmacion = messagebox.askyesno("Confirmación", f"Se van a actualizar las fechas de {archivos_a_actualizar} archivos. ¿Deseas continuar?")
    if not confirmacion:
        return
    
    log_filename = generar_nombre_log()
    with open(log_filename, 'w') as log_file:
        log_file.write(f"Log generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        actualizados = 0
        for archivo_relativo, ruta_origen in archivos_origen.items():
            ruta_destino = archivos_destino.get(archivo_relativo)
            if ruta_destino and os.path.isfile(ruta_destino):
                # Guardamos la fecha original antes de actualizarla
                fecha_origen = os.path.getmtime(ruta_origen)
                fecha_destino = os.path.getmtime(ruta_destino)
                
                # Actualizamos la fecha del archivo de destino
                os.utime(ruta_destino, (fecha_origen, fecha_origen))
                
                # Escribimos la información en el log (fecha original y nueva fecha)
                log_file.write(f"Actualizado: {archivo_relativo} - {ruta_destino} | Fecha original: {datetime.fromtimestamp(fecha_destino).strftime('%Y-%m-%d %H:%M:%S')} | Nueva fecha: {datetime.fromtimestamp(fecha_origen).strftime('%Y-%m-%d %H:%M:%S')}\n")
                actualizados += 1

        log_file.write(f"\nTotal de archivos actualizados: {actualizados}\n")
    
    messagebox.showinfo("Proceso finalizado", f"Se actualizaron las fechas de {actualizados} archivos.\nLog guardado en {log_filename}")

def obtener_archivos(carpeta):
    archivos = {}
    # Recorremos los archivos en la carpeta, incluidos los subdirectorios y los archivos de la raíz
    for raiz, _, archivos_en_carpeta in os.walk(carpeta):
        for archivo in archivos_en_carpeta:
            ruta_absoluta = os.path.join(raiz, archivo)
            ruta_relativa = os.path.relpath(ruta_absoluta, carpeta)
            archivos[ruta_relativa] = ruta_absoluta
    return archivos

# Configuración de la UI
root = tk.Tk()
root.title("Comparador de carpetas")

# Agregar un mensaje explicativo
mensaje_explicativo = tk.Label(root, text="Este programa permite comparar dos carpetas y actualizar las fechas de modificación de los archivos en la carpeta de destino, basándose en los archivos de la carpeta de origen.", wraplength=400, justify="left")
mensaje_explicativo.pack(padx=20, pady=10)

carpeta_origen = tk.StringVar()
carpeta_destino = tk.StringVar()

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Carpeta de origen
label_origen = tk.Label(frame, text="Carpeta de origen:")
label_origen.pack(fill="x")

frame_origen = tk.Frame(frame)
frame_origen.pack(fill="x", pady=5)

entry_origen = tk.Entry(frame_origen, textvariable=carpeta_origen, width=40)
entry_origen.pack(side="left", fill="x", padx=5)

boton_origen = tk.Button(frame_origen, text="Seleccionar...", command=lambda: seleccionar_carpeta(carpeta_origen))
boton_origen.pack(side="right")

# Carpeta de destino
label_destino = tk.Label(frame, text="Carpeta de destino:")
label_destino.pack(fill="x")

frame_destino = tk.Frame(frame)
frame_destino.pack(fill="x", pady=5)

entry_destino = tk.Entry(frame_destino, textvariable=carpeta_destino, width=40)
entry_destino.pack(side="left", fill="x", padx=5)

boton_destino = tk.Button(frame_destino, text="Seleccionar...", command=lambda: seleccionar_carpeta(carpeta_destino))
boton_destino.pack(side="right")

# Botón para comparar y actualizar
boton_comparar = tk.Button(frame, text="Comparar y actualizar fechas", command=comparar_y_actualizar)
boton_comparar.pack(pady=20)

root.mainloop()
