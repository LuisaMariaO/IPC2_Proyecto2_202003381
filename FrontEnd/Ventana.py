from tkinter import *
import os




def ventanaPrincipal():
    ventana=Tk()
    ancho=ventana.winfo_screenwidth()
    alto=ventana.winfo_screenheight()
    ventana.geometry("%dx%d" % (ancho, alto))
    ventana.title("Digital Intelligence S.A.")
    ruta_abs=os.path.abspath('.')
    ventana.iconbitmap(ruta_abs+'\\FrontEnd\\Imagenes\\icono.ico')
    ventana.mainloop()

def ventanaInicio():
    loading=Tk()
    loading.title=("Cargando")
    loading.geometry=("500x500")
    label=Label(loading, text="Hola")
    label.pack(pady=20)

        