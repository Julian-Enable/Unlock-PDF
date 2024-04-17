import os
import shutil
import time
from PyPDF2 import PdfReader, PdfWriter

def solicitar_datos_usuario():
    print("Bienvenido al removedor de contraseñas de PDF.")
    directorio_fuente = input("Por favor, ingresa el directorio fuente que contiene los PDFs con protección por contraseña: ")
    directorio_destino = input("Por favor, ingresa el directorio destino donde se colocarán los nuevos PDFs sin protección: ")
    password = input("Si los archivos PDF están protegidos con contraseña, por favor ingrésala aquí (de lo contrario, deja este campo en blanco): ")
    return directorio_fuente, directorio_destino, password

def main():
    directorio_fuente, directorio_destino, password = solicitar_datos_usuario()

    fecha_ejec = time.strftime("%Y%m%d%H%M%S", time.localtime())
    nombre_carpeta_respaldo_destino = os.path.join(directorio_destino, fecha_ejec + '_respaldo')
    nombre_carpeta_nueva_destino = os.path.join(directorio_destino, fecha_ejec + '_nuevo')
    os.makedirs(nombre_carpeta_respaldo_destino, exist_ok=True)
    os.makedirs(nombre_carpeta_nueva_destino, exist_ok=True)

    nb_pdf_corregidos, nb_archivos_movidos = 0, 0

    for nombre_archivo in os.listdir(directorio_fuente):
        ruta_archivo_fuente = os.path.join(directorio_fuente, nombre_archivo)
        if not os.path.isfile(ruta_archivo_fuente) or not nombre_archivo.lower().endswith('.pdf'):
            continue

        destino_archivo_backup = os.path.join(nombre_carpeta_respaldo_destino, nombre_archivo)
        destino_archivo_nuevo = os.path.join(nombre_carpeta_nueva_destino, nombre_archivo)

        try:
            with open(ruta_archivo_fuente, 'rb') as f:
                lector_pdf = PdfReader(f)
                
                if lector_pdf.is_encrypted and password:
                    if not lector_pdf.decrypt(password):
                        print(f"No se pudo desencriptar {nombre_archivo} con la contraseña proporcionada.")
                        continue
                
                escritor_pdf = PdfWriter()
                for pagina in lector_pdf.pages:
                    escritor_pdf.add_page(pagina)

                with open(destino_archivo_nuevo, 'wb') as f_out:
                    escritor_pdf.write(f_out)

                nb_pdf_corregidos += 1

            shutil.move(ruta_archivo_fuente, destino_archivo_backup)
            nb_archivos_movidos += 1
        except Exception as e:
            print(f"Error al procesar {nombre_archivo}: {e}")

    print(f"{nb_archivos_movidos} archivo(s) se han movido a {nombre_carpeta_respaldo_destino}.")
    print(f"{nb_pdf_corregidos} archivo(s) PDF se han tratado.")
    input("Presiona enter para finalizar...")

if __name__ == "__main__":
    main()