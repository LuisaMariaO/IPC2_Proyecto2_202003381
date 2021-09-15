from Linea import Linea
class ListaLineas:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    def vacia(self):
         return self.primero == None 
    
    def agregar(self, numero, no_componentes, tiempo):
        if self.vacia():
            self.primero = self.ultimo = Linea(numero, no_componentes, tiempo)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Linea(numero, no_componentes, tiempo)
            self.ultimo.anterior = aux
            
            
        self.size+=1
        
    
    def imprimir(self):
        aux = self.primero
        while aux:
            print("numero= "+str(aux.numero)+" Componentes= "+str(aux.no_componentes)+" Tiempo= "+str(aux.tiempo))
            aux = aux.siguiente
