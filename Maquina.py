from ListaLineas import ListaLineas
from ListaProductos import ListaProductos
from ListaComponentes import ListaComponentes
from ListaProductosArchivo import ListaProductosArchivo
class Maquina:
    def __init__(self, n):
        #n=lineas de ensamblaje
        self.n=n
        self.lineas = ListaLineas()
        self.productos=ListaProductos()
        self.simulacionMasiva=ListaProductosArchivo()
        


   
      