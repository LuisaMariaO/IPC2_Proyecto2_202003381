from tkinter import *
import os


def ventanaPrincipal():
    #Termina la pantalla de carga
    loading.destroy()
    #Configuración general de la ventana principal
    ventana=Tk()
    ancho=ventana.winfo_screenwidth()
    alto=ventana.winfo_screenheight()
    ventana.geometry("%dx%d" % (ancho, alto))
    ventana.title("Digital Intelligence S.A.")
    ruta_abs=os.path.abspath('.')
    ventana.iconbitmap(ruta_abs+'\\FrontEnd\\Imagenes\\icono.ico')
    
    #Boton de configuración de máquina
    img_config = PhotoImage(file=ruta_abs+'\\FrontEnd\\Imagenes\\settings.png')
    boton_config=Button(text="Cargar configuración",image=img_config, compound=TOP, height=60, width=115)
    boton_config.place(x=(ancho-125),y=0)

    #Carga de archivo
    img_loadfile = PhotoImage(file=ruta_abs+'\\FrontEnd\\Imagenes\\load.png')
    boton_cargar=Button(text="Cargar productos",image=img_loadfile, compound=TOP, height=60, width=90)
    boton_cargar.place(x=0,y=0)
    
    #Exportar reporte
    img_expfile = PhotoImage(file=ruta_abs+'\\FrontEnd\\Imagenes\\export.png')
    boton_exp=Button(text="Exportar reportes",image=img_expfile, compound=TOP, height=60, width=90)
    boton_exp.place(x=99,y=0)

    #Ayuda
    img_help = PhotoImage(file=ruta_abs+'\\FrontEnd\\Imagenes\\help.png')
    boton_help=Button(text="Ayuda",image=img_help, compound=TOP, height=60, width=90)
    boton_help.place(x=198,y=0)

    ventana.mainloop()

  
    


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

