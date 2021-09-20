from re import T
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

    def liberarLineas(self):
        aux = self.primero
        while aux:
            aux.disponible=True
            aux = aux.siguiente

    def getLinea(self,numero):
     
        aux = self.primero
        while aux:
            if numero==aux.numero:
      
                return aux
            aux = aux.siguiente
        return None

    def setComponenteSiguiente(self, numero, componente):
        aux = self.primero
        while aux:
            if numero==aux.numero and componente<=aux.no_componentes:
                aux.componente_siguiente=componente
                #print("Siguiente: ",aux.numero," ", aux.componente_siguiente)
                return aux
            aux = aux.siguiente
        return None
    def setComponenteActual(self, numero, componente):
        aux = self.primero
        while aux:
            if numero==aux.numero and componente<=aux.no_componentes:
                aux.componente_actual=componente
                return aux
            aux = aux.siguiente
        return None
    def setOcupada(self, numero):
        aux=self.primero
        while aux:
            if numero==aux.numero:
                aux.disponible=False
                return aux
            aux = aux.siguiente
        return None
    def setDisponible(self, numero):
        aux=self.primero
        while aux:
            if numero==aux.numero:
                aux.disponible=True
                return aux
            aux = aux.siguiente
        return None

    def setEnsamblando(self, numero):
        aux=self.primero
        while aux:
            if numero==aux.numero:
                aux.ensamblando=True
                return aux
            aux = aux.siguiente
        return None
        

    def moverAdelante(self, numero, componente):
        aux = self.primero
        while aux:
            if numero==aux.numero and componente<=aux.no_componentes:
                aux.componente_actual=componente+1
                print("Linea ",numero," Mover brazo - Componente ",componente+1)
                

                return "Linea ",numero," Mover brazo - Componente ",componente+1
            aux = aux.siguiente
        return None

    def moverAtras(self,numero, componente):
        aux = self.primero
        while aux:
            if numero==aux.numero and componente<=aux.no_componentes:
                aux.componente_actual=componente-1
                print("Linea ",numero," Mover brazo - Componente ",componente-1)
            

                return "Linea ",numero," Mover brazo - Componente ",componente-1
            aux = aux.siguiente
        return None
        

    def ensamblar(self,numero,componente):
        
        aux = self.primero
        while aux:
            if numero==aux.numero and componente<=aux.no_componentes:
                aux.componente_siguiente=None
                print("Linea ", numero, " Ensamblar - Componente",componente)
            

                return "Linea ", numero, " Ensamblar - Componente",componente
            aux = aux.siguiente
        return None



