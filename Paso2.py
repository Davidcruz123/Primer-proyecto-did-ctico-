
import Mysql
import correos
import mysql.connector
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import hashlib
from datetime import date,datetime,timedelta
import random
from Look_up import lookup

class users:  #Es para la funcionalidad de nuestras ventanas
    def __init__(self):
        self.db = Mysql.claseDatabase()
        evento1 = 'Se inició la aplicación'
        self.fecha = date.today()
        self.hora = datetime.now().strftime("%H:%M:%S")
        




    def abrir_ventana_principal(self):
        evento1 = 'Ventana abierta= Login'
        self.audit_trail1(evento1)
        window = Tk()
        self.wind = window
        self.wind.title('Login')
        self.wind.geometry('300x200')

        # Creando un cuadro_contenedor-Un cuadro que adentro me permite tener elementos
        cuadro_contenedor = LabelFrame(self.wind, text='Titulo')
        cuadro_contenedor.grid(row=0, column=0, columnspan=3, pady=20)

        # usuario
        Label(cuadro_contenedor, text='Usuario:').grid(row=1, column=0)
        self.usuario = Entry(cuadro_contenedor)
        self.usuario.grid(row=1, column=1)

        # Pasword
        Label(cuadro_contenedor, text='CLave:').grid(row=2, column=0)
        self.clave = Entry(cuadro_contenedor, show="*")  # Se usa show para ocultar la contrasena
        self.clave.grid(row=2, column=1)

        # Boton validar
        ttk.Button(cuadro_contenedor, text='Ingresar', command=self.validar).grid(row=3, columnspan=2, sticky=W + E,
                                                                                  pady=10)
        # Boton ingresar usuario

        ttk.Button(cuadro_contenedor, text='Registrar usuario', command=self.ventana_ingresar_usuario).grid(row=4,
                                                                                                            column=0)

        # Boton olvidaste pasw

        ttk.Button(cuadro_contenedor, text='¿Olvidaste la contraseña?', command=self.vent_restaurar_pasw).grid(row=4,
                                                                                                                     column=1)

        self.loopventanaprincipal=window.mainloop()
    def audit_trail1(self,evento):

        columnas_evento1 = ['evento', 'fecha', 'hora']
        valores_evento1 = [evento, self.fecha, self.hora]
        self.db.insert_data2('audit_trail', columnas_evento1, valores_evento1)

    def audit_trail2(self,evento,usuario):

        columnas_evento1 = ['usuario','evento', 'fecha', 'hora']
        valores_evento1 = [usuario,evento, self.fecha, self.hora]
        self.db.insert_data2('audit_trail', columnas_evento1, valores_evento1)

    def ventana_ingresar_usuario(self):
        # self.wind.withdraw()
        self.vent_ing_usuario=Toplevel()
        self.vent_ing_usuario.title('Ingrese nuevo usuario')
        self.cuadro_contenedor_2=LabelFrame(self.vent_ing_usuario,text='Titulo').grid(row=0,column=0,columnspan=3,pady=20)

        # usuario
        Label(self.vent_ing_usuario, text='Ingrese Usuario:').grid(row=2, column=0)
        self.ingrese_user = Entry(self.vent_ing_usuario)
        self.ingrese_user.grid(row=2, column=1)

        # Pasword
        Label(self.vent_ing_usuario, text='Ingrese CLave:').grid(row=3, column=0)
        self.ingrese_clave = Entry(self.vent_ing_usuario,show="*")
        self.ingrese_clave.grid(row=3, column=1)          #Siempre separar grid, de lo contrario, el get no funciona

        # mail
        Label(self.vent_ing_usuario, text='Ingrese Correo:').grid(row=1, column=0)
        self.ingrese_correo = Entry(self.vent_ing_usuario)
        self.ingrese_correo.grid(row=1, column=1)  # Siempre separar grid, de lo contrario, el get no funciona

        # Boton Guardar
        ttk.Button(self.vent_ing_usuario, text='Guardar usuario',command=self.insertar_datos).grid(row=4, columnspan=2, sticky=W + E, pady=10)
        # en los botones las funciones terminan sin parentesis, de lo contrario se ejecutan sin llamarlas
        #Boton Cancelar
        ttk.Button(self.vent_ing_usuario,text='Atras',command=self.vent_ing_usuario.destroy).grid(row=5, columnspan=2, pady=10)
        #El método grab_set() asegura que no haya eventos de raton o teclado que se envíen a otra ventana diferente a la que se está usando
        # Se utiliza para crear una ventana de tipo modal que será necesario cerrar para trabajar con tra diferente, con ello tambien se impide
        #que la misma ventana se abra varias veces

        self.vent_ing_usuario.grab_set()

    def cerrar_ventana(self,vent_cerrar,vent_abrir):
        vent_cerrar.destroy()
        vent_abrir.deiconify()
    def validar_correo(self,cadena):
        boolean = False
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', cadena.lower()):
            boolean = True
        return boolean
    def limpiar_entry(self,lista):
        for x in lista:
            x.delete(0, 'end')

    def insertar_datos(self):
        #Se obtienen los valores de lob botones, se convierte a str en caso que halla numeros
        usuario = str(self.ingrese_user.get())
        clave = str(self.ingrese_clave.get())
        correo=str(self.ingrese_correo.get())


        if usuario=="" and clave=="" and correo=="":    #si no se han ingresado datos
            messagebox.showerror('Error','No ha ingresado datos')
        elif usuario=="" and clave!="" and correo!="":        #vacio usuario
            messagebox.showwarning('Warning','Ingrese usuario')
        elif usuario!="" and clave==""and correo!="":        #Vacio clave
            messagebox.showwarning('Warning','Ingrese clave')
        elif usuario!="" and clave!="" and correo=="":        #vacio correo
            messagebox.showwarning('Warning', 'Ingrese correo')

        elif usuario!="" and clave!="" and correo!="":         #significa que los tres espacios tienen valores
            if len(clave)<4:
                messagebox.showwarning('Warning','La clave debe ser de mínimo 4 carácteres',)
            else:
                estado_correo=self.validar_correo(correo)            #se corrobora que sea un correo válido
                if estado_correo:
                    try:
                        clave_codificada = self.codificar(clave)

                        # Creamos un código aleatorio que será enviado al correo
                        base_de_datos = 'users'
                        columnass = ['usuario', 'clave', 'correo', 'codes']

                        aleatorio = str(random.randint(1000, 9999))
                        #Correo electrónico que se enviará
                        asunto=str("Codigo de activacion")
                        mensaje_enviar="Para activar su cuenta ingrese usuario y contrasena en la pestana login y presione ingresar, seguido a eso ingrese su codigo de activacion\n" \
                                       "Su codigo de activacion es {}".format(aleatorio)      # no se permiten tildes o dará error
                        print(asunto,mensaje_enviar,correo)
                        print(correo)


                        correos.mail(asunto,mensaje_enviar,correo)
                        print(aleatorio)
                        aleatorio_codificado = self.codificar(aleatorio)
                        valores = [usuario, clave_codificada, correo, aleatorio_codificado]
                        #Se agregan los valores ingresados a la db
                        self.db.insert_data2(base_de_datos, columnass, valores)
                        messagebox.showinfo('Exito', 'Se te enviará una clave de validación al correo')

                        limpiar_entry=[self.ingrese_correo,self.ingrese_clave,self.ingrese_user]
                        self.limpiar_entry(limpiar_entry)

                        evento3 = 'Se ha agregado un nuevo usuario: {}'.format(usuario)
                        self.audit_trail1(evento3)



                    except mysql.connector.errors.IntegrityError:     # se setió en mysql que no se permiten repetidos en correo o usuario
                        messagebox.showerror('Warning', 'Correo o usuario ya existente')
                        evento2 = 'Intento fallido agregar usuario'
                        self.audit_trail1(evento2)
                        print('revisando esta pistola')
                else:
                    messagebox.showwarning('Warning','Ingrese un correo valido')

        else:                                                                  #si los espacios estan vacios
            messagebox.showwarning('Warning', 'Faltan valores')


    def validar(self):
        datos_consulta = self.db.query()          # se pregunta por usuario,clave,correo y estado
        usuario = str(self.usuario.get())
        contrasena = (self.clave.get())
        validar = False
        contrasena_codificada = self.codificar(contrasena)


        if usuario != "" and contrasena != "":  # Si se ingresaron datos
            estado=''
            usuario_existe=False
            self.correo2=""
            correo=self.correo2
            for datos in datos_consulta:
                if datos[0] == usuario and datos[1] == contrasena_codificada:   #Si usuario y contrasena coinciden
                    validar = True                                              #Se crea una función validar, que me dice que usuario y contrasena coinciden
                    estado=datos[3]
                    self.correo2=datos[2]
                if datos[0] == usuario and datos[1] != contrasena_codificada: #si usuario coincide y contrasena no

                    usuario_existe=True                                        ##se crea usuario existente, para saber que usuario si coincide
                    correo=datos[2]                                            #Esto me ayudará a saber si un usuario está intentando ingresar
                    # correo=correo2
            if validar:  # Si son correctos
                if estado == 'Inactivo':
                    self.vent_activar_usuario()           #Si está inactivo abrimos la ventana de validación
                elif estado == "Bloqueado":
                    messagebox.showwarning('Usuario Bloqueado', 'Ingrese a olvidaste la contrasena' )     #Si está bloqueado lo mostramos
                else:
                    # se borra de valicación, para que no se bloqee en caso de ingresar mal el usuario y pasw
                    sql5 = "DELETE FROM validación WHERE usuario='{}'".format(usuario)
                    self.db.borrar(sql5)
                    #audit trail
                    evento = "{} ha iniciado sesion".format(usuario)
                    self.audit_trail2(evento, usuario)
                    #cerrar y abrir ventanas
                    self.user=usuario
                    self.wind.destroy()
                    lookup()



            else:  # si son incorrectos
                if usuario_existe and estado!='Bloqueado':                 #Usuario existe//// se ingresa usuario pero mal pasw
                    #Se borran los datos mas viejos a 5min
                    fecha = date.today()
                    hora_target = datetime.now() - timedelta(minutes=5)
                    hora_target2 = hora_target.strftime("%H:%M:%S")
                    sql="DELETE FROM validación WHERE (fecha<='{}' and hora<'{}') OR fecha<'{}'".format(fecha,hora_target2,fecha)
                    self.db.borrar(sql)
                    #Couantas veces está el usuario en el tiempo
                    columnas_validacion=['usuario','correo','fecha','hora']
                    query_validacion=self.db.query2('validación',columnas_validacion)

                    nueva_lista=[]
                    for datos in query_validacion:
                        nueva_lista.append(datos[0])
                    contador=nueva_lista.count(usuario)
                    # print(contador)

                    bloqueo=False
                    if contador==2:
                        sql2="UPDATE users SET estado='Bloqueado' WHERE usuario='{}' ".format(usuario)
                        self.db.borrar(sql2)
                        messagebox.showerror('Usuario Bloqueado', 'Ha excedido el numero permitido de intentos')
                        bloqueo=True
                        #audit trail
                        evento6 = 'Se ha bloqueado el correo: {}'.format(correo)
                        self.audit_trail1(evento6)



                    #Se ingresa el intento en la db
                    base_de_datos = 'validación'
                    columnass = ['usuario', 'correo','fecha','hora']
                    fecha = date.today()
                    hora = datetime.now().strftime("%H:%M:%S")
                    valores = [usuario, correo,fecha,hora]

                    self.db.insert_data2(base_de_datos, columnass, valores)

                    if bloqueo==False:
                        messagebox.showwarning('Warning', 'Datos invalidos', )

                else:
                    messagebox.showwarning('Warning', 'Datos invalidos*', )




        else:
            messagebox.showwarning('Warning', 'Datos invalidos', )



    def vent_activar_usuario(self):

        self.activar=Toplevel()
        self.activar.title('Activar usuario')
        self.activar.geometry('350x130')
        labelframe = LabelFrame(self.activar, text="Ingrese código de activación")
        labelframe.pack(fill="both", expand="yes")

        self.left = Entry(labelframe)
        self.left.pack()
        ttk.Button(labelframe, text='Activar',command=self.funcion_validar).pack()
        ttk.Button(labelframe, text='Atras', command=self.activar.destroy).pack()

        self.activar.grab_set()

    def funcion_validar(self):
        lista_columnas=['correo','codes']
        basedatos='users'
        validar_codigo=self.db.query2(basedatos,lista_columnas)       #
        mail=[]
        codes=[]
        for datos in validar_codigo:
            mail.append(datos[0])
            codes.append(datos[1])
        codigo_ingresado=self.left.get()
        codigo_ingresado_codificado=self.codificar(str(codigo_ingresado))
     
        if codigo_ingresado_codificado in codes:              #Si el codigo ingresado está entre la columa codigos

            indice=codes.index(codigo_ingresado_codificado)            #se obtiene el indice
            if mail[indice]==self.correo2:                    #solo es para comprobar que el codigo responda al correo dado
                sql3 = "UPDATE users SET estado='Activo' WHERE correo='{}' ".format(self.correo2)       #Se actualiza a activo
                self.db.borrar(sql3)
                messagebox.showinfo('Exito', 'Usuario activado correctamente')
                self.activar.destroy()
                evento4 = 'Se ha activado el correo: {}'.format(self.correo2)
                self.audit_trail1(evento4)
            else:
                print('ingresó un codigo erroneo')
        else:
            messagebox.showerror('No es posible activar', 'El código ingresado no es correcto')


    def vent_restaurar_pasw(self):
        limpiar_entry = [self.usuario, self.clave]
        self.limpiar_entry(limpiar_entry)
        try:
            self.cambiar_contraseña.destroy()           #Esto me permite al darle atras en la otra ventana, aparecer en esta
        except AttributeError:                          #Gracias al try, cuando no hemos creado la ventana cambiar contrasena
            print('Exepción ocurrida')                                #omitimos el error
        self.restaurar=Toplevel()
        self.restaurar.title('Restaurar contrasena')
        self.restaurar.geometry('350x130')
        labelframe = LabelFrame(self.restaurar, text="Ingrese córreo electrónico")
        labelframe.pack(fill="both", expand="yes")

        self.correo_ingresado = Entry(labelframe)
        self.correo_ingresado.pack()
        ttk.Button(labelframe, text='Obtener código de activación',command=self.restaurar_pasw).pack()
        ttk.Button(labelframe, text='Atras', command=self.restaurar.destroy).pack()

        self.restaurar.grab_set()


    def restaurar_pasw(self):

        lista_columnas = ['correo','estado']
        basedatos = 'users'
        validar_correo = self.db.query2(basedatos, lista_columnas)  #
        mail = []
        estado_lista=[]
        for datos in validar_correo:
            mail.append(datos[0])                                  #llamamos a la db, y hacemos una lista de correos
        for datos in validar_correo:
            estado_lista.append(datos[1])
        correo_ingresado = self.correo_ingresado.get()


        if correo_ingresado in mail:                                  #se revisa que el correo ingresado se encuentre en la db
            indice_correo_ingresado = mail.index(correo_ingresado)  # se obtiene el indice
            estado = estado_lista[indice_correo_ingresado]          #esto es para el audi trail

            aleatorio = str(random.randint(1000, 9999))
            print('Codigo enviado al correo')
            print(aleatorio)
            aleatorio_codificado = self.codificar(aleatorio)

            #Correo electrónico que se enviará
            asunto = str("Codigo de seguridad")
            mensaje_enviar = "Para activar su cuenta ingrese usuario y contrasena en la pestana login y presione ingresar, seguido a eso ingrese su codigo de activacion\n" \
                             "Su codigo de activacion es {}".format(aleatorio)  # no se permiten tildes o dará error
            correos.mail(asunto, mensaje_enviar, correo_ingresado)

            #Se actualiza el código en la db
            sql4 = "UPDATE users SET codes='{}' WHERE correo='{}'".format(aleatorio_codificado,self.correo_ingresado.get())
            self.db.borrar(sql4)
            #Mensaje aparece
            messagebox.showinfo('Exito','Se te enviará una clave de validación al correo')

            self.abrir_cambiar_pasw(correo_ingresado)
            self.restaurar.destroy()
                #AUDI TRAIL
            if estado=='Bloqueado':
                evento8 = 'Se ha enviado un codigo de desbloqueo a {}'.format(correo_ingresado)
                self.audit_trail1(evento8)
            elif estado=='Activo':
                evento9 = 'Se ha enviado un codigo de cambio de usuario a {}'.format(correo_ingresado)
                self.audit_trail1(evento9)
            elif estado=='Inactivo':
                evento10 = 'Correo inactivo {} ha solicitado un cambio de contrasena'.format(correo_ingresado)
                self.audit_trail1(evento10)




        else:
            messagebox.showerror('Error', 'El correo ingresado no es valido')



    def abrir_cambiar_pasw(self,correo_vent_anterior):
        self.correoguardado=correo_vent_anterior
        self.cambiar_contraseña=Toplevel()
        self.cambiar_contraseña.title('Cambiar Contraseña')
        # cuadro_contenedor=LabelFrame(self.cambiar_contraseña,text='Cambio de contraseña').grid(row=0,column=0,columnspan=3,pady=20)

        # Contrasena
        Label(self.cambiar_contraseña, text='Nueva contraseña:').grid(row=2, column=0)
        self.nueva_contrasena = Entry(self.cambiar_contraseña,show="*")
        self.nueva_contrasena.grid(row=2, column=1)

        # Repetir contrasena
        Label(self.cambiar_contraseña, text='Repetir contraseña:').grid(row=3, column=0)
        self.repetir_contrasena = Entry(self.cambiar_contraseña,show="*")
        self.repetir_contrasena.grid(row=3, column=1)          #Siempre separar grid, de lo contrario, el get no funciona

        # mail
        Label(self.cambiar_contraseña, text='Ingrese código:').grid(row=1, column=0)
        self.ingrese_codigo = Entry(self.cambiar_contraseña)
        self.ingrese_codigo.grid(row=1, column=1)  # Siempre separar grid, de lo contrario, el get no funciona

        # Boton Aceptar
        ttk.Button(self.cambiar_contraseña, text='Aceptar',command=self.cambiar_pasw).grid(row=4, columnspan=2, sticky=W + E, pady=10)

        #Boton Cancelar
        ttk.Button(self.cambiar_contraseña,text='Atras',command=self.atras_vent_camb_pasw).grid(row=5, columnspan=2, pady=10)
        #El método grab_set() asegura que no haya eventos de raton o teclado que se envíen a otra ventana diferente a la que se está usando
        # Se utiliza para crear una ventana de tipo modal que será necesario cerrar para trabajar con tra diferente, con ello tambien se impide
        #que la misma ventana se abra varias veces

        self.cambiar_contraseña.grab_set()
    def atras_vent_camb_pasw(self):
        self.vent_restaurar_pasw()
        self.cambiar_contraseña.destroy()


    def cambiar_pasw(self):

        pasw = str(self.nueva_contrasena.get())
        pasw_codificado=self.codificar(str(pasw))
        rep_pasw = str(self.repetir_contrasena.get())
        codigo = str(self.ingrese_codigo.get())
        correo=self.correoguardado#str(self.correo_ingresado.get())

        if pasw!="" and rep_pasw !="" and codigo!="":   #si se han ingresado todos los datos
            if len(pasw) < 4:
                messagebox.showwarning('Warning', 'La clave debe ser de mínimo 4 carácteres', )
            else:
                if pasw==rep_pasw:                                #Si las contrasenas son iguales
                    lista_columnas = ['correo', 'codes','usuario']
                    basedatos = 'users'
                    validar_codigo = self.db.query2(basedatos, lista_columnas)  #
                    mail = []
                    codes = []
                    usuario_lista=[]
                    for datos in validar_codigo:
                        mail.append(datos[0])
                        codes.append(datos[1])
                        usuario_lista.append(datos[2])
                    codigo_ingresado_codificado = self.codificar(str(codigo))

                    # print(codigo_ingresado_codificado)
                    # print(codes)
                    if codigo_ingresado_codificado in codes:                    #Si el codigo es valido
                        indice = codes.index(codigo_ingresado_codificado)  # se obtiene el indice
                        usuario=usuario_lista[indice]
                        if mail[indice] == correo:  # solo es para comprobar que el codigo responda al correo dado

                            sql3 = "UPDATE users SET clave='{}',estado='Activo' WHERE correo='{}' ".format(pasw_codificado,correo)  # Se actualiza a activo
                            self.db.borrar(sql3)
                            messagebox.showinfo('Exito', 'Contrasena actualizada correctamente')

                            evento11 = 'Correo {} ha actualizado contrasena correctamente'.format(correo)
                            self.audit_trail1(evento11)

                            sql6 = "DELETE FROM validación WHERE usuario='{}'".format(usuario)
                            self.db.borrar(sql6)
                            limpiar_entry=[self.nueva_contrasena,self.repetir_contrasena,self.ingrese_codigo]
                            self.limpiar_entry(limpiar_entry)
                            self.cambiar_contraseña.destroy()
                            # self.vent_restaurar_pasw.destroy()

                    else:
                        messagebox.showerror('Error','Ingresó un codigo erroneo')
                else:
                    messagebox.showinfo('Warning', 'Contrasenas no coinciden')

        else:
            messagebox.showwarning('Warning','Datos invalidos')





    def codificar(self,cadena):
        hash1=hashlib.sha1()
        hash1.update(cadena.encode("UTF-8"))
        hex1=hash1.hexdigest()
        return hex1









