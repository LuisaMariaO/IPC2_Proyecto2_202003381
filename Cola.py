from Elaboracion import Elaboracion
class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
   
    def vacia(self):
         return self.primero == None 
    
    def encolar(self, linea, componente):
        if self.vacia():
            self.primero = self.ultimo = Elaboracion(linea,componente)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Elaboracion(linea,componente)
            self.ultimo.anterior = aux
            
            
        self.size+=1

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

    def finalizado(self,linea, componente):
        aux = self.primero
        if self.size>0:
            while aux is not None:
                if linea==aux.linea and componente==aux.componente:
                    aux.ensamblado=True
                    return aux
         
                aux = aux.siguiente
        return None


    def graficar(self):
        graphviz=''
        #Crep los nodos
        aux = self.primero
        if self.size>0:
            while aux is not None:
                graphviz+='\t\t'+str(aux.linea)+str(aux.componente)+'[label="'+str(aux.linea)+str(aux.componente)+'", fillcollor=azure]\n'
                aux = aux.siguiente
        #Conecto los nodos
        aux = self.primero
        graphviz+='\t\t{rank=same; '+str(aux.linea)+str(aux.componente)
        aux=aux.siguiente
        if self.size>0:
            while aux is not None:
                graphviz+='->'+str(aux.linea)+str(aux.componente)
                aux = aux.siguiente
        graphviz+='}\n'

        return graphviz
        