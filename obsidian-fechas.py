import os
import re
import argparse

# Configurá el directorio usando argparse para aceptar argumentos de línea de comandos
def obtener_argumentos():
    parser = argparse.ArgumentParser(description='Reemplazar fechas en archivos .md en un directorio.')
    parser.add_argument('directorio', type=str, help='Ruta del directorio con archivos .md')
    return parser.parse_args()

# Expresión regular para encontrar fechas en formato DD/MM/AAAA
patron = re.compile(r'(\d{2})\/(\d{2})\/(\d{4})')

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

# Ejecutar la función principal
if __name__ == '__main__':
    args = obtener_argumentos()
    corregir_fechas_en_directorio(args.directorio)

