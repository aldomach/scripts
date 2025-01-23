import os
import platform
from datetime import datetime

# Genera un archivo .bat para comprimir archivos PDF utilizando PDF24. 
# El script mantiene la estructura de directorios original en el destino, 
# asegurando que no se sobrescriban archivos existentes. 
# Las rutas de origen, destino, el software PDF24 y la calidad de compresión 
# son configurables al inicio del script.


# Variables al inicio
origen = "c:\Temp\comprimir\DISPONIBLES"
destino = "c:\Temp\comprim"
software = "C:/Program Files/PDF24/pdf24-DocTool.exe"
calidad = "default/medium"

def ajustar_ruta(ruta):
    # Normaliza la ruta y cambia las barras según el sistema operativo
    ruta = os.path.normpath(ruta)
    if platform.system() == "Windows":
        return ruta.replace('\\', '/')
    return ruta

def generar_nombre_unico(ruta):
    """Genera un nombre único para evitar sobrescribir archivos existentes"""
    base, extension = os.path.splitext(ruta)
    contador = 1
    while os.path.exists(ruta):
        ruta = f"{base}_{contador}{extension}"
        contador += 1
    return ruta

def generar_script():
    # Generar el nombre del archivo con la fecha y hora actual
    archivo_bat = datetime.now().strftime('script_%Y%m%d_%H%M%S.bat')

    with open(archivo_bat, 'w') as f:
        for root, dirs, files in os.walk(origen):
            for file in files:
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

# Llamada para generar el script
generar_script()
