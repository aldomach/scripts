import os
import re

# Configurá el directorio donde se encuentran tus archivos markdown
directorio = r'c:\Users\aldo_\Mi unidad\DriveSyncFiles\Aldo_Seewald\aldo_informatica'

# Expresión regular para encontrar fechas en formato DD/MM/AAAA
patron = re.compile(r'(\d{2})\/(\d{1})\/(\d{4})')

# Reemplazo para cambiar fechas a [[AAAA-MM-DD]]
reemplazo = r'[[\3-\2-\1]]'

# Función para recorrer directorios y subdirectorios
def corregir_fechas_en_directorio(directorio):
    for root, _, files in os.walk(directorio):
        for archivo in files:
            if archivo.endswith('.md'):
                ruta_archivo = os.path.join(root, archivo)
                
                try:
                    # Lee el contenido del archivo
                    with open(ruta_archivo, 'r', encoding='utf-8') as file:
                        contenido = file.read()

                    # Reemplaza las fechas en el contenido
                    nuevo_contenido = re.sub(patron, reemplazo, contenido)

                    # Escribe el nuevo contenido de vuelta al archivo
                    with open(ruta_archivo, 'w', encoding='utf-8') as file:
                        file.write(nuevo_contenido)

                    print(f'Fechas corregidas en: {ruta_archivo}')
                
                except PermissionError:
                    print(f'Permiso denegado: {ruta_archivo}')
                except Exception as e:
                    print(f'Error al procesar {ruta_archivo}: {e}')

# Ejecutar la función
corregir_fechas_en_directorio(directorio)

