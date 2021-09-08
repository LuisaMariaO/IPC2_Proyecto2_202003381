from tkinter import *
import os


def ventanaPrincipal():
    global x,y
    loading.destroy()
    ventana=Tk()
    ancho=ventana.winfo_screenwidth()
    
    alto=ventana.winfo_screenheight()
    x=ancho/2
    y=alto/2
    ventana.geometry("%dx%d" % (ancho, alto))
    ventana.title("Digital Intelligence S.A.")
    ruta_abs=os.path.abspath('.')
    ventana.iconbitmap(ruta_abs+'\\FrontEnd\\Imagenes\\icono.ico')
    


loading=Tk()
loading.title("Cargando")
x=0
y=0
x=(loading.winfo_screenwidth())//2-250
    
y=(loading.winfo_screenheight())//2-250

loading.geometry("500x500"+"+"+str(x)+"+"+str(y))
loading.overrideredirect(1)

img = PhotoImage(file = 'Logo.png')
label_img = Label(loading, image = img)
label_img.pack()


loading.resizable(0,0)
loading.after(3000, ventanaPrincipal)
mainloop()

