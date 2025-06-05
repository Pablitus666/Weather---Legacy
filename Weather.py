import os
import sys
import threading
import tkinter as tk
from tkinter import PhotoImage, Toplevel, Label
from customtkinter import CTk, CTkEntry, CTkButton
import requests
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena el _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ruta del logo
logo_ico_path = resource_path("images/logo.ico")
logo_png_path = resource_path("images/logo.png")
robot_png_path = resource_path("images/robot.png")
boton_png_path = resource_path("images/boton.png")

# API key y URL
API_key = "6d16d24abaebaee9557ff6d2d37e903b"
URL = "https://api.openweathermap.org/data/2.5/weather"

# Función para mostrar la respuesta
def mostrar_respuesta(clima):
    try:
        nombre_ciudad = clima["name"]
        desc = clima["weather"][0]["description"]
        temp = clima["main"]["temp"]

        ciudad["text"] = nombre_ciudad
        temperatura["text"] = str(int(temp)) + "°C"
        descripcion["text"] = desc

        # Ajustar el tamaño de la ventana
        ventana.update_idletasks()
        new_height = ventana.winfo_reqheight()
        ventana.geometry(f"370x{new_height}")
        centrar_ventana(ventana)
    except KeyError:  # Especificamos el tipo de excepción
        ciudad["text"] = "Intenta Nuevamente"

# Función para obtener el clima
def clima_JSON(ciudad_nombre):
    try:
        parametros = {"APPID": API_key, "q": ciudad_nombre, "units": "metric", "lang": "es"}
        response = requests.get(URL, params=parametros)
        clima = response.json()
        ventana.after(0, mostrar_respuesta, clima)  # Llamar mostrar_respuesta en el hilo principal
    except requests.RequestException as e:
        print(f"Error: {e}")

def obtener_clima_en_segundo_plano(ciudad_nombre):
    hilo = threading.Thread(target=clima_JSON, args=(ciudad_nombre,))
    hilo.start()

# Función para manejar el evento de presionar Enter
def enter_key_pressed(event):
    obtener_clima_en_segundo_plano(texto_ciudad.get())

# Función para manejar el evento de presionar Delete
def delete_key_pressed(event):
    texto_ciudad.delete(0, 'end')

# Función para centrar la ventana
def centrar_ventana(ventana, ancho=None, alto=None):
    ventana.update_idletasks()
    if ancho is None or alto is None:
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Variable global para controlar la ventana de información
info_window_open = False

# Función personalizada para mostrar un cuadro de mensaje con fuente grande y saltos de línea
def mostrar_informacion():
    global info_window_open
    if info_window_open:
        return

    info_window_open = True

    info_window = Toplevel(ventana)
    info_window.withdraw()
    info_window.title("Información")
    info_window.config(bg='#023047')
    info_window.resizable(0, 0)
    info_window.iconbitmap(logo_ico_path)

    ancho = 375
    alto = 225

    centrar_ventana(info_window, ancho, alto)
    info_window.deiconify()

    frame_info = tk.Frame(info_window, bg='#023047')
    frame_info.pack(pady=10, padx=10)

    img = PhotoImage(file=robot_png_path)
    img_label = tk.Label(frame_info, image=img, bg='#023047')
    img_label.image = img
    img_label.grid(row=0, column=0, padx=10, pady=5, rowspan=3)

    message = tk.Label(frame_info, text="Desarrollado por: \nPablo Téllez A.\n \nTarija - 2024.", justify="center",
                       bg='#023047', fg='white', font=("Comic Sans MS", 14, "bold"), anchor="center")
    message.grid(row=0, column=1, padx=8, pady=10, sticky="n")

    # Redimensionar la imagen del botón
    original_boton_image = Image.open(boton_png_path)
    resized_boton_image = original_boton_image.resize((100, 40), Image.LANCZOS)
    boton_image = ImageTk.PhotoImage(resized_boton_image)

    # Estilo para el botón de cerrar
    close_button = tk.Button(frame_info, text="Cerrar", image=boton_image, compound="center", command=lambda: cerrar_info_window(info_window), bg='#023047', fg='#ffffff', font=("Comic Sans MS", 12, "bold"), bd=0, highlightthickness=0, activebackground='#023047', activeforeground='#fcbf49')
    close_button.image = boton_image
    close_button.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="n")

    # Configurar comportamiento visual de botón al pasar el ratón
    close_button.bind("<Enter>", lambda e: close_button.config(fg="#fcbf49"))
    close_button.bind("<Leave>", lambda e: close_button.config(fg="#ffffff"))

def cerrar_info_window(window):
    global info_window_open
    window.destroy()
    info_window_open = False

# Configuración de la ventana principal
ventana = CTk()
ventana.geometry("370x610")
# Configurar el color de fondo de la ventana
ventana.config(bg='#023047')
# Establecer el título de la ventana
ventana.title("Weather Report")
# Cargar la imagen del icono (.ico)
ventana.iconbitmap(logo_ico_path)
# Esto remueve el botón maximizar
ventana.resizable(0,0)
# Cargar la imagen del logo
logo_image = PhotoImage(file=logo_png_path)

# Mostrar la imagen del logo en un Label
logo_label = tk.Label(ventana, image=logo_image, bg='#023047')
logo_label.pack(padx=30, pady=20)
# Vincular la imagen con el evento de clic
logo_label.bind("<Button-1>", lambda e: mostrar_informacion())

texto_ciudad = CTkEntry(ventana, font=("Arial", 20, "bold"), justify="center",
                        placeholder_text='Nombre de la ciudad', border_color='#219ebc', fg_color='#023047', width=300, height=40)
texto_ciudad.pack(padx=30, pady=10)

obtener_clima = CTkButton(ventana, text="Weather Report", font=("Arial", 20, "bold"), command=lambda: obtener_clima_en_segundo_plano(texto_ciudad.get()), text_color='#ffffff', fg_color='#219ebc')
obtener_clima.pack(pady=15)  # Reducido pady para subir la posición

# Vincular la tecla Enter con la función
ventana.bind('<Return>', enter_key_pressed)

# Vincular la tecla Delete con la función
ventana.bind('<Delete>', delete_key_pressed)

ciudad = tk.Label(ventana, bg='#023047', fg='white', font=("Arial", 20, "bold"), wraplength=350)
ciudad.pack(padx=20, pady=20)

temperatura = tk.Label(ventana, bg='#023047', fg='white', font=("Arial", 60, "bold"))
temperatura.pack(padx=10, pady=10)

descripcion = tk.Label(ventana, bg='#023047', fg='white', font=("Arial", 20, "bold"))
descripcion.pack(padx=10, pady=10)

# Centrar la ventana al inicializar
ventana.update_idletasks()  # Necesario para que winfo_width() y winfo_height() devuelvan valores correctos
centrar_ventana(ventana)

ventana.mainloop()
