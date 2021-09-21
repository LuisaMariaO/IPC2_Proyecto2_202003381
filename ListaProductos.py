from os import name
from Producto import Producto
class ListaProductos:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

    def vacia(self):
         return self.primero == None 
    
    def agregar(self, nombre):
        if self.vacia():
            self.primero = self.ultimo = Producto(nombre)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Producto(nombre)
            self.ultimo.anterior = aux
            
            
        self.size+=1
        
    
    def imprimir(self):
        aux = self.primero
        while aux:
            print("Producto= "+aux.nombre)
            aux = aux.siguiente

    def getProducto(self,nombre):
        
        aux = self.primero
        while aux:
            if aux.nombre==nombre:
                
                return aux
            aux=aux.siguiente
        return None

    def setSimulado(self,nombre):
        
        aux = self.primero
        while aux:
            if aux.nombre==nombre:
                
                aux.simulado=True
            aux=aux.siguiente
        return None