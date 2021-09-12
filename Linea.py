from ListaComponentes import ListaComponentes
class Linea():
    def __init__(self,numero,tiempo,no_componentes):
        self.numero=numero
        self.tiempo=tiempo
        self.no_componentes=no_componentes
        self.componentes=ListaComponentes()
        #Componente de la línea en el que se encuentra el brazo
        self.componente_actual=None
        self.siguiente = None
        self.anterior = None
       