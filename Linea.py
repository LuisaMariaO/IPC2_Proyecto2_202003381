from ListaComponentes import ListaComponentes
class Linea():
    def __init__(self,numero,no_componentes,tiempo):
        self.numero=numero
        self.no_componentes=no_componentes
        self.tiempo=tiempo
       
        self.componentes=ListaComponentes()
        #Componente de la línea en el que se encuentra el brazo

        self.componente_actual=0
        self.componente_siguiente=None
        self.disponible=True
        self.siguiente = None
        self.anterior = None
       