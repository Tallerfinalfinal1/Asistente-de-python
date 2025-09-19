import pyttsx3
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import asyncio
import python_weather
import geocoder
import aiohttp
from bs4 import BeautifulSoup
import requests
import datetime
from babel.dates import format_date
from langcodes import Language
import mysql.connector
import time
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from pathlib import Path
import win32com.client as win32
import tkinter as tk
import http.server
import socketserver
import threading
import pyperclip
from gtts import gTTS
import subprocess
import unicodedata
import webbrowser
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import pygame
import os
import subprocess
import mysql.connector
import mysql.connector
from mysql.connector import Error
import random
import spacy
from transformers import pipeline
from gpt4all import GPT4All

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 120)




def hablar(audio):
    engine.say(audio)
    engine.runAndWait()


def obtener_consulta():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Reconociendo...")
        consulta = recognizer.recognize_google(audio, language="es")
        print("Dijiste:", consulta)
        return consulta.lower()
    except Exception as e:
        hablar("No se entendió, podrías repetirlo?")
        return ""



def obtener_hora():
    hora_actual = datetime.datetime.now().strftime("%I:%M:%S %p")
    hablar("La hora actual es " + hora_actual)


def obtener_fecha():
    fecha_actual = datetime.datetime.now()
    fecha_formateada = format_date(fecha_actual, format="full", locale="es_ES")
    hablar("La fecha de hoy es " + fecha_formateada)


def saludar():
    hora = datetime.datetime.now().hour
    if 6 <= hora < 12:
        hablar("¡Buenos días!")
    elif 12 <= hora < 18:
        hablar("¡Buenas tardes!")
    else:
        hablar("¡Buenas noches!")
    hablar("¿En qué puedo ayudarte hoy?")


def buscar_wikipedia(consulta):
    hablar("Buscando en Wikipedia...")
    wikipedia.set_lang("es")
    try:
        resumen = wikipedia.summary(consulta, sentences=2)
        hablar(resumen)
    except wikipedia.exceptions.PageError:
        hablar("Lo siento, no encontré información en Wikipedia para esa consulta.")
    except wikipedia.exceptions.DisambiguationError as e:
        hablar("La consulta es ambigua. ¿Podrías ser más específico?")


def normalizar_correo(correo):
    # Función para normalizar el correo electrónico según las especificaciones
    correo = correo.lower()  # Convertir todo a minúsculas
    correo = correo.replace(" ", "")
    correo = correo.replace(" arroba ", "")  # Eliminar " arroba "
    correo = correo.replace(" punto ", ".")  # Reemplazar " punto " por "."
    correo = correo.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")  # Eliminar tildes
    
    # Añadir "@" si no se ha añadido correctamente
    if "@" not in correo:
        correo += "@gmail.com"  # Cambia "example.com" por el dominio que prefieras

    return correo


def enviar_correo(destinatario, asunto, descripcion, adjuntos=None):
    # Abrir una nueva ventana del navegador y cargar la página del correo
    webbrowser.open("https://mail.google.com/mail/u/0/?pli=1#inbox")

    # Esperar a que se cargue la página
    time.sleep(10)  # Ajusta el tiempo según la velocidad de carga de tu conexión

    # Mover el mouse al nuevo correo y esperar un momento
    pyautogui.click(x=70, y=217)  
    time.sleep(1)  # Pausa más larga para asegurar que el campo está listo

    # Mover el mouse al campo de destinatario y esperar un momento
    pyautogui.click(x=855, y=295)  
    time.sleep(1)  # Pausa más larga para asegurar que el campo está listo

    # Escribir el destinatario, incluyendo el "@" como una combinación de teclas
    destinatario_normalizado = normalizar_correo(destinatario)
    for char in destinatario_normalizado:
        if char == "@":
            pyautogui.hotkey('ctrl', 'alt', 'q')  # Presionar Ctrl + Alt + q
        else:
            pyautogui.write(char)

    # Mover el mouse al campo de asunto y esperar un momento
    pyautogui.click(x=857, y=342)  
    time.sleep(1)  # Pausa más larga para asegurar que el campo está listo
    pyautogui.write(asunto)

    # Mover el mouse al campo de descripción y esperar un momento
    pyautogui.click(x=839, y=379)  
    time.sleep(1)  # Pausa más larga para asegurar que el campo está listo
    pyautogui.write(descripcion)

    # Esperar un momento para que el usuario adjunte archivos (si es necesario)
    if adjuntos:
        time.sleep(60)  # Esperar un minuto

    # Mover el mouse al botón de enviar y hacer click
    pyautogui.moveTo(x=830, y=685, duration=0.5)
    pyautogui.click()


def abrir_sitio_web(url):
    wb.open_new_tab(url)


def buscar_google(consulta):
    base_url = "https://www.google.com/search?q="
    query = "+".join(consulta.split())
    url = base_url + query
    abrir_sitio_web(url)  # Solo abrir el sitio sin decir el link


def buscar_cancion(cancion):
    url = "https://www.youtube.com/results?search_query=" + "+".join(cancion.split())
    abrir_sitio_web(url)


def cerrar_sesion():
    os.system("shutdown - 1")


def reiniciar():
    os.system("shutdown /r /t 1")


def apagar():
    os.system("shutdown /s /t 1")


directorio_guardado = r"C:\Users\megam\Pictures\Screenshots"


if not os.path.exists(directorio_guardado):
    os.makedirs(directorio_guardado)


def tomar_captura_pantalla(numero_capturas=1):
    for i in range(numero_capturas):
        try:
            captura = pyautogui.screenshot()
            archivo_captura = os.path.join(directorio_guardado, f"captura_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{i + 1}.png")
            captura.save(archivo_captura)
        except Exception as e:
            print("Error al guardar la captura de pantalla:", e)
            hablar("Hubo un error al guardar la captura de pantalla.")
        else:
            hablar(f"¡Captura de pantalla {i + 1} realizada !")


def estado_sistema():
    uso_de_cpu = str(psutil.cpu_percent())
    frequencia_de_cpu = str(psutil.cpu_freq())
    uso_disco = psutil.disk_usage("/")
    hablar("El uso de CPU es de " + uso_de_cpu + " %")
    hablar("La frecuencia del procesador es de " + str(frequencia_de_cpu) + " MHz")
    hablar("El uso del disco es de " + str(uso_disco.percent) + " %")

def obtener_clima(ciudad):
    url = f"https://www.google.com/search?q=clima+{ciudad}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        clima = soup.find("div", class_="BNeawe").text
        hablar(f"El clima en {ciudad} es {clima}")
    else:
        hablar("Lo siento, no pude encontrar el clima para esa ciudad.")


def obtener_ruta_guardado(ubicacion):
    directorio_base = os.path.expanduser("~")  # Directorio base del usuario
    ubicacion = ubicacion.lower()  # Convertir a minúsculas para una comparación sin distinción entre mayúsculas y minúsculas

    if ubicacion == "escritorio":
        return os.path.join(directorio_base, "Desktop")
    elif ubicacion == "documentos":
        return os.path.join(directorio_base, "Documents")
    elif ubicacion == "descargas":
        return os.path.join(directorio_base, "Downloads")
    else:
        # Si la ubicación no coincide con las opciones predefinidas, asumimos que es una ruta completa
        return ubicacion


def crear_archivo(tipo_archivo, ubicacion=None, nombre_archivo=None):
    if ubicacion:
        ruta_guardado = obtener_ruta_guardado(ubicacion)
        if not os.path.exists(ruta_guardado):
            hablar("La ubicación especificada no existe.")
            return
        os.chdir(ruta_guardado)

    if nombre_archivo:
        nombre_archivo = nombre_archivo.strip()  # Eliminar espacios en blanco adicionales
        if tipo_archivo == "Word":
            nombre_archivo += ".docx"
            try:
                word = win32.Dispatch("Word.Application")
                word.Visible = True
                doc = word.Documents.Add()
                doc.SaveAs(os.path.abspath(nombre_archivo))
                doc.Close()
                hablar(f"¡Archivo '{nombre_archivo}' creado exitosamente!")
            except Exception as e:
                hablar(f"Error al crear el archivo: {e}")
        elif tipo_archivo == "Excel":
            nombre_archivo += ".xlsx"
            os.system(f"start excel /e \"{nombre_archivo}\"")
        elif tipo_archivo == "PowerPoint":
            nombre_archivo += ".pptx"
            os.system(f"start powerpnt /s \"{nombre_archivo}\"")
        elif tipo_archivo == "Bloc de notas":
            nombre_archivo += ".txt"
            try:
                with open(nombre_archivo, "w") as archivo:
                    pass  # Crear archivo vacío
                hablar(f"¡Archivo '{nombre_archivo}' creado exitosamente!")
            except Exception as e:
                hablar(f"Error al crear el archivo: {e}")
        else:
            hablar("Lo siento, no reconozco ese tipo de archivo.")
    else:
        if tipo_archivo == "Word":
            os.system("start winword")
        elif tipo_archivo == "Excel":
            os.system("start excel")
        elif tipo_archivo == "PowerPoint":
            os.system("start powerpnt")
        elif tipo_archivo == "Bloc de notas":
            os.system("start notepad")
        else:
            hablar("Lo siento, no reconozco ese tipo de archivo.")


def crear_carpeta(nombre_carpeta, ubicacion=None):
    if ubicacion:
        ruta_guardado = obtener_ruta_guardado(ubicacion)
    else:
        hablar("Por favor, dime la ubicación donde deseas crear la carpeta:")
        ubicacion = obtener_consulta()
        ruta_guardado = obtener_ruta_guardado(ubicacion)
    
    if not os.path.exists(ruta_guardado):
        hablar("La ubicación especificada no existe.")
        return
    
    os.chdir(ruta_guardado)

    nombre_carpeta = nombre_carpeta.strip()  # Eliminar espacios en blanco adicionales
    try:
        os.makedirs(nombre_carpeta)
        hablar(f"¡Carpeta '{nombre_carpeta}' creada exitosamente!")
    except Exception as e:
        hablar(f"Error al crear la carpeta: {e}")




def obtener_codigo_idioma(nombre_idioma):
    """
    Convierte el nombre del idioma hablado por el usuario a su código estándar.
    """
    idiomas = {
        'español': 'es',
        'inglés': 'en',
        'francés': 'fr',
        'alemán': 'de',
        'italiano': 'it',
        'portugués': 'pt',
        'ruso': 'ru',
        'chino': 'zh-CN',
        'japonés': 'ja',
        'coreano': 'ko',
        'árabe': 'ar',
        'holandés': 'nl',
        'sueco': 'sv',
    }
    return idiomas.get(nombre_idioma.lower(), 'en')  # Por defecto, regresa 'en' si no se encuentra el idioma


def hablar_texto_no_latino(texto, idioma_destino):
    try:
        tts = gTTS(text=texto, lang=idioma_destino)
        archivo_mp3 = "traduccion.mp3"
        tts.save(archivo_mp3)
        os.system(f"start {archivo_mp3}")  # En Windows, puedes usar 'start'
    except Exception as e:
        hablar(f"Lo siento, no pude reproducir el texto en {idioma_destino} debido a: {str(e)}")

def traducir_texto(texto, idioma_origen='auto'):
    try:
        hablar("Por favor, dime a qué idioma quieres traducir el texto.")
        idioma_destino_hablado = obtener_consulta()
        idioma_destino = obtener_codigo_idioma(idioma_destino_hablado)  # Convierte el idioma hablado a su código
        traductor = GoogleTranslator(source=idioma_origen, target=idioma_destino)
        traduccion = traductor.translate(texto)

        if idioma_destino in ['ru', 'zh-CN', 'ja', 'ko', 'ar']:  # Idiomas con alfabetos no latinos
            hablar("Voy a usar Google Text-to-Speech para pronunciar la traducción.")
            hablar_texto_no_latino(traduccion, idioma_destino)  # Usa gTTS
            print(f"Traducción al {idioma_destino_hablado.capitalize()}: {traduccion}")
        else:
            hablar(f"El texto traducido es: {traduccion}")  # Usa pyttsx3 para idiomas latinos
            print(f"Traducción al {idioma_destino_hablado.capitalize()}: {traduccion}")
        return traduccion
        
    except Exception as e:
        hablar(f"No pude realizar la traducción debido a: {str(e)}")
        return None





def convertir_texto_a_numero(texto):
    numeros_textuales = {
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
        "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
        "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20,
        "veintiuno": 21, "veintidós": 22, "veintitrés": 23, "veinticuatro": 24, "veinticinco": 25,
        "veintiséis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29, "treinta": 30,
        "treinta y uno": 31, "treinta y dos": 32, "treinta y tres": 33, "treinta y cuatro": 34, "treinta y cinco": 35,
        "treinta y seis": 36, "treinta y siete": 37, "treinta y ocho": 38, "treinta y nueve": 39, "cuarenta": 40,
        "cuarenta y uno": 41, "cuarenta y dos": 42, "cuarenta y tres": 43, "cuarenta y cuatro": 44, "cuarenta y cinco": 45,
        "cuarenta y seis": 46, "cuarenta y siete": 47, "cuarenta y ocho": 48, "cuarenta y nueve": 49, "cincuenta": 50,
        "cincuenta y uno": 51, "cincuenta y dos": 52, "cincuenta y tres": 53, "cincuenta y cuatro": 54, "cincuenta y cinco": 55,
        "cincuenta y seis": 56, "cincuenta y siete": 57, "cincuenta y ocho": 58, "cincuenta y nueve": 59, "sesenta": 60,
        "sesenta y uno": 61, "sesenta y dos": 62, "sesenta y tres": 63, "sesenta y cuatro": 64, "sesenta y cinco": 65,
        "sesenta y seis": 66, "sesenta y siete": 67, "sesenta y ocho": 68, "sesenta y nueve": 69, "setenta": 70,
        "setenta y uno": 71, "setenta y dos": 72, "setenta y tres": 73, "setenta y cuatro": 74, "setenta y cinco": 75,
        "setenta y seis": 76, "setenta y siete": 77, "setenta y ocho": 78, "setenta y nueve": 79, "ochenta": 80,
        "ochenta y uno": 81, "ochenta y dos": 82, "ochenta y tres": 83, "ochenta y cuatro": 84, "ochenta y cinco": 85,
        "ochenta y seis": 86, "ochenta y siete": 87, "ochenta y ocho": 88, "ochenta y nueve": 89, "noventa": 90,
        "noventa y uno": 91, "noventa y dos": 92, "noventa y tres": 93, "noventa y cuatro": 94, "noventa y cinco": 95,
        "noventa y seis": 96, "noventa y siete": 97, "noventa y ocho": 98, "noventa y nueve": 99, "cien": 100,
        "ciento uno": 101, "ciento dos": 102, "ciento tres": 103, "ciento cuatro": 104, "ciento cinco": 105,
        "ciento seis": 106, "ciento siete": 107, "ciento ocho": 108, "ciento nueve": 109, "ciento diez": 110,
        "ciento once": 111, "ciento doce": 112, "ciento trece": 113, "ciento catorce": 114, "ciento quince": 115,
        "ciento dieciséis": 116, "ciento diecisiete": 117, "ciento dieciocho": 118, "ciento diecinueve": 119, "ciento veinte": 120,
        "ciento veintiuno": 121, "ciento veintidós": 122, "ciento veintitrés": 123, "ciento veinticuatro": 124, "ciento veinticinco": 125,
        "ciento veintiséis": 126, "ciento veintisiete": 127, "ciento veintiocho": 128, "ciento veintinueve": 129, "ciento treinta": 130,
        "ciento treinta y uno": 131, "ciento treinta y dos": 132, "ciento treinta y tres": 133, "ciento treinta y cuatro": 134, "ciento treinta y cinco": 135,
        "ciento treinta y seis": 136, "ciento treinta y siete": 137, "ciento treinta y ocho": 138, "ciento treinta y nueve": 139, "ciento cuarenta": 140,
        "ciento cuarenta y uno": 141, "ciento cuarenta y dos": 142, "ciento cuarenta y tres": 143, "ciento cuarenta y cuatro": 144, "ciento cuarenta y cinco": 145,
        "ciento cuarenta y seis": 146, "ciento cuarenta y siete": 147, "ciento cuarenta y ocho": 148, "ciento cuarenta y nueve": 149, "ciento cincuenta": 150,
        # Puedes continuar hasta el número que necesites
    }

    texto = texto.lower().strip()  # Convertir el texto a minúsculas y eliminar espacios en blanco

    # Comprobar si el texto contiene el prefijo "código" y extraer el número
    if texto.startswith("código "):
        partes = texto.split(" ", 1)  # Dividir solo en la primera aparición
        if len(partes) == 2:
            texto = partes[1].strip()  # Tomar la parte después de "código"

    # Intentar convertir el texto a un número textual o devolver el texto original
    return str(numeros_textuales.get(texto, texto))



# Función para conectar a la base de datos

def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            host="localhost",  # Cambia este valor a "localhost" si estás ejecutando en local.
            user="localhost",
            passwd="",
            database="recordatorio"
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
conexion = conectar_base_datos()

# Función para crear un nuevo recordatorio en la base de datos
def crear_recordatorio(recordatorio, conexion):
    try:
        cursor = conexion.cursor()

        # Obtener el último código utilizado
        cursor.execute("SELECT MAX(Codigo) FROM `recuerdos`")
        ultimo_codigo = cursor.fetchone()[0]

        # Si no hay recordatorios en la base de datos, establecer el código en 1
        if ultimo_codigo is None:
            nuevo_codigo = 1
        else:
            nuevo_codigo = ultimo_codigo + 1

        # Insertar el nuevo recordatorio con el código calculado
        cursor.execute("INSERT INTO `recuerdos` (Codigo, Nombre) VALUES (%s, %s)", (nuevo_codigo, recordatorio))
        conexion.commit()
        cursor.close()

        hablar(f"Recordatorio creado con el código: {nuevo_codigo}")
    except Error as e:
        print(f"Error al crear el recordatorio: {e}")

# Función para recuperar un recordatorio de la base de datos utilizando su código
def recordar_recordatorio(conexion):
    try:
        hablar("Por favor, di el código del recordatorio.")
        codigo_texto = obtener_consulta()
        
        # Convertir el texto a un número si es un número textual o sigue el formato "Código N"
        codigo = convertir_texto_a_numero(codigo_texto)
        
        try:
            codigo = int(codigo)
        except ValueError:
            hablar("Por favor, di un número válido como código.")
            return
        
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre FROM `recuerdos` WHERE Codigo = %s", (codigo,))
        resultado = cursor.fetchone()
        if resultado:
            hablar(f"Recordatorio: {resultado[0]}")
        else:
            hablar("No se encontró ningún recordatorio con ese código.")
        cursor.close()
    except Error as e:
        print(f"Error al recordar el recordatorio: {e}")

# Función para borrar un recordatorio de la base de datos utilizando su código
def borrar_recordatorio(conexion):
    try:
        hablar("Por favor, di el código del recordatorio que deseas eliminar.")
        codigo_texto = obtener_consulta()
        
        # Convertir el texto a un número si es un número textual o sigue el formato "Código N"
        codigo = convertir_texto_a_numero(codigo_texto)
        
        try:
            codigo = int(codigo)
        except ValueError:
            hablar("Por favor, di un número válido como código.")
            return
        
        cursor = conexion.cursor()

        # Eliminar el recordatorio con el código dado
        cursor.execute("DELETE FROM `recuerdos` WHERE Codigo = %s", (codigo,))
        num_filas_afectadas = cursor.rowcount
        conexion.commit()
        cursor.close()

        if num_filas_afectadas > 0:
            hablar(f"Recordatorio con código {codigo} ha sido eliminado")
        else:
            hablar("No se encontró ningún recordatorio con ese código o ya ha sido eliminado anteriormente")
    except Error as e:
        print(f"Error al borrar el recordatorio: {e}")

# Función para modificar un recordatorio de la base de datos utilizando su código
def modificar_recordatorio(conexion):
    try:
        hablar("Por favor, di el código del recordatorio que deseas modificar.")
        codigo_texto = obtener_consulta()
        
        # Convertir el texto a un número si es un número textual o sigue el formato "Código N"
        codigo = convertir_texto_a_numero(codigo_texto)
        
        try:
            codigo = int(codigo)
        except ValueError:
            hablar("Por favor, di un número válido como código.")
            return
        
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre FROM `recuerdos` WHERE Codigo = %s", (codigo,))
        resultado = cursor.fetchone()
        if resultado:
            hablar(f"El recordatorio actual es: {resultado[0]}. ¿Cuál es el nuevo contenido del recordatorio?")
            nuevo_contenido = obtener_consulta()
            cursor.execute("UPDATE `recuerdos` SET Nombre = %s WHERE Codigo = %s", (nuevo_contenido, codigo))
            conexion.commit()
            hablar("¡El recordatorio ha sido modificado exitosamente!")
        else:
            hablar("No se encontró ningún recordatorio con ese código.")
        cursor.close()
    except Error as e:
        print(f"Error al modificar el recordatorio: {e}")



def obtener_localizacion():
    ubicacion = geocoder.ip("me")
    hablar(f"Te encuentras en {ubicacion.city}, {ubicacion.state}, {ubicacion.country}")


def abrir_carpeta(ruta_carpeta):
    os.startfile(ruta_carpeta)



def normalizar_texto(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    return texto_normalizado.lower()



def buscar_carpeta(nombre_carpeta):
    nombre_carpeta_normalizado = normalizar_texto(nombre_carpeta)
    
    # Inicialmente, suponemos que no se ha encontrado la carpeta
    carpeta_encontrada = False
    
    # Buscar recursivamente la carpeta en todo el sistema
    for directorio_raiz, directorios, archivos in os.walk("/"):  # Comienza la búsqueda desde la raíz del sistema
        for directorio in directorios:
            if normalizar_texto(directorio) == nombre_carpeta_normalizado:
                carpeta_encontrada = True
                ruta_carpeta = os.path.join(directorio_raiz, directorio)
                hablar(f"Carpeta '{nombre_carpeta}' encontrada en: {ruta_carpeta}")
                abrir_carpeta(ruta_carpeta)  # Asegúrate de que esta línea esté llamando a la función correcta
                return  # Termina la búsqueda después de encontrar la primera ocurrencia de la carpeta
    
    if not carpeta_encontrada:
        hablar(f"No se encontró la carpeta '{nombre_carpeta}'.")
        

def gracias():
    hablar("Gracias de qué? Yo no he hecho nada, estoy mal programado.")


async def obtener_noticias():
    fuentes = [
        "https://www.bbc.co.uk/mundo",
        "https://cnnespanol.cnn.com/",
        "https://elpais.com",
        "https://www.infobae.com/america/",
        "https://www.france24.com/es/"
    ]
    
    async with aiohttp.ClientSession() as session:
        for fuente in fuentes:
            async with session.get(fuente) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    noticias = soup.find_all("h3")
                    
                    if noticias:
                        hablar(f"Aquí tienes las últimas noticias de {fuente}:")
                        for i, noticia in enumerate(noticias[:3]):  # Limito a 3 por fuente para no abrumar
                            texto_noticia = noticia.get_text().strip()
                            if texto_noticia:
                                hablar(f"Noticia {i + 1}: {texto_noticia}")
                            else:
                                hablar(f"No se pudo obtener el texto de la noticia {i + 1}.")
                    else:
                        hablar(f"No se encontraron noticias en {fuente}.")
                else:
                    hablar(f"No pude obtener noticias de {fuente}. Código de estado: {response.status}")





def enviar_mensaje_whatsapp(contacto, mensaje):
    # Abrir WhatsApp Web
    webbrowser.open("https://web.whatsapp.com/")

    # Esperar a que se cargue WhatsApp Web
    time.sleep(10)

    # Coordenadas del icono de búsqueda de nuevo chat
    x_buscar_chat, y_buscar_chat = 156, 204
    pyautogui.click(x_buscar_chat, y_buscar_chat)

    # Esperar a que aparezca el campo de búsqueda
    time.sleep(2)

    # Escribir el nombre del contacto
    pyautogui.write(contacto)
    pyautogui.press("enter")

    # Esperar a que se abra el chat
    time.sleep(2)

    # Coordenadas para escribir el mensaje
    x_mensaje, y_mensaje = 675, 687
    pyautogui.click(x_mensaje, y_mensaje)

    # Escribir y enviar el mensaje
    pyautogui.write(mensaje)
    pyautogui.press("enter")

# Ejemplo de uso
# enviar_mensaje_whatsapp("Nombre del contacto", "¡Hola, este es un mensaje de prueba!")


def buscar_imagen(imagen):
    consulta = f"https://www.google.com/search?tbm=isch&q={imagen}"
    webbrowser.open(consulta)



def obtener_porcentaje_bateria():
    bateria = psutil.sensors_battery()
    porcentaje = bateria.percent
    hablar(f"La batería está al {porcentaje}%")
    
    
# 2. Árboles y grafos para relacionar características de animales
class NodoAnimal:
    def __init__(self, nombre, categoria, descripcion):
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

# Árbol de animales con los nuevos sonidos
def crear_arbol_animales():
    raiz = NodoAnimal("Animales", "Reino Animal", "Seres vivos que pueden moverse y responden a estímulos.")

    # Categorías principales
    mamiferos = NodoAnimal("Mamíferos", "Vertebrados", "Tienen pelo y producen leche para alimentar a sus crías.")
    aves = NodoAnimal("Aves", "Vertebrados", "Tienen plumas y generalmente pueden volar.")
    
    # Animales específicos
    perro = NodoAnimal("Perro", "Mamífero", "El perro es un amigo fiel y juguetón. Hay muchas razas de perros, cada una con su propia personalidad. Algunos perros son pequeños y se pueden llevar en un bolso, mientras que otros son muy grandes y pueden proteger tu hogar. Les encanta jugar a buscar pelotas y pasear. ¡Los perros son muy buenos para aprender trucos y pueden ser entrenados para ayudar a las personas!")
    gato = NodoAnimal("Gato", "Mamífero", "El gato es un animal doméstico muy ágil y curioso. Son expertos en saltar y escalar. Les gusta dormir mucho, ¡a veces hasta 16 horas al día! Tienen un gran sentido del oído y pueden escuchar sonidos que nosotros no podemos. Los gatos son conocidos por ser limpios y usan una caja de arena para hacer sus necesidades. También pueden ser muy cariñosos y les encanta jugar con ovillos de lana.")
    leon = NodoAnimal("León", "Mamífero", "El león es conocido como el 'rey de la selva', aunque vive en la sabana. Los leones son muy fuertes y sociales; viven en grupos llamados manadas. Un león macho tiene una melena impresionante que lo hace ver más grande y feroz. ¡Los leones también son muy buenos cazadores y pueden correr rápido para atrapar a su presa! Aunque son grandes y poderosos, les encanta descansar bajo la sombra de los árboles.")
    vaca = NodoAnimal("Vaca", "Mamífero", "La vaca es un animal de granja que produce leche, la cual se usa para hacer queso, yogur y helado. Tienen un carácter tranquilo y pasan mucho tiempo pastando en los campos. Las vacas son muy sociables y les gusta estar en grupos. También son conocidas por su gran barriga y por hacer 'muuu'. ¡Sabías que las vacas pueden reconocer a otros animales y a las personas?")
    oveja = NodoAnimal("Oveja", "Mamífero", "La oveja es famosa por su suave lana, que se usa para hacer ropa como suéteres y bufandas. Son animales de rebaño y les gusta estar juntas. Las ovejas tienen un sentido del olfato muy agudo y pueden identificar a otras ovejas. ¡Además, pueden reconocer caras humanas! Son muy curiosas y a menudo se acercan para investigar cosas nuevas.")
    cerdo = NodoAnimal("Cerdo", "Mamífero", "El cerdo es conocido por su hocico y su forma regordeta. Son animales muy inteligentes y pueden aprender a hacer trucos, como sentarse o dar la pata. Les gusta revolcarse en el barro para refrescarse y protegerse del sol. ¡Los cerdos son muy sociales y disfrutan de la compañía de otros cerdos! Pueden ser tan limpios que prefieren hacer sus necesidades lejos de su área de descanso.")
    pajaro = NodoAnimal("Pájaro", "Ave", "Los pájaros son animales que pueden volar y tienen plumas. Hay muchas especies de pájaros, y cada una tiene su propio canto. Algunos pájaros, como el loro, pueden imitar sonidos y palabras. Les gusta construir nidos en árboles o en edificios. ¡Los pájaros son muy curiosos y pueden ser muy juguetones! Pueden comer semillas, frutas e incluso insectos.")
    aguila = NodoAnimal("Águila", "Ave", "El águila es un ave rapaz que tiene una vista increíble. Puede ver objetos desde muy lejos y es muy rápida al volar. Las águilas construyen grandes nidos en lo alto de los árboles. Son cazadoras expertas y atrapan a sus presas con garras muy afiladas. ¡Las águilas son símbolos de libertad y poder en muchas culturas!")
    buho = NodoAnimal("Búho", "Ave", "El búho es un ave nocturna, lo que significa que está activa por la noche. Tienen ojos grandes que les ayudan a ver en la oscuridad. Suelen cazar ratones y otros pequeños animales. ¡Los búhos pueden girar su cabeza hasta 270 grados para ver a su alrededor! También son conocidos por su característico 'uuuh' y son considerados sabios en muchas culturas.")


    # Agregar animales al árbol
    mamiferos.agregar_hijo(perro)
    mamiferos.agregar_hijo(gato)
    mamiferos.agregar_hijo(leon)
    mamiferos.agregar_hijo(vaca)
    mamiferos.agregar_hijo(oveja)
    mamiferos.agregar_hijo(cerdo)
    aves.agregar_hijo(pajaro)
    aves.agregar_hijo(aguila)
    aves.agregar_hijo(buho)
    
    # Agregar categorías al árbol principal
    raiz.agregar_hijo(mamiferos)
    raiz.agregar_hijo(aves)
    
    return raiz

# Función para buscar características en el árbol
def buscar_animal(arbol, animal_buscado):
    if arbol.nombre.lower() == animal_buscado.lower():
        return arbol
    for hijo in arbol.hijos:
        resultado = buscar_animal(hijo, animal_buscado)
        if resultado:
            return resultado
    return None

# 3. Sonidos de animales con enlaces y reproducción
animal_sonidos = {
    "perro": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-dog.mp3",
    "gato": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-cat.mp3",
    "león": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-lion.mp3",
    "vaca": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-cow.mp3",
    "oveja": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-sheep.mp3",
    "cerdo": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-pig.mp3",
    "pájaro": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-bird1.mp3",
    "águila": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-eagle.mp3",
    "búho": r"C:\Users\megam\Downloads\SonidosAnimales\sfx-animal-owl.mp3"
}



def reproducir_sonido_animal(animal):
    arbol_animales = crear_arbol_animales()
    animal_encontrado = buscar_animal(arbol_animales, animal)

    if animal_encontrado:
        if animal in animal_sonidos:
            sonido_url = animal_sonidos[animal]
            hablar(f"El {animal_encontrado.nombre} es un {animal_encontrado.categoria}. {animal_encontrado.descripcion}")
            
            try:
                # Iniciar pygame y cargar el sonido
                pygame.mixer.init()
                pygame.mixer.music.load(sonido_url)
                pygame.mixer.music.play()

                # Esperar hasta que el sonido termine de reproducirse
                while pygame.mixer.music.get_busy():
                    continue
            except Exception as e:
                print(f"Hubo un error al reproducir el sonido del {animal}: {str(e)}")
        else:
            hablar(f"No tengo el sonido del {animal} en este momento.")
    else:
        hablar(f"No tengo información sobre el {animal}.")
        


# Definición de datos
datos = {
    "cultural": [
        "La lengua más hablada en el mundo es el mandarín.",
        "El carnaval más grande del mundo se celebra en Río de Janeiro.",
        "La Biblioteca de Alejandría fue una de las mayores del mundo antiguo.",
    ],
    "animal": [
        "Los elefantes pueden comunicarse a través de vibraciones en el suelo.",
        "Las mariposas Monarca migran más de 4,000 kilómetros cada año.",
        "El tiburón ballena es el pez más grande del mundo.",
        "Los pingüinos emperador pueden bucear hasta 550 metros.",
        "Los perros tienen un sentido del olfato entre 10,000 y 100,000 veces mejor que el de los humanos.",
        "Las abejas pueden recordar rostros humanos.",
    ],
    "ecologico": [
        "El Amazonas produce el 20% del oxígeno de la Tierra.",
        "Un árbol puede absorber hasta 22 kg de dióxido de carbono por año.",
        "El océano cubre más del 70% de la superficie terrestre.",
        "Las selvas tropicales cubren menos del 6% de la superficie terrestre, pero contienen más del 50% de las especies.",
        "El 90% de los residuos plásticos acaban en el océano.",
        "Cada minuto, el Amazonas pierde el equivalente a 1.5 canchas de fútbol en árboles.",
    ],
    "geografico": [
        "El Everest es la montaña más alta del mundo con 8,848 metros.",
        "El desierto de Atacama es el más árido del planeta.",
        "Australia es el continente habitado más seco.",
        "El Nilo es el río más largo del mundo con 6,650 kilómetros.",
        "Groenlandia es la isla más grande del mundo.",
        "El lago Baikal en Rusia contiene el 20% del agua dulce no congelada del mundo.",
    ],
}

def truco_magia():
    hablar("Okey, di un número del 1 al 500.")
    numero_usuario = input("Dime un número del 1 al 500: ")  # Puedes cambiar esto por reconocimiento de voz si lo estás usando
    
    # Simulación del "cálculo complejo"
    hablar("Recalculando...")
    time.sleep(2)  # Espera 1 segundo
    hablar("Derivando...")
    time.sleep(2)
    hablar("Analizando...")
    time.sleep(2)
    hablar("Resolviendo la Conjetura de Goldbach...")
    time.sleep(3)
    
    # El "truco de magia"
    hablar(f"¡Tu número es... {numero_usuario}!")

# Función para obtener un dato aleatorio de todos los datos
def obtener_dato_aleatorio():
    # Obtener todos los datos en una lista
    todos_los_datos = []
    for categoria in datos.values():
        todos_los_datos.extend(categoria)
    
    # Seleccionar un dato aleatorio
    return random.choice(todos_los_datos)


ruta_modelo = "Llama-3.2-3B-Instruct-Q4_0.gguf"  # Nombre del modelo
ruta_completa = "C:\\Users\\megam\\Downloads\\descargasss"  # Ruta donde está el archivo

def responder_pregunta(pregunta_usuario):
    try:
        with GPT4All(ruta_modelo, model_path=ruta_completa, device="cpu") as modelo:
            respuesta = modelo.generate(pregunta_usuario, max_tokens=100)
        return respuesta
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"


        
def principal():
    saludar()
    while True:
        consulta = obtener_consulta()
        print(consulta)
        if "qué hora es" in consulta:
            obtener_hora()
        elif "responde" in consulta:
            responder_pregunta(consulta)
        elif "qué fecha es" in consulta:
            obtener_fecha()
        elif "wikipedia" in consulta:
            buscar_wikipedia(consulta.split("wikipedia")[-1].strip())
        elif "enviar correo" in consulta:
            hablar("¿A quién quieres enviar el correo electrónico?")
            destinatario = obtener_consulta()
            hablar("¿Cuál es el asunto del correo electrónico?")
            asunto = obtener_consulta()
            hablar("¿Cuál es el contenido del correo electrónico?")
            descripcion = obtener_consulta()
            enviar_correo(destinatario, asunto, descripcion)
        elif "cómo te he tratado" in consulta:
            hablar("¡Ayuda por favor! Este señor me hijueputea")
        elif "gracias" in consulta:
            gracias()
        elif "abrir sitio web" in consulta:
            abrir_sitio_web(consulta.split("abrir sitio web")[-1].strip())
        elif "traducir" in consulta:
            hablar("¿Qué texto te gustaría traducir?")
            texto_a_traducir = obtener_consulta()  # Pide el texto al usuario
            traducir_texto(texto_a_traducir)
        elif "buscar" in consulta:
            query = consulta.split("buscar en internet")[-1].strip()
            buscar_google(query)
        elif "buscar en internet" in consulta:
            query = consulta.split("buscar en internet")[-1].strip()
            buscar_google(query)
        elif "pon en youtube" in consulta:
            query = consulta.split("pon en youtube")[-1].strip()
            buscar_cancion(query)
        elif "poner" in consulta:
            query = consulta.split("poner")[-1].strip()
            buscar_cancion(query)
        elif "cerrar sesión" in consulta:
            cerrar_sesion()
        elif "reiniciar" in consulta:
            reiniciar()
        elif "apagar" in consulta:
            apagar()
        elif "crear carpeta" in consulta:
            hablar("Por favor, dime la ubicación donde deseas crear la carpeta:")
            ubicacion = obtener_consulta()
            hablar("Ahora, dime el nombre de la carpeta que deseas crear:")
            nombre_carpeta = obtener_consulta()
            crear_carpeta(nombre_carpeta, ubicacion)
        elif "crear archivo" in consulta:
            hablar("¿Qué tipo de archivo te gustaría crear? Puedes elegir entre Word, Excel y Bloc de notas.")
            tipo_archivo = obtener_consulta().capitalize()
            hablar("¿En qué ubicación te gustaría guardar el archivo? Puedes decir 'escritorio', 'documentos', 'descargas', 'imágenes', 'música' o 'vídeos'.")
            ubicacion = obtener_consulta()
            hablar("Por favor, dime el nombre del archivo (sin extensión).")
            nombre_archivo = obtener_consulta()
            crear_archivo(tipo_archivo, ubicacion, nombre_archivo)
        elif "abre la carpeta de" in consulta:
            nombre_carpeta = consulta.split("abre la carpeta de")[-1].strip()
            buscar_carpeta(nombre_carpeta)
        elif "toma una captura de pantalla" in consulta:
            tomar_captura_pantalla()
        elif "cuál es el estado de sistema" in consulta or "cuál es el estado del sistema" in consulta:
            estado_sistema()
        elif "cuéntame un chiste" in consulta:
            hablar(pyjokes.get_joke(language="es"))
        elif "cuál es el clima" in consulta:
            ciudad = consulta.split("clima")[-1].strip()
            obtener_clima(ciudad)
        elif "dame mi ubicación" in consulta:
            obtener_localizacion()
        elif "dime unas noticias" in consulta:
            asyncio.run(obtener_noticias())
        elif "mensaje de whatsapp" in consulta:
            hablar("¿A quién quieres enviar el mensaje?")
            contacto = obtener_consulta()
            hablar("¿Cuál es el mensaje?")
            mensaje = obtener_consulta()
            enviar_mensaje_whatsapp(contacto, mensaje)
        elif "buscar imagen" in consulta:
            buscar_imagen(consulta.replace("buscar imagen", "").strip())
        elif "cuál es el porcentaje de batería" in consulta:
            obtener_porcentaje_bateria()
        elif "sonido de" in consulta:
            animal = consulta.replace("sonido de", "").strip()
            reproducir_sonido_animal(animal)
        elif "recordatorio" in consulta:
            crear_recordatorio(consulta.split("recordatorio")[-1].strip(), conexion)
        elif "borrar" in consulta:
            borrar_recordatorio(conexion)
        elif "recordar" in consulta:
            recordar_recordatorio(conexion)
        elif "modificar" in consulta:
            modificar_recordatorio(conexion)
        elif "dato" in consulta.lower():
         dato = obtener_dato_aleatorio()
         hablar(dato)  # Asumiendo que tienes una función hablar para output
        elif "dame un truco de magia" in consulta: 
         truco_magia()
        elif "adiós" in consulta:
            hablar("¡Adiós!")
            break



if __name__ == "__main__":
  hablar("¡Hola! Soy tu asistente de python,")
principal()