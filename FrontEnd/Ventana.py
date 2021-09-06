import tkinter
import os
class Ventana():

    def __init__(self):
        self.ventana=tkinter.Tk()
        ancho=self.ventana.winfo_screenwidth()
        alto=self.ventana.winfo_screenheight()
        self.ventana.geometry("%dx%d" % (ancho, alto))
        self.ventana.title("Digital Intelligence S.A.")
        ruta_abs=os.path.abspath('.')
        self.ventana.iconbitmap(ruta_abs+'\\FrontEnd\\Imagenes\\icono.ico')
        self.ventana.mainloop()