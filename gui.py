#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog,QPushButton, QMessageBox,QTableWidget,QTableWidgetItem
import pandas as pd
import os.path as path
import os
import random
import sys
import csv
import glob

class inicio(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("inter.ui", self)
        self.pushButton.clicked.connect(self.ver_sentencia)
        self.tablas.setColumnCount(2)
        self.tablas.setHorizontalHeaderLabels(['Tabla','Total'])
        self.all_tables()

    def ver_sentencia(self):
        self.identificar(self.lineEdit.text())
        #QMessageBox.about(self, 'PyQt5 message', self.lineEdit.text())
    
    def identificar(self,sentencia):
        lista_tokens = sentencia.split(" ")
        # crear_tabla curso (id:int(10),nombre:var(30),programa:int)
        sent = lista_tokens.pop(0)
        if( sent == 'crear_tabla'):
            self.crear_tabla(lista_tokens)
        
        # inserta curso (id,nombre,programa) (1,matematica,101)
        elif( sent == 'inserta'):
            tabla = lista_tokens.pop(0)
            lista_attr = lista_tokens.pop(0)[1 : -1].split(",")
            lista_datos = lista_tokens.pop(0)[1 : -1].split(",")
            df = pd.read_csv('database/datos_'+tabla+'.csv')
            df = df.append(pd.Series(lista_datos, index=lista_attr), ignore_index=True)
            df.to_csv('database/datos_'+tabla+'.csv', index=False)
            QMessageBox.about(self, 'Base de Datos', 'Insertó correctamente '+ str(lista_datos))
            #self.show_table('datos_'+tabla)
        
        # inserta_rand curso (id,nombre,programa) (auto(1),str(1;curso),nrand(10;17)) 10
        elif( sent == 'inserta_rand'):
            tabla = lista_tokens.pop(0)
            lista_attr = lista_tokens.pop(0)[1 : -1].split(",")
            lista_datos = lista_tokens.pop(0)[1 : -1].split(",")
            total = int(lista_tokens.pop(0))
            df = pd.read_csv('database/datos_'+tabla+'.csv')
            nf = pd.DataFrame({},columns= lista_attr)
            k = 0
            for i in lista_datos:
                arr = []
                if('auto' in i[:i.find('(')]):
                    first = int( i[i.find('(')+1 : i.find(')')])
                    arr = list(range(first, first+total))
                elif('str' in i[:i.find('(')]):
                    strn = i[i.find('(')+1 : i.find(')')].split(";")
                    arr = self.str_auto(int(strn[0]), strn[1], total)
                elif('nrand' in i[:i.find('(')]):
                    rand = i[i.find('(')+1 : i.find(')')].split(";")
                    arr = [random.randrange(int(rand[0]), int(rand[1]), 1) for _ in range(total)]
                else:
                    arr = self.only_str(i,total)
                n_arr = df[lista_attr[k]].tolist() + arr
                nf[lista_attr[k]] = pd.Series(n_arr)
                k=k+1
            print("Ingresaso correctamente", total)
            nf.to_csv('database/datos_'+tabla+'.csv', index=False)
            QMessageBox.about(self, 'Base de Datos', 'Insertó correctamente '+ str(total)+"\nCantidad total de filas "+str(nf.shape[0]))
        
        # select curso where nombre=curso_4
        elif(sent == 'select'):
            tabla = lista_tokens.pop(0)                
            df = pd.read_csv('database/datos_'+tabla+'.csv')
            mitabla = pd.read_csv('database/tabla_'+tabla+'.csv')
            if not lista_tokens:
                self.show_table('datos_'+tabla)
            elif lista_tokens.pop(0) == 'where':
                condicion = lista_tokens.pop(0).split('=')
                tipo = mitabla.loc[mitabla['columna'] == condicion[0]]
                val = condicion[1]
                validar = tipo['tipo'] == 'int'
                if validar.bool():
                    res = df.loc[df[condicion[0]] == int(val)]
                else:
                    res = df.loc[df[condicion[0]] == val]
                print(condicion, res)
                res.to_csv('database/select.csv', index=False)
                self.show_table('select')
            else:
                QMessageBox.about(self, 'Base de Datos', 'Error de sintaxis')
            #print(lista_tokens)
        
        # delete curso where nombre=curso_7
        elif(sent == 'delete'):
            tabla = lista_tokens.pop(0)                
            df = pd.read_csv('database/datos_'+tabla+'.csv')
            mitabla = pd.read_csv('database/tabla_'+tabla+'.csv')
            
            if lista_tokens.pop(0) == 'where':
                condicion = lista_tokens.pop(0).split('=')
                tipo = mitabla.loc[mitabla['columna'] == condicion[0]]
                val = condicion[1]
                validar = tipo['tipo'] == 'int'
                if validar.bool():
                    res = df.loc[df[condicion[0]] == int(val)]
                else:
                    res = df.loc[df[condicion[0]] == val]
                nf = df.drop(res.index.tolist())
                print(condicion, res.index.tolist())
                nf.to_csv('database/datos_'+tabla+'.csv', index=False)
                QMessageBox.about(self, 'Base de Datos', 'Eliminado correctamente')
                self.show_table('datos_'+tabla)
            else:
                QMessageBox.about(self, 'Base de Datos', 'Error de sintaxis')
        
        # update curso set nombre=matematica where id=6
        elif(sent == 'update'):
            tabla = lista_tokens.pop(0)                
            df = pd.read_csv('database/datos_'+tabla+'.csv')
            mitabla = pd.read_csv('database/tabla_'+tabla+'.csv')
            if lista_tokens.pop(0) == 'set':
                update = lista_tokens.pop(0).split('=')

                if lista_tokens.pop(0) == 'where':
                    condicion = lista_tokens.pop(0).split('=')
                    tipo = mitabla.loc[mitabla['columna'] == condicion[0]]
                    val = condicion[1]
                    validar = tipo['tipo'] == 'int'
                    if validar.bool():
                        res = df.loc[df[condicion[0]] == int(val)]
                    else:
                        res = df.loc[df[condicion[0]] == val]
                    indices = res.index.tolist()
                    print(indices)
                    df[update[0]].iloc[indices] = update[1]
                    df.to_csv('database/datos_'+tabla+'.csv', index=False)
                    QMessageBox.about(self, 'Base de Datos', 'Modificado correctamente')
                    self.show_table('datos_'+tabla)
                else:
                    QMessageBox.about(self, 'Base de Datos', 'Error de sintaxis')
                
        # drop curso
        elif(sent == 'drop'):
            tabla = lista_tokens.pop(0)
            if (path.isfile('database/tabla_'+tabla+'.csv')):
                os.remove('database/tabla_'+tabla+'.csv')
                os.remove('database/datos_'+tabla+'.csv')
                QMessageBox.about(self, 'Base de Datos', 'Eliminado correctamente tabla y datos de '+tabla)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        # show curso    
        elif(sent == 'show'):
            tabla = lista_tokens.pop(0)
            self.show_table('tabla_'+tabla)

        self.all_tables()


    def only_str(self, name , total):
        arr = []
        for i in range(total):
            arr.append(name)
        return arr

    def str_auto(self,first,name,total):
        arr = []
        for i in range(total):
            arr.append(name+'_'+str(first))
            first+=1
        return arr

    def crear_tabla (self,lista_tokens):
        tabla = lista_tokens.pop(0)
        if not(path.isfile('database/tabla_'+tabla+'.csv')):
            lista_attr = lista_tokens[0][1 : -1].split(",")
            datos = []
            for i in lista_attr:
                lista_valor = i.split(':')
                attr = lista_valor.pop(0)
                tipo = lista_valor.pop(0)
                tip = tipo[0:3]
                if '(' in tipo:
                    tam = tipo[tipo.find('(')+1:tipo.find(')')]
                elif tip == 'int':
                    tam = '8'
                elif tip == 'var':
                    tam = '4'
                dato = [attr,tip,tam]
                datos.append(dato)
            columnas = ['columna','tipo','tam']
            self.guardar_csv(tabla, columnas, datos)
        else:
            QMessageBox.about(self, 'Base de Datos', 'La tabla '+tabla+' ya existe.')

    def guardar_csv (self, tabla, columnas, datos):
        df = pd.DataFrame(data=datos,columns=columnas)
        df.to_csv('database/tabla_'+tabla+'.csv', index=False)
        tf = pd.DataFrame({},columns=df[columnas[0]])
        tf.to_csv('database/datos_'+tabla+'.csv', index=False)
        print(df)
        self.show_table('tabla_'+tabla)

    
    def show_table (self, name):
        if not(path.isfile('database/'+name+'.csv')):
            QMessageBox.about(self, 'Base de Datos', 'No existe.')
            return 
        dataframe = pd.read_csv('database/'+name+'.csv')
        print(dataframe)
        # cambio tamanio
        self.tableWidget.setRowCount(dataframe.shape[0])
        self.tableWidget.setColumnCount(dataframe.shape[1])
        #lleno tableWidget
        df_columns = list(dataframe)
        self.tableWidget.setHorizontalHeaderLabels(df_columns)
        for i,row in dataframe.iterrows():
            for j in range(len(df_columns)):
                self.tableWidget.setItem(i,j, QTableWidgetItem(str(row[df_columns[j]]))) 

    def all_tables (self):
        files = glob.glob('database/tabla_*.csv')
        print(files)
        self.tablas.setRowCount(len(files))
        k=0
        for i in files:
            name = i[i.find('\\')+1:i.find('.')]
            tabla = name[name.find('_')+1:]
            dt = pd.read_csv('database/datos_'+tabla+'.csv')
            self.tablas.setItem(k,0, QTableWidgetItem(tabla)) 
            self.tablas.setItem(k,1, QTableWidgetItem(str(dt.shape[0])))
            k=k+1


#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
_ventana = inicio()
_ventana.show()
app.exec_()
#"""

#que hace demorar a los bloques calcular tabla
#10 de V o F
#arbolito (4)
#tabla de indices (2)
#2 preguntas de sql (4)
#1 pregunta cultura general tree b (2)