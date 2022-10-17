import datetime
from tkinter import Button, Entry, Label, Listbox, Tk, Toplevel, mainloop

from conecction_db import insert_cliente, list_customer, list_series
from main import Principal
from pruebas import Example
from docu import test_system


def register_user():
    nombre = cuadro_nombre.get()
    edad = cuadro_edad.get()
    direccion = cuadro_direccion.get()
    fecha = str(datetime.datetime.now())
    insert_cliente(nombre, edad, direccion, fecha)
    list_customer()
    ventana_nueva.destroy()


def windows_user():
    global ventana_nueva
    ventana_nueva = Toplevel()
    ventana_nueva.title("Registrar usuario")
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

def sentadillas(usuario):
    Example()
    emi = Principal(usuario)
    a = emi.magic()
    ventana_nueva.destroy()


def biceps(usuario):
    emi = Principal(usuario)
    a = emi.mancurnas()
    ventana_nueva.destroy()


def select_user():
    select = listbox.curselection()[0]
    usuario = list_customer()[select]
    print(usuario)
    
    ventana_eleccion_ejercicio = Toplevel()
    ventana_eleccion_ejercicio.title("Selección de ejercicios")
    ventana_eleccion_ejercicio.geometry("400x300")
    label = Label(
        ventana_eleccion_ejercicio,
        text="Seleccione la opcion deseada!",
        padx=50,
        pady=25,
    )
    label.pack()
    boton1 = Button(
        ventana_eleccion_ejercicio,
        text="    Registrar   biceps   ",
        bg="green",
        padx=50,
        pady=25,
        command=biceps,
    )
    boton1.pack()
    boton2 = Button(
        ventana_eleccion_ejercicio,
        text="Registrar  sentadillas",
        bg="green",
        padx=50,
        pady=25,
        command=sentadillas(usuario),
    )
    boton2.pack()
    # a = emi.mancurnas()
    ventana_eleccion_ejercicio.destroy()


def destroy_2():
    ventana_list_customer.destroy()


def select_user_2():
    select = listbox.curselection()[0]
    usuario = list_customer()[select]
    print(usuario)
    lista = list_series(usuario)
    global ventana_list_customer
    ventana_list_customer = Toplevel()
    ventana_list_customer.title("Rutinas")
    ventana_list_customer.geometry("400x300")
    global listbox_rutinas
    listbox_rutinas = Listbox(ventana_list_customer)
    n = 0
    for customer in lista:
        listbox_rutinas.insert(n, customer)
        n = +1
    listbox_rutinas.pack()
    boton = Button(
        ventana_list_customer,
        text="Salir",
        bg="green",
        padx=50,
        pady=25,
        command=destroy_2,
    )
    boton.pack()


def windows_list_user():
    global ventana_nueva
    ventana_nueva = Toplevel()
    ventana_nueva.title("Usuarios")
    ventana_nueva.geometry("400x300")
    global listbox
    listbox = Listbox(ventana_nueva)
    customers = list_customer()
    n = 0
    for customer in customers:
        listbox.insert(n, customer)
        n = +1
    listbox.pack()
    boton = Button(
        ventana_nueva,
        text="Seleccion",
        bg="green",
        padx=50,
        pady=25,
        command=select_user,
    )
    boton.pack()


def windows_list_user_2():
    global ventana_nueva
    ventana_nueva = Toplevel()
    ventana_nueva.title("Usuarios")
    ventana_nueva.geometry("400x300")
    global listbox
    listbox = Listbox(ventana_nueva)
    customers = list_customer()
    n = 0
    for customer in customers:
        listbox.insert(n, customer)
        n = +1
    listbox.pack()
    boton = Button(
        ventana_nueva,
        text="Seleccion",
        bg="green",
        padx=50,
        pady=25,
        command=select_user_2,
    )
    boton.pack()

def destroy():
    root.destroy()

def test():
    test_system()


root = Tk()
root.title("Contador de Ejercicios")
root.geometry("600x550")
label = Label(
    root,
    text="Seleccione la opcion deseada!",
    padx=50,
    pady=25,
)
label.pack()
boton1 = Button(
    root,
    text="Registrar  nuevo  usuario",
    bg="green",
    padx=50,
    pady=25,
    command=windows_user,
)
boton1.pack()
boton2 = Button(
    root,
    text="Registrar Actividad fisica",
    bg="green",
    padx=50,
    pady=25,
    command=windows_list_user,
)
boton2.pack()
boton3 = Button(
    root,
    text="Listar repeticione Rutinas",
    bg="green",
    padx=50,
    pady=25,
    command=windows_list_user_2,
)
boton3.pack()
boton4 = Button(
    root,
    text=" Testeo    De     Sistema  ",
    bg="green",
    padx=50,
    pady=25,
    command=test,
)
boton4.pack()
boton5 = Button(
    root,
    text=" Salir      del      programa ",
    bg="red",
    padx=50,
    pady=25,
    command=destroy,
)
boton5.pack()


mainloop()
