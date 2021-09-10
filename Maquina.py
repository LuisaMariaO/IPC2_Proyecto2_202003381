from ListaLineas import ListaLineas
from ListaComponentes import ListaComponentes
class Maquina:
    def __init__(self, n, m):
        #n=lineas de ensamblaje
        self.n=n
        #m=componentes
        self.m=m
        #Posicion actual del brazo robotico, posicion inicial nula
        self.linea=None
        self.componente=None
        self.lineas = ListaLineas()
        self.componentes=ListaComponentes()
   
      