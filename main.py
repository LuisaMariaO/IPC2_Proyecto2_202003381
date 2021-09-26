from Producto import Producto
import sys
from os import system
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QAction, QMessageBox, QDialog, QTableWidget, QTableWidgetItem

from Interfaz import MainWindow
import xml.etree.ElementTree as ET
from Maquina import Maquina
import re
from os import name, system


class Ventana(QMainWindow):
    global maquina
    def __init__(self):
        super().__init__()
        self.ui=MainWindow()
        self.ui.setupUi(self)

        self.maquina=None
        self.archivoActual=""
        self.limite_linea=None
        self.limte_componente=None
        self.bandera=True
        #Carga configuración de máquina
        self.ui.action_config_maquina.triggered.connect(self.config)
        self.ui.action_simulacion.triggered.connect(self.leerSimulacion)
        #Genera reportes de cola de secuencia
        self.ui.action_reporte_cola.triggered.connect(self.reporteCola)

        self.ui.action_acerca_de.triggered.connect(self.info)
        self.ui.action_my_info.triggered.connect(self.about)

        self.ui.comboBox.activated[str].connect(self.agregarComponentes)

        #Botón de simular
        self.ui.B_play.clicked.connect(self.simular)

        self.ui.B_siguiente.clicked.connect(self.simularMasivo)

        self.ui.progressBar.setValue(0)

        #celda = QTableWidgetItem("Hola")
        #self.ui.table.setItem(1,1,celda)

        

        #self.pushButton.clicked.connect(self.hola)
    def config(self):
  
        archivo=QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\','Archivos xml (*.xml)')
        try:
            #Tomo la posición 0 de la ruta, pues QFileDialog retorna la ruta y el tipo de archivo
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


    def info(self):
        QMessageBox.about(self, "Ayuda", "© Digital Intelligence S.A. 2021\nSimulacion de ensamblado de productos\n")
        
    def about(self):
        QMessageBox.about(self, "Sobre el programador", "Luisa María Ortíz Romero\n\n4to semestre\nIngeniería en Ciencias y Sistemas\nUniversidad de San Carlos de Guatemala")

    def agregarComponentes(self, producto):
        self.ui.list_componentes.clear()
        self.ui.table.clear()
        self.ui.temporizador.display(0)
        self.ui.progressBar.setValue(0)
        if producto!="Seleccionar":
            producto=self.maquina.productos.getProducto(producto) #Producto actual
            cola=producto.elaboracion
            
            elemento=cola.primero

            while elemento is not None:
                self.ui.list_componentes.addItem(elemento.componente)
                elemento=elemento.siguiente

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
            if not producto.simulado:
                cola=producto.elaboracion
                
                elemento=cola.primero
                #Encuentra los componentes a los que espera llegar cada línea antes de ensamblar por primera vez
                self.asignarSiguientes(elemento)
        

                #Vuelvo a recorrer la cola desde el inicio para comenzar los movimientos
                elemento=cola.primero
                proximo=cola.primero
                proximo_linea=proximo.linea
                proximo_linea=int(proximo_linea.replace("L","")) 
                proximo_componente=proximo.componente
                proximo_componente=int(proximo_componente.replace("C",""))

                #print(proximo_linea)
                #print(proximo_componente)

                columnas=0
                ultimo=cola.ultimo

                linea_actual=self.maquina.lineas.primero

                tiempo=1
                x=0
                producto.segundos.agregar(tiempo)
               
                while proximo is not None: 
                    
                    numero=elemento.linea
                    numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                    componente=elemento.componente
                    componente=int(componente.replace("C",""))
                    linea=self.maquina.lineas.getLinea(numero)
                    if not elemento.ensamblado:

                        if linea.disponible:
                        
                            self.maquina.lineas.setOcupada(numero)
                            if linea.componente_actual==linea.componente_siguiente:
                                if linea.componente_actual==proximo_componente and linea.numero==proximo_linea and componente==linea.componente_actual:
                                    
                                    proximo=proximo.siguiente
                                    for ensamble in range(0,linea.tiempo):
                                        accion=self.maquina.lineas.ensamblar(linea.numero,linea.componente_actual)
                                        segundo=producto.segundos.getSegundo(tiempo)
                                        segundo.acciones.agregar(linea.numero,accion)
                                        
                                        tiempo+=1
                                        producto.segundos.agregar(tiempo)
                                        
                                        #print("Segundo: ", tiempo)
                                    self.maquina.lineas.liberarLineas()
                                    
                                    if proximo is None:
                                        break
                                    proximo_linea=proximo.linea
                                    proximo_linea=int(proximo_linea.replace("L","")) 
                                    proximo_componente=proximo.componente
                                    proximo_componente=int(proximo_componente.replace("C",""))

                                    producto.elaboracion.finalizado(elemento.linea, elemento.componente)
                                    x+=5
                                    self.ui.progressBar.setValue(x)
                                    elemento=producto.elaboracion.primero
                                    self.asignarSiguientes(elemento)
                                    
                                    #print("Segundo: ", tiempo)
                                    continue
                            elif linea.componente_siguiente is not None and linea.componente_actual<linea.componente_siguiente:
                
                                accion=self.maquina.lineas.moverAdelante(numero, linea.componente_actual)
                                segundo=producto.segundos.getSegundo(tiempo)
                                segundo.acciones.agregar(linea.numero,accion)
                            elif linea.componente_siguiente is not None and linea.componente_actual>linea.componente_siguiente:

                                accion=self.maquina.lineas.moverAtras(numero, linea.componente_actual)
                                segundo=producto.segundos.getSegundo(tiempo)
                                segundo.acciones.agregar(linea.numero,accion)
                        
    
                    elemento=elemento.siguiente
                    if elemento is None:
                        elemento=producto.elaboracion.primero
                        
                        tiempo+=1
                        producto.segundos.agregar(tiempo)
                    # print("Segundo: ", tiempo)
                        self.maquina.lineas.liberarLineas()

                self.maquina.productos.setSimulado(producto.nombre)        
                self.ui.temporizador.display(tiempo-1)
                self.ui.progressBar.setValue(100)
           
            else:
                final=producto.segundos.ultimo
                self.ui.temporizador.display(final.segundo-1)
                self.ui.progressBar.setValue(100)

        
        final=producto.segundos.ultimo
        self.ui.table.setRowCount(final.segundo)
        self.ui.table.setColumnCount(self.maquina.n)
        headers = QTableWidgetItem("Segundo")
        self.ui.table.setVerticalHeaderItem(0,headers)
        #Agrego las cabeceras de las columnas
        for columnas in range (0,self.maquina.n):
            header = QTableWidgetItem("Linea "+ str(columnas+1))
            self.ui.table.setHorizontalHeaderItem(columnas,header)

        #Agrego las cabeceras de las filas
        for fila in range (1,final.segundo):
            header = QTableWidgetItem(str(fila))
            self.ui.table.setVerticalHeaderItem(fila,header)

        #Agrego los movimientos a la tabla
        tempo=producto.segundos.primero
        for fila in range(1,final.segundo+1):
            for columna in range(0,self.maquina.n):
                celda = QTableWidgetItem("No hacer nada")
                self.ui.table.setItem(fila,columna,celda)
            #tempo=tempo.siguiente

        while tempo is not None:
            acci=tempo.acciones
            action=acci.primero
            while action is not None:
                celda = QTableWidgetItem(action.accion)
                self.ui.table.setItem(tempo.segundo,action.linea-1,celda)
                action=action.siguiente
                


            tempo=tempo.siguiente


        #Haciendo el reporte HTML
        html=open('HTML\\Simulación_'+producto.nombre+'.html','w')
        body="""
        <!DOCTYPE html>
        <html>
        <head>
        <title> Simulación_ """+producto.nombre+"""</title>
        </head>
        <body>
        <table border="1px" cellspacing=0>
        """
        
        final=producto.segundos.ultimo
   
        cabeceras="<tr><th>Tiempo</th>"
        #Agrego las cabeceras de las columnas
        for columnas in range (0,self.maquina.n):
            cabeceras+="<th> Linea "+str(columnas+1)+"</th>"
         

        celdas=""

        
        

        body+="<h2> Producto: "+producto.nombre+"</h2> "
        body+="<h3> Tiempo de ensamblaje: "+str(final.segundo-1)+" segundos</h2> "
        body+="<h2>Proceso</h2> "

        for fila in range(1,final.segundo):
            celdas+="<tr>"
            celdas+="<td>"+str(fila)+"</td>"
            for columna in range(0,self.maquina.n):
                lleno=False
                tempo=producto.segundos.primero
                while tempo is not None:
                    acci=tempo.acciones
                    action=acci.primero
                    while action is not None:
                        if columna+1==action.linea and fila==tempo.segundo:
                            celdas+='<td style="width:100px">'+action.accion+"</td>"
                            lleno=True
                        
                        action=action.siguiente
                    tempo=tempo.siguiente
                if not lleno:
                    celdas+='<td style="width:100px">No hacer nada</td>'
            celdas+="</tr>"
            celdas+="\n"
            

        cabeceras+="<tr>"
        body+=cabeceras
        body+=celdas
        body+="""
        </body>
        </html>
        """
        html.write(body)
        html.close()

        xml=open('XML\\Simulacion_'+producto.nombre+'.xml','w')
        content="""<?xml version="1.0" encoding="UTF-8"?>
<SalidaSimulacion>
\t<Nombre>
\t\tSimulacion_"""+producto.nombre+"""
\t</Nombre>
\t<ListadoProductos>
\t\t<Producto>
\t\t\t<Nombre>
\t\t\t\t"""+producto.nombre+"""
\t\t\t</Nombre>
\t\t\t<TiempoTotal> """+str(final.segundo-1)+""" </TiempoTotal>
\t\t\t<ElaboracionOptima>
"""
        tempo=producto.segundos.primero
        for fila in range(1,final.segundo):
            content+='\t\t\t\t<Tiempo NoSegundo="'+str(fila)+'">\n'
            for columna in range(1,self.maquina.n+1):
                content+='\t\t\t\t\t<LineaEnsamblaje NoLinea="'+str(columna)+'">\n'
                lleno=False
                tempo=producto.segundos.primero
                while tempo is not None:
                    acci=tempo.acciones
                    action=acci.primero
                    while action is not None:
                        if columna==action.linea and fila==tempo.segundo:
                            content+='\t\t\t\t\t\t'+action.accion+'\n'
                            lleno=True
                        
                        action=action.siguiente
                    tempo=tempo.siguiente
                if not lleno:
                    content+='\t\t\t\t\t\tNo hacer nada\n'   
            content+='\t\t\t\t\t</LineaEnsamblaje>\n'
            content+='\t\t\t\t</Tiempo>\n'

          
                       
        content+="""\t\t\t</ElaboracionOptima>
\t\t</Producto>
\t</ListadoProductos>
</SalidaSimulacion>
        """
        xml.write(content)
        xml.close()


        
        
        

        self.ui.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.table.resizeColumnsToContents()
        self.maquina.lineas.Reestablecer()      
                
            

    def asignarSiguientes(self, elemento):
        while elemento is not None:
                numero=elemento.linea
                numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                componente=elemento.componente
                componente=int(componente.replace("C",""))
                linea=self.maquina.lineas.getLinea(numero)
                if linea.componente_siguiente==None and not elemento.ensamblado:
                    self.maquina.lineas.setComponenteSiguiente(numero,componente) #Asigno el componente en todo el sistema
                    linea.componente_siguiente=componente #Asigno el componente de manera local
                    self.limite_linea=numero
                    self.limite_componente=linea.componente_siguiente

                    
                    #'''El componente siguiente es la base para comenzar a mover las líneas'''
                
                elemento=elemento.siguiente

    def leerSimulacion(self):
        if self.maquina is None:
            QMessageBox.about(self, "Eror", "No se ha configurado la máquina")
        else:


            archivo=QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\','Archivos xml (*.xml)')
            try:
                self.ui.B_siguiente.setEnabled(True)
                tree = ET.parse(archivo[0])
                root = tree.getroot()  
                for Ma in root:
                    for n in Ma.iter('Nombre'):
                        a=n.text
                        a=a.replace('\t','')
                        a=a.replace('\n','')
                        a=a.replace('    ','')
                        self.archivoActual=a
                    
                    #Busco cada producto
                    for listado in Ma.iter('ListadoProductos'):
                        for producto in listado.iter('Producto'):
                            nombre=producto.text
                            nombre=nombre.replace('    ','')
                            nombre=nombre.replace('\t','')
                            nombre=nombre.replace('\n','')
                            
                            self.ui.comboBox.setCurrentText(nombre)
                            self.maquina.simulacionMasiva.agregar(nombre)

                xml=open('XML\\'+self.archivoActual+'.xml','w')
                content="""<?xml version="1.0" encoding="UTF-8"?>
<SalidaSimulacion>
\t<Nombre>
\t\t"""+self.archivoActual+"""
\t</Nombre>
\t<ListadoProductos>"""
                xml.write(content)
                xml.close()
                    
                self.simularMasivo()
                            

            
                QMessageBox.about(self, "Notificación", "¡Simulación Iniciada!")
            except:
                QMessageBox.about(self, "Advertencia", "No es posible abrir el archivo")

    def simularMasivo(self):

        actual=self.maquina.simulacionMasiva.primero
        self.ui.comboBox.setCurrentText(actual.nombre)
        self.agregarComponentes(actual.nombre)

        if actual is not None:
            self.ui.B_play.setEnabled(False)
            producto=self.maquina.productos.getProducto(actual.nombre) #Producto actual
            if not producto.simulado:
                cola=producto.elaboracion
                
                elemento=cola.primero
                #Encuentra los componentes a los que espera llegar cada línea antes de ensamblar por primera vez
                self.asignarSiguientes(elemento)
        

                #Vuelvo a recorrer la cola desde el inicio para comenzar los movimientos
                elemento=cola.primero
                proximo=cola.primero
                proximo_linea=proximo.linea
                proximo_linea=int(proximo_linea.replace("L","")) 
                proximo_componente=proximo.componente
                proximo_componente=int(proximo_componente.replace("C",""))

                #print(proximo_linea)
                #print(proximo_componente)

                columnas=0
                ultimo=cola.ultimo

                linea_actual=self.maquina.lineas.primero

                tiempo=1
                x=0
                producto.segundos.agregar(tiempo)
               
                while proximo is not None: 
                    
                    numero=elemento.linea
                    numero=int(numero.replace("L","")) #Reemplazo las letras porque las líneas y componentes están almacenados como enteros
                    componente=elemento.componente
                    componente=int(componente.replace("C",""))
                    linea=self.maquina.lineas.getLinea(numero)
                    if not elemento.ensamblado:

                        if linea.disponible:
                        
                            self.maquina.lineas.setOcupada(numero)
                            if linea.componente_actual==linea.componente_siguiente:
                                if linea.componente_actual==proximo_componente and linea.numero==proximo_linea and componente==linea.componente_actual:
                                    
                                    proximo=proximo.siguiente
                                    for ensamble in range(0,linea.tiempo):
                                        accion=self.maquina.lineas.ensamblar(linea.numero,linea.componente_actual)
                                        segundo=producto.segundos.getSegundo(tiempo)
                                        segundo.acciones.agregar(linea.numero,accion)
                                        
                                        tiempo+=1
                                        producto.segundos.agregar(tiempo)
                                        
                                        #print("Segundo: ", tiempo)
                                    self.maquina.lineas.liberarLineas()
                                    
                                    if proximo is None:
                                        break
                                    proximo_linea=proximo.linea
                                    proximo_linea=int(proximo_linea.replace("L","")) 
                                    proximo_componente=proximo.componente
                                    proximo_componente=int(proximo_componente.replace("C",""))

                                    producto.elaboracion.finalizado(elemento.linea, elemento.componente)
                                    x+=5
                                    self.ui.progressBar.setValue(x)
                                    elemento=producto.elaboracion.primero
                                    self.asignarSiguientes(elemento)
                                    
                                    #print("Segundo: ", tiempo)
                                    continue
                            elif linea.componente_siguiente is not None and linea.componente_actual<linea.componente_siguiente:
                
                                accion=self.maquina.lineas.moverAdelante(numero, linea.componente_actual)
                                segundo=producto.segundos.getSegundo(tiempo)
                                segundo.acciones.agregar(linea.numero,accion)
                            elif linea.componente_siguiente is not None and linea.componente_actual>linea.componente_siguiente:

                                accion=self.maquina.lineas.moverAtras(numero, linea.componente_actual)
                                segundo=producto.segundos.getSegundo(tiempo)
                                segundo.acciones.agregar(linea.numero,accion)
                        
    
                    elemento=elemento.siguiente
                    if elemento is None:
                        elemento=producto.elaboracion.primero
                        
                        tiempo+=1
                        producto.segundos.agregar(tiempo)
                    # print("Segundo: ", tiempo)
                        self.maquina.lineas.liberarLineas()

                self.maquina.productos.setSimulado(producto.nombre)        
                self.ui.temporizador.display(tiempo-1)
                self.ui.progressBar.setValue(100)
                
           
            else:
                final=producto.segundos.ultimo
                self.ui.temporizador.display(final.segundo-1)
                self.ui.progressBar.setValue(100)
           
        else:
            self.ui.B_play.setEnabled(True)

        
        final=producto.segundos.ultimo
        self.ui.table.setRowCount(final.segundo)
        self.ui.table.setColumnCount(self.maquina.n)
        headers = QTableWidgetItem("Segundo")
        self.ui.table.setVerticalHeaderItem(0,headers)
        #Agrego las cabeceras de las columnas
        for columnas in range (0,self.maquina.n):
            header = QTableWidgetItem("Linea "+ str(columnas+1))
            self.ui.table.setHorizontalHeaderItem(columnas,header)

        #Agrego las cabeceras de las filas
        for fila in range (1,final.segundo):
            header = QTableWidgetItem(str(fila))
            self.ui.table.setVerticalHeaderItem(fila,header)

        #Agrego los movimientos a la tabla
        tempo=producto.segundos.primero
        for fila in range(1,final.segundo+1):
            for columna in range(0,self.maquina.n):
                celda = QTableWidgetItem("No hacer nada")
                self.ui.table.setItem(fila,columna,celda)
            #tempo=tempo.siguiente

        while tempo is not None:
            acci=tempo.acciones
            action=acci.primero
            while action is not None:
                celda = QTableWidgetItem(action.accion)
                self.ui.table.setItem(tempo.segundo,action.linea-1,celda)
                action=action.siguiente
                


            tempo=tempo.siguiente


        #Haciendo el reporte HTML
        html=open('HTML\\Simulación_'+producto.nombre+'.html','w')
        body="""
        <!DOCTYPE html>
        <html>
        <head>
        <title> Simulación_ """+producto.nombre+"""</title>
        </head>
        <body>
        <table border="1px" cellspacing=0>
        """
        
        final=producto.segundos.ultimo
   
        cabeceras="<tr><th>Tiempo (s)</th>"
        #Agrego las cabeceras de las columnas
        for columnas in range (0,self.maquina.n):
            cabeceras+="<th> Linea "+str(columnas+1)+"</th>"
         

        #Agrego los movimientos a la tabla
        celdas=""
        #for fila in range(1,final.segundo):
            #celdas+="</tr>"
            #celdas+="<td>"+str(fila)+"</td>"
            #for columna in range(0,self.maquina.n):
               
                #celdas+="<td>No hacer nada</td>"
            #celdas+="</tr>"

        
        

        body+="<h2> Producto: "+producto.nombre+"</h2> "
        body+="<h3> Tiempo de ensamblaje: "+str(final.segundo-1)+" segundos</h2> "
        body+="<h2>Proceso</h2> "

        for fila in range(1,final.segundo):
            celdas+="<tr>"
            celdas+="<td>"+str(fila)+"</td>"
            for columna in range(0,self.maquina.n):
                lleno=False
                tempo=producto.segundos.primero
                while tempo is not None:
                    acci=tempo.acciones
                    action=acci.primero
                    while action is not None:
                        if columna+1==action.linea and fila==tempo.segundo:
                            celdas+='<td style="width:100px">'+action.accion+"</td>"
                            lleno=True
                        
                        action=action.siguiente
                    tempo=tempo.siguiente
                if not lleno:
                    celdas+='<td style="width:100px">No hacer nada</td>'
            celdas+="</tr>"
            celdas+="\n"
            

        cabeceras+="<tr>"
        body+=cabeceras
        body+=celdas
        body+="""
        </body>
        </html>
        """
        html.write(body)
        html.close()

        xml=open('XML\\'+self.archivoActual+'.xml','a')

        content="""\n\t\t<Producto>
\t\t\t<Nombre>
\t\t\t\t"""+producto.nombre+"""
\t\t\t</Nombre>
\t\t\t<TiempoTotal> """+str(final.segundo-1)+""" </TiempoTotal>
\t\t\t<ElaboracionOptima>
"""
        tempo=producto.segundos.primero
        for fila in range(1,final.segundo):
            content+='\t\t\t\t<Tiempo NoSegundo="'+str(fila)+'">\n'
            for columna in range(1,self.maquina.n+1):
                content+='\t\t\t\t\t<LineaEnsamblaje NoLinea="'+str(columna)+'">\n'
                lleno=False
                tempo=producto.segundos.primero
                while tempo is not None:
                    acci=tempo.acciones
                    action=acci.primero
                    while action is not None:
                        if columna==action.linea and fila==tempo.segundo:
                            content+='\t\t\t\t\t\t'+action.accion+'\n'
                            lleno=True
                        
                        action=action.siguiente
                    tempo=tempo.siguiente
                if not lleno:
                    content+='\t\t\t\t\t\tNo hacer nada\n'   
            content+='\t\t\t\t\t</LineaEnsamblaje>\n'
            content+='\t\t\t\t</Tiempo>\n'

          
                       
        content+="""\t\t\t</ElaboracionOptima>
\t\t</Producto>"""

        xml.write(content)
        xml.close()

        
        
        

        self.ui.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.table.resizeColumnsToContents()
        self.maquina.lineas.Reestablecer()
        self.maquina.simulacionMasiva.desencolar()

        if self.maquina.simulacionMasiva.primero is None:
            self.ui.B_siguiente.setEnabled(False)
            self.ui.B_play.setEnabled(True)

            xmlf=open('XML\\'+self.archivoActual+'.xml','a')
            contentf="""\n\t</ListadoProductos>\n</SalidaSimulacion>"""
            xmlf.write(contentf)
            xmlf.close()

    

if __name__=='__main__':
    app=QApplication(sys.argv)
    GUI=Ventana()
    GUI.show()
    sys.exit(app.exec_())