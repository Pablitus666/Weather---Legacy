# servicios.py
import requests

API_key = "6d16d24abaebaee9557ff6d2d37e903b"
URL = "https://api.openweathermap.org/data/2.5/weather"

def clima_JSON(ciudad_nombre, callback_ok, callback_error):
    try:
        parametros = {
            "APPID": API_key,
            "q": ciudad_nombre,
            "units": "metric",
            "lang": "es"
        }
        response = requests.get(URL, params=parametros, timeout=5)
        clima = response.json()
        callback_ok(clima)
    except requests.RequestException:
        callback_error("Error de red. Intenta nuevamente.")

def mostrar_respuesta(clima, ciudad_label, temperatura_label, descripcion_label):
    try:
        nombre_ciudad = clima["name"]
        desc = clima["weather"][0]["description"]
        temp = clima["main"]["temp"]

        ciudad_label["text"] = nombre_ciudad
        temperatura_label["text"] = f"{int(temp)}°C"
        descripcion_label["text"] = desc
    except KeyError:
        mostrar_mensaje("No se pudo obtener el clima. Intenta nuevamente.", ciudad_label, temperatura_label, descripcion_label, None)

def mostrar_mensaje(msg, ciudad_label, temperatura_label, descripcion_label, entrada):
    ciudad_label["text"] = msg
    temperatura_label["text"] = ""
    descripcion_label["text"] = ""
    if entrada:
        entrada.delete(0, 'end')
