import datetime
from tkinter import Button, Entry, Label, Tk, Toplevel, mainloop

from conecction_db import insert_cliente, list_customer


def register_user():
    nombre = cuadro_nombre.get()
    edad = cuadro_edad.get()
    direccion = cuadro_direccion.get()
    fecha = str(datetime.datetime.now())
    insert_cliente(nombre, edad, direccion, fecha)
    list_customer()


def windows_user():
    ventana_nueva = Toplevel()
    ventana_nueva.title("ventana secundaria")
    ventana_nueva.geometry("400x300")
    bienvenido = Label(ventana_nueva, text="BIENVENIDO")
    bienvenido.grid(row=0, column=0)
    bienvenido.config(font=("Arial", 16))
    # nombre  fecha, direccion
    nombre_label = Label(ventana_nueva, text="Cual es tu nombre:")
    nombre_label.grid(row=1, column=0)
    nombre_label.config(padx=10, pady=10)
    global cuadro_nombre
    cuadro_nombre = Entry(ventana_nueva)
    cuadro_nombre.grid(row=1, column=1)
    # edad
    edad_label = Label(ventana_nueva, text="Cual es tu edad:")
    edad_label.grid(row=2, column=0)
    edad_label.config(padx=10, pady=10)
    global cuadro_edad
    cuadro_edad = Entry(ventana_nueva)
    cuadro_edad.grid(row=2, column=1)
    # direccion
    direccion_label = Label(ventana_nueva, text="Cual es tu direccion:")
    direccion_label.grid(row=3, column=0)
    direccion_label.config(padx=10, pady=10)
    global cuadro_direccion
    cuadro_direccion = Entry(ventana_nueva)
    cuadro_direccion.grid(row=3, column=1)

    # Boton para grabar
    boton_grabar = Button(
        ventana_nueva,
        text="Registrar usuario",
        padx=50,
        pady=25,
        command=register_user,
    )
    boton_grabar.grid(row=4, column=1)


root = Tk()
root.title("Contador de Ejercicios")
root.geometry("500x500")
label = Label(
    root,
    text="Seleccione la opcion deseada!",
    padx=50,
    pady=25,
)
label.pack()
boton1 = Button(
    root,
    text="Registrar nuevo usuario",
    bg="green",
    padx=50,
    pady=25,
    command=windows_user,
)
boton1.pack()
# var = StringVar()
# var.set("¡Hola, mundo!")

# entry = ttk.Entry()
# entry.place(x=50, y=50)


mainloop()
