import sqlite3
import datetime
import os

# Ruta de la base de datos original
ruta_origen = r"C:\Users\megam\Downloads\recordatorios.db"

# Carpeta destino del backup
carpeta_destino = r"C:\Users\megam\OneDrive\Pictures"

# Verificar que la base de datos existe
if not os.path.exists(ruta_origen):
    print("❌ Error: No se encontró la base de datos en la ruta indicada.")
else:
    try:
        # Crear nombre del archivo de respaldo con fecha y hora
        fecha = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        ruta_backup = os.path.join(carpeta_destino, f"backup_recordatorio_{fecha}.db")

        # Crear conexiones
        conexion_origen = sqlite3.connect(ruta_origen)
        conexion_backup = sqlite3.connect(ruta_backup)

        # Realizar el backup
        with conexion_backup:
            conexion_origen.backup(conexion_backup)

        # Cerrar conexiones
        conexion_backup.close()
        conexion_origen.close()

        print(f"✅ Backup creado exitosamente en:\n{ruta_backup}")

    except Exception as e:
        print(f"❌ Error al crear el backup: {e}")
