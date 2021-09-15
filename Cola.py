from Elaboracion import Elaboracion
class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    def encolar(self,linea,componente): 
        
        nuevo = Elaboracion(linea, componente) 
        self.size += 1
        if self.primero is None:
            self.primero = nuevo
        else:
            aux = self.primero
            while aux.siguiente is not None:
                aux = aux.siguiente
            aux.siguiente = nuevo

    def desencolar(self):
        pass

    def imprimirCola(self):
        aux = self.primero
        if self.size>0:
            while aux is not None:
                print(str(aux.linea)+str(aux.componente)+'->',end="")
                aux = aux.siguiente
        else:
            print("")
        print("")