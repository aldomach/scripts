import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import shutil

stop_conversion = False

# Obtener la carpeta donde está el script
script_directory = os.path.dirname(os.path.abspath(__file__))


# Función para convertir archivos a PDF
def convert_to_pdf(input_path, output_path, libreoffice_path):
    try:
        command = [
            libreoffice_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_path,
            input_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al convertir {input_path} a PDF: {e}")


# Función para copiar la fecha del archivo original al PDF
def copy_file_date(src, dst):
    try:
        timestamp = os.path.getmtime(src)
        os.utime(dst, (timestamp, timestamp))
    except Exception as e:
        raise RuntimeError(f"Error al copiar la fecha del archivo de {src} a {dst}: {e}")


# Función para iniciar la conversión
def start_conversion():
    global stop_conversion
    stop_conversion = False

    # Validaciones de las entradas
    if not os.path.exists(libreoffice_path_var.get()):
        messagebox.showerror("Error", "Ruta de LibreOffice inválida.")
        return

    if not os.path.exists(source_folder_var.get()):
        messagebox.showerror("Error", "Carpeta de origen inválida.")
        return

    if save_to_other_location_var.get():
        if not os.path.exists(destination_folder_var.get()):
            messagebox.showerror("Error", "Carpeta de destino inválida.")
            return

    if not move_option_var.get():
        messagebox.showerror("Error", "Debe seleccionar una opción para mover los archivos originales.")
        return

    extensions_to_convert = [ext for ext, var in checkboxes.items() if var.get()]
    if not extensions_to_convert:
        messagebox.showerror("Error", "No se seleccionaron extensiones para convertir.")
        return

    source_folder = source_folder_var.get()
    dest_folder = destination_folder_var.get() if save_to_other_location_var.get() else source_folder

    # Log
    log_file = os.path.join(dest_folder, f"log_conversion_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    with open(log_file, 'w') as log:
        for root, _, files in os.walk(source_folder):
            if stop_conversion:
                log.write("Conversión detenida por el usuario.\n")
                break
            for file in files:
                if any(file.endswith(ext) for ext in extensions_to_convert):
                    input_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, source_folder)
                    output_dir = os.path.join(dest_folder, relative_path)
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.pdf")

                    try:
                        convert_to_pdf(input_path, output_dir, libreoffice_path_var.get())
                        if maintain_date_var.get() and os.path.exists(output_path):
                            copy_file_date(input_path, output_path)

                        log.write(f"ÉXITO: {file} - {output_path}\n")

                        # Mover archivo original según la opción seleccionada
                        if move_option_var.get() == "mover_si_mas_pequeno":
                            if os.path.exists(output_path):
                                pdf_size = os.path.getsize(output_path)
                                original_size = os.path.getsize(input_path)
                                
                                if pdf_size < original_size:
                                    # Mover el archivo original solo si el PDF es más pequeño
                                    move_folder = move_originals_folder_var.get()
                                    if move_folder:
                                        move_dest_path = os.path.join(move_folder, relative_path, file)
                                        os.makedirs(os.path.dirname(move_dest_path), exist_ok=True)
                                        shutil.move(input_path, move_dest_path)
                                        log.write(f"Archivo original movido a: {move_dest_path}\n")
                                else:
                                    log.write(f"Archivo original NO movido. El PDF es más grande o igual que el archivo de origen.\n")
                        elif move_option_var.get() == "mover_todos":
                            move_folder = move_originals_folder_var.get()
                            if move_folder:
                                move_dest_path = os.path.join(move_folder, relative_path, file)
                                os.makedirs(os.path.dirname(move_dest_path), exist_ok=True)
                                shutil.move(input_path, move_dest_path)
                                log.write(f"Archivo original movido a: {move_dest_path}\n")
                        else:
                            log.write("Opción de mover archivos originales no seleccionada.\n")

                    except Exception as e:
                        log.write(f"FALLÓ: {file} - {e}\n")

    messagebox.showinfo("Conversión Completa", f"Conversión completada. Log guardado en {log_file}")


# Función para detener la conversión
def stop_conversion_process():
    global stop_conversion
    stop_conversion = True


# Función para explorar carpetas
def browse_folder(var):
    folder = filedialog.askdirectory()
    if folder:
        var.set(folder)


# Función para explorar archivos
def browse_file(var):
    file = filedialog.askopenfilename()
    if file:
        var.set(file)


# Función para activar o desactivar la selección de carpeta de destino
def toggle_destination():
    destination_entry.configure(state=tk.NORMAL if save_to_other_location_var.get() else tk.DISABLED)
    destination_button.configure(state=tk.NORMAL if save_to_other_location_var.get() else tk.DISABLED)


# Función para activar o desactivar la selección de mover archivos originales
def toggle_move_originals():
    move_originals_entry.configure(state=tk.NORMAL if move_option_var.get() in ["mover_si_mas_pequeno", "mover_todos"] else tk.DISABLED)
    move_originals_button.configure(state=tk.NORMAL if move_option_var.get() in ["mover_si_mas_pequeno", "mover_todos"] else tk.DISABLED)


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Conversor de Archivos a PDF")
root.geometry("600x730")

# Descripción
tk.Label(root, 
         text="Esta herramienta convierte documentos a PDF utilizando LibreOffice.\n\n "
              "Seleccione la carpeta de origen, las extensiones a convertir, y si desea guardar en otra ubicación o mover los archivos originales. "
              "\n\nPuede mantener la fecha del archivo original si lo desea.", 
         wraplength=550).pack(anchor="w", padx=10, pady=10, fill="x")

# Ruta de LibreOffice
libreoffice_path_var = tk.StringVar(value="C:/Program Files/LibreOffice/program/soffice.exe")
tk.Label(root, text="Ruta de LibreOffice:").pack(anchor="w")
tk.Entry(root, textvariable=libreoffice_path_var).pack(fill="x", padx=10)
tk.Button(root, text="Examinar", command=lambda: browse_file(libreoffice_path_var)).pack(anchor="e", padx=10)

# Carpeta de origen
source_folder_var = tk.StringVar()
tk.Label(root, text="Carpeta de origen:").pack(anchor="w")
tk.Entry(root, textvariable=source_folder_var).pack(fill="x", padx=10)
tk.Button(root, text="Examinar", command=lambda: browse_folder(source_folder_var)).pack(anchor="e", padx=10)

# Texto y Selección de Extensiones
tk.Label(root, text="Seleccionar extensiones a convertir:").pack(anchor="w")

# Diccionario de extensiones por categorías
extensions = {
    "Calc": [".ods", ".xls", ".xlsx"],
    "Write": [".odt", ".doc", ".docx"],
    "Otros": [".ppt", ".pptx", ".rtf", ".txt", ".html", ".xml"]
}

# Variables para controlar si se deben seleccionar todas las extensiones de una categoría
category_vars = {}

# Marco para las casillas de verificación
frame = tk.Frame(root)
frame.pack(pady=10)

# Crear las casillas de verificación para las categorías
for category, exts in extensions.items():
    category_var = tk.BooleanVar()
    category_vars[category] = category_var

    # Crear el checkbox para la categoría
    checkbox = tk.Checkbutton(frame, text=category, variable=category_var, command=lambda category=category: toggle_extensions(category))
    checkbox.grid(row=0, column=list(extensions.keys()).index(category), padx=10, pady=5)

# Casillas de verificación individuales para las extensiones
checkboxes = {}
cols = 7
row_counter = 1

# Generar casillas para todas las extensiones posibles
for ext in [".odt", ".ods", ".odp", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".rtf", ".txt", ".html", ".xml"]:
    var = tk.BooleanVar()
    checkboxes[ext] = var

    # Crear el checkbox para cada extensión
    tk.Checkbutton(frame, text=ext, variable=var).grid(row=row_counter, column=(list(checkboxes.keys()).index(ext) % cols), padx=10, pady=5)

    if len(checkboxes) % cols == 0:
        row_counter += 1  # Siguiente fila

# Función para seleccionar/deseleccionar las extensiones de una categoría
def toggle_extensions(category):
    for ext in extensions[category]:
        # Si la categoría está seleccionada, seleccionamos las extensiones correspondientes
        checkboxes[ext].set(category_vars[category].get())


# Carpeta de destino
save_to_other_location_var = tk.BooleanVar()
tk.Checkbutton(root, text="Guardar en otra ubicación", variable=save_to_other_location_var, command=toggle_destination).pack(anchor="w", padx=10)

destination_folder_var = tk.StringVar()
destination_entry = tk.Entry(root, textvariable=destination_folder_var, state=tk.DISABLED)
destination_entry.pack(fill="x", padx=10)
destination_button = tk.Button(root, text="Examinar", command=lambda: browse_folder(destination_folder_var), state=tk.DISABLED)
destination_button.pack(anchor="e", padx=10)

# Opción para mover archivos originales
move_option_var = tk.StringVar(value="no_mover")
tk.Label(root, text="Seleccionar opción para mover archivos originales:").pack(anchor="w", padx=10)

tk.Radiobutton(root, text="Dejar originales en su lugar", variable=move_option_var, value="no_mover", command=toggle_move_originals).pack(anchor="w", padx=10)
tk.Radiobutton(root, text="Mover si el PDF es más pequeño", variable=move_option_var, value="mover_si_mas_pequeno", command=toggle_move_originals).pack(anchor="w", padx=10)
tk.Radiobutton(root, text="Mover todos los procesados", variable=move_option_var, value="mover_todos", command=toggle_move_originals).pack(anchor="w", padx=10)

# Carpeta para mover archivos originales
move_originals_folder_var = tk.StringVar()
move_originals_entry = tk.Entry(root, textvariable=move_originals_folder_var)
move_originals_entry.pack(fill="x", padx=10)
move_originals_button = tk.Button(root, text="Examinar", command=lambda: browse_folder(move_originals_folder_var))
move_originals_button.pack(anchor="e", padx=10)

# Mantener fecha del archivo original
maintain_date_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Mantener fecha original del archivo", variable=maintain_date_var).pack(anchor="w", padx=10)

# Botones de conversión y detener
tk.Button(root, text="Convertir", command=start_conversion).pack(pady=10)
tk.Button(root, text="Detener", command=stop_conversion_process).pack(pady=5)


root.mainloop()
