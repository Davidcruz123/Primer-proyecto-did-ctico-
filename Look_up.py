from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import pandas as pd
import numpy as np
import Mysql
import Paso2

class lookup:
    def __init__(self):

        self.Funcionusers = Paso2.users()
        usuario_en_lista=['usuario']
        usuario=[]
        datos_query=self.Funcionusers.db.query2('audit_trail',usuario_en_lista)
        for datos in datos_query:
            usuario.append(datos[0])

        self.usuario_ingresado=usuario[len(usuario)-1]


        self.abrir_vent_look_up()





    def abrir_vent_look_up(self):

        ventana2=Tk()
        self.wind = ventana2
        self.wind.title('Look-up')

        # Creando un Frame.... es un cuadro que adentro me permite tener elementos
        cuadro = LabelFrame(self.wind, text='Ingrese Datos')  # titulo del cuadro
        cuadro.grid(row=0, column=0, columnspan=3,
                    pady=20)  # Donde se colocará    el span es que 3 columnas se dejaran sin contenido
        # pad es un espaciado para que los elementos no se vean tan juntos

        #Boton Buscar exel
        self.boton_busc_exc = ttk.Button(cuadro, text='Seleccione archivo excel a abrir',command=self.buscarexel).grid(row=1, columnspan=2, sticky=W + E)

        # Columna 1 input
        Label(cuadro, text='Seleccione la columna donde se encuentra el valor deseado: ').grid(row=2,
                                                                                               column=0)  # Crear el texto
        self.inp1 = Entry(cuadro)  # Crear la caja de texto...Es un imput donde el usuario agrega datos
        # Lo que se agrege se guardará en la propiedad llamada name
        self.inp1.grid(row=2, column=1)
        self.inp1.config(state='disabled')

        # Valor a buscar input
        Label(cuadro, text='Seleccione el valor a buscar: ').grid(row=3, column=0)
        self.inp2 = Entry(cuadro)
        self.inp2.grid(row=3, column=1)
        self.inp2.config(state='disabled')

        # Columna 2 input
        Label(cuadro, text='Seleccione la columna donde se encuentra el valor a devolver: ').grid(row=4, column=0)
        self.inp3 = Entry(cuadro)
        self.inp3.grid(row=4, column=1)
        self.inp3.config(state='disabled')

        # Botón

        self.aa = ttk.Button(cuadro, text='Revisar',state='disabled',command=self.func_lookup)  # W+E es de oeste a este, es decir
        self.aa.grid(row=8, columnspan=2,sticky=W + E)
        #Boton Volver
        self.Boton_atras = ttk.Button(ventana2, text='Cerrar sesión',command=self.cerrar_sesion)
        self.Boton_atras.grid(row=9,columnspan=4)
        self.wind.mainloop()

    def cerrar_sesion(self):

        # Paso2.users.abrir_ventana_principal()
        self.wind.destroy()
        # Funcionusers = Paso2.users()
        evento = 'Se cerró sesión'
        self.Funcionusers.audit_trail1(evento)
        Inicio =self.Funcionusers.abrir_ventana_principal()






    def buscarexel(self):

        filename = askopenfilename(filetypes=[("Excel files", ".csv .xls .xlsx")])  # Se abre el buscador de archivos
        print(askopenfilename,"                ",filename)

        if filename.endswith('.csv') or filename.endswith('.xlsx'):
            archivocorrecto=True
            es_csv=filename.endswith('.csv')
        else:
            archivocorrecto=False

        
        print(archivocorrecto)

        if archivocorrecto:  # Es verdadero si la extensión encontrada termina en .csv o .xlsx



            if es_csv:
                self.df = pd.read_csv(filename)  # Se convierte el archivo en un dataframe
            else:
                self.df = pd.read_excel(filename)
            print(self.df)

            self.inp1['state'] = 'normal'
            self.inp2['state'] = 'normal'
            self.inp3['state'] = 'normal'
            self.aa['state'] = 'normal'
            self.aa.config(state = 'normal')

            self.aa['state'] = 'normal'
            evento='Se ha seleccionado un archivo csv'


            self.Funcionusers.audit_trail2(evento,self.usuario_ingresado)

    def func_lookup(self):
        columna = str(self.inp1.get())

        objetivo = str(self.inp2.get())
        columna2 = str(self.inp3.get())

    

        if columna in list(self.df.columns):  # df. columns me tira las columnas del df
            columna_en_lista = list(self.df[columna])
            condicion1 = True
            if objetivo in columna_en_lista:
                indice_fila = columna_en_lista.index(objetivo)
                condicion2 = True
            else:
                condicion2 = False


        else:
            condicion1 = False

        if columna2 in list(self.df.columns):
            columna2_en_lista = list(self.df[columna2])
            indice_de_columna2 = list(self.df.columns).index(columna2)
            condicion3 = True
        else:
            condicion3 = False

        if condicion1 and condicion2 and condicion3:
            messagebox.showwarning('Resultado', self.df.iloc[indice_fila, indice_de_columna2])
            evento3 = 'Se realizó una busqueda look up exitosa'

            self.Funcionusers.audit_trail2(evento3, self.usuario_ingresado)
        elif condicion1 == False:
            messagebox.showwarning('No se puede obtener el resultado',
                                   'El valor de columna a buscar el valor deseado no se encuentra en el archivo ')
        elif condicion2 == False:
            messagebox.showwarning('No se puede obtener el resultado',
                                   'El valor a buscar no se encuentra en el archivo ')
        elif condicion3 == False:
            messagebox.showwarning('No se puede obtener el resultado',
                                   'El valor de columna donde está el valor a devolver no se encuentra en el archivo ')
        elif condicion1 == False and condicion2 == False and condicion3 == False:
            messagebox.showwarning('No se puede obtener el resultado', 'No se han ingresado datos ')
        elif condicion2 == False and condicion3 == False:
            messagebox.showwarning('No se puede obtener el resultado',
                                   'No se ha ingresado la columna a buscar el valor deseado ')
        elif condicion1 == False and condicion3 == False:
            messagebox.showwarning('No se puede obtener el resultado', 'No se ingresado el valor a buscar ')
        else:
            messagebox.showwarning('No se puede obtener el resultado',
                                   'No se ingresado el valor de la columna donde está el valor a devolver ')






