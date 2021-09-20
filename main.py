from Producto import Producto
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QAction, QMessageBox, QDialog
from Interfaz import MainWindow
import xml.etree.ElementTree as ET
from Maquina import Maquina
import re
from os import system


class Ventana(QMainWindow):
    global maquina
    def __init__(self):
        super().__init__()
        self.ui=MainWindow()
        self.ui.setupUi(self)

        self.maquina=None
        self.limite_linea=None
        self.limte_componente=None
        #Carga configuración de máquina
        self.ui.action_config_maquina.triggered.connect(self.config)
        #Genera reportes de cola de secuencia
        self.ui.action_reporte_cola.triggered.connect(self.reporteCola)

        #Botón de simular
        self.ui.B_play.clicked.connect(self.simular)

        #self.pushButton.clicked.connect(self.hola)
    def config(self):
  
        archivo=QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\','Archivos xml (*.xml)')
        try:
            #Tomo la posición 0 de la ruta, pues QFileDialog retorna una tupla compuesta por la ruta y el tipo de archivo
            tree = ET.parse(archivo[0])
            root = tree.getroot()  
            for Ma in root:
                for l in Ma.iter('CantidadLineasProduccion'):
                    lineas=l.text
                    lineas=int(lineas)
                    
                    #Creación de objeto máquina
                    self.maquina=Maquina(lineas)
                
                #Busco las lineas de producción
                for listado in Ma.iter('ListadoLineasProduccion'):
                    for linea in listado.iter('LineaProduccion'):
                        for numero in linea.iter('Numero'):
                            number=int(numero.text)
                        for componentes in linea.iter('CantidadComponentes'):
                            components=int(componentes.text)
                        for tiempo in linea.iter('TiempoEnsamblaje'):
                            time=int(tiempo.text)
                        self.maquina.lineas.agregar(number,components,time)
                #maquina.lineas.imprimir()
                for productos in Ma.iter('ListadoProductos'):
                    for producto in productos.iter('Producto'):
                        for nombre in producto.iter('nombre'):
                            name=nombre.text
                            name=name.replace('\t','')
                            name=name.replace('\n','')
                        self.maquina.productos.agregar(name)
                        for elaboracion in producto.iter('elaboracion'):
                            item=self.maquina.productos.getProducto(name)
                            patronElaboracion=re.compile('L[0-9]+p?C[0-9]+')
                            patron=patronElaboracion.findall(elaboracion.text)
                            patronLinea=re.compile('L[0-9]+') #Encuentra la linea
                            patronComponente=re.compile('C[0-9]+') #Encuentra el componente
                            
                            for el in patron:
                                #Toma la linea
                                line=patronLinea.search(el)
                                line=line.group()
                                #Toma el componente
                                component=patronComponente.search(el)
                                component=component.group()
                                #Agrega a la cola de elaboracion
                                item.elaboracion.encolar(line,component)
            QMessageBox.about(self, "Notificación", "¡Configuración cargada con éxito!")
                            
             
        except:
            QMessageBox.about(self, "Advertencia", "No es posible abrir el archivo")

        #Agregando items al comboBox
        aux = self.maquina.productos.primero
        while aux:
            self.ui.comboBox.addItem(aux.nombre)
            aux = aux.siguiente


    def reporteCola(self):

        actual=self.ui.comboBox.currentText() #Producto actual en el ComboBox

        if actual!="Seleccionar":#Valor por default
            producto=self.maquina.productos.getProducto(actual)
            graphviz="""
            digraph L{
            node[shape=box3d fillcolor=cadetblue3 style =filled]
        
            subgraph cluster_p{\n"""
            graphviz+='\t\tlabel="Cola de secuencia: '+producto.nombre+'"\n'
            graphviz+="""\t\tbgcolor = azure
            edge[dir = "normal"]\n"""
            #Códgo realizado en la cola
            graphviz+=producto.elaboracion.graficar()
            nombre=producto.nombre.replace(" ", "")
            graphviz+="}\n}"
            graph= open('Reportes\\Dot\\'+nombre+'.dot','w')
            graph.write(graphviz)
            graph.close()
            
            system('dot -Tpng Reportes\\Dot\\'+nombre+'.dot -o Reportes\\Cola_'+nombre+'.png')
            system('Reportes\\Cola_'+nombre+'.png')


    def simular(self):
        actual=self.ui.comboBox.currentText()
        if actual!="Seleccionar":
            producto=self.maquina.productos.getProducto(actual) #Producto actual
            cola=producto.elaboracion
            
            elemento=cola.primero
            #Encuentra los componentes a los que espera llegar cada línea antes de ensamblar por primera vez
            self.asignarSiguientes(elemento)
    

            #Vuelvo a recorrer la cola desde el inicio para comenzar los movimientos
            elemento=cola.primero
            proximo=cola.primero
            proximo_linea=proximo.linea
            proximo_linea=int(proximo_linea.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
            proximo_componente=proximo.componente
            proximo_componente=int(proximo_componente.replace("C",""))

            print(proximo_linea)
            print(proximo_componente)

            columnas=0
            ultimo=cola.ultimo

            


            
            while proximo is not None: 
                numero=elemento.linea
                numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                componente=elemento.componente
                componente=int(componente.replace("C",""))
                linea=self.maquina.lineas.getLinea(numero)
      
                if linea.disponible:
                    self.maquina.lineas.setOcupada(numero)   
                    if linea.componente_actual<linea.componente_siguiente:
                        self.maquina.lineas.moverAdelante(numero, linea.componente_actual)
                    elif linea.componente_actual>linea.componente_siguiente:
                        self.maquina.lineas.moverAtras(numero, linea.componente_actual)
                    elif linea.componente_actual==linea.componente_siguiente :
                        if linea.componente_actual==proximo_componente and linea.numero==proximo_linea:
                        
                            self.maquina.lineas.ensamblar(numero, linea.componente_actual)
                            producto.elaboracion.finalizado(numero, linea.componente_actual)
                            self.maquina.lineas.setDisponible(numero)
                            proximo=proximo.siguiente
                            proximo_linea=proximo.linea
                            proximo_linea=int(proximo_linea.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                            proximo_componente=proximo.componente
                            proximo_componente=int(proximo_componente.replace("C",""))
                            print(proximo_linea)
                            print(proximo_componente)
                            elemento=cola.primero
                            self.maquina.lineas.setComponenteSiguiente(proximo_linea,proximo_componente)
                            
                            continue
                
                elemento=elemento.siguiente
                if elemento is None:
                    self.maquina.lineas.liberarLineas()
                    elemento=cola.primero
                
            

    def asignarSiguientes(self, elemento):
        while elemento is not None:
                numero=elemento.linea
                numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                componente=elemento.componente
                componente=int(componente.replace("C",""))
                linea=self.maquina.lineas.getLinea(numero)
                if linea.componente_siguiente==None:
                    self.maquina.lineas.setComponenteSiguiente(numero,componente) #Asigno el componente en todo el sistema
                    linea.componente_siguiente=componente #Asigno el componente de manera local
                    self.limite_linea=numero
                    self.limite_componente=linea.componente_siguiente

                    
                    #'''El componente siguiente es la base para comenzar a mover las líneas'''
                   # return linea.componente_siguiente
                    
                #print(linea.tiempo)
                elemento=elemento.siguiente

    def asignarSiguiente(self, numero, componente):
        linea=self.maquina.lineas.getLinea(numero)
        self.maquina.lineas.setComponenteSiguiente(numero,componente) #Asigno el componente en todo el sistema
        linea.componente_siguiente=componente #Asigno el componente de manera local
        self.limite_linea=numero
        self.limite_componente=linea.componente_siguiente

    
    def asignarLimite(self, cola):
        elemento=cola.primero

        while elemento is not None:
            numero=elemento.linea
            numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
            componente=elemento.componente
            componente=int(componente.replace("C",""))
            linea=self.maquina.lineas.getLinea(numero)
            if linea.componente_siguiente!=None:
                self.limte_linea=numero
                self.limite_componente=linea.componente_siguiente
            elemento=elemento.siguiente
       


    def retornarSiguientes(self,elemento):
          while elemento is not None:
                numero=elemento.linea
                numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                componente=elemento.componente
                componente=int(componente.replace("C",""))
                linea=self.maquina.lineas.getLinea(numero)
                if linea.componente_siguiente==None:
                    self.maquina.lineas.setComponenteSiguiente(numero,componente) #Asigno el componente en todo el sistema
                    linea.componente_siguiente=componente #Asigno el componente de manera local
                    #'''El componente siguiente es la base para comenzar a mover las líneas'''
                    return linea.componente_siguiente
                    
                #print(linea.tiempo)
                elemento=elemento.siguiente


if __name__=='__main__':
    app=QApplication(sys.argv)
    GUI=Ventana()
    GUI.show()
    sys.exit(app.exec_())