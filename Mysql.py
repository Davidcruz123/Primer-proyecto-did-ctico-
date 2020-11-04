import mysql.connector

class claseDatabase:
    def __init__(self):
        self.db=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='david',
            database='db_python')
        self.cursor=self.db.cursor()
        print('Conexión exitosa')

    def query(self):
        sql="SELECT usuario,clave,correo,estado FROM users"

        try:
            self.cursor.execute(sql)
            resultado_user=self.cursor.fetchall()

            return (resultado_user)

            self.db.close()

        except Exception as e:
            print('valor no existe')
            raise

    def query2(self, db, columnas_de_db):

        cadena=self.lista_a_string(columnas_de_db)
        sql="SELECT "+cadena+" FROM "+db


        try:
            self.cursor.execute(sql)
            resultado_user=self.cursor.fetchall()

            return (resultado_user)

            self.db.close()

        except Exception as e:
            print('valor no existe... error')
            raise

    def actualizar(self,id,user,clave):

        sql="UPDATE users SET usuario='{}', clave='{}' WHERE user_id={}".format(user,clave,id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
        except Exception as e:
            raise



    def close(self):
        self.db.close()


    def insert_data(self,user,clave,correo):
        sql="INSERT INTO users(usuario,clave,correo) VALUES(%s,%s,%s)"
        usuario = (user, clave,correo)
        try:
            self.cursor.execute(sql,usuario)
            self.db.commit()
            self.db.close
        except Exception as e:
            raise


    def insert_data2(self,db,columnas,values):
        into=self.lista_a_string(columnas)
        valores=self.lista_a_string2(values)

        sql='INSERT INTO {} ({}) VALUES({})'.format(db,into,valores)

        try:

            self.cursor.execute(sql)
            self.db.commit()
            self.db.close
        except Exception as e:
            raise
    def lista_a_string(self,listaa):
        lista = listaa
        cadena = ""
        for x in lista:
            cadena = cadena + str(x) + ','             #Con esto convertimos la coma en separador
        cadena = cadena[:len(cadena) - 1]              #Se elimina la última coma
        return cadena


    def lista_a_string2(self,listaa):
        lista = listaa
        cadena = ""
        for x in lista:
            cadena = cadena +"'"+ str(x)+"'" + ','
        cadena = cadena[:len(cadena) - 1]
        return cadena


    def borrar(self,sql):

        try:

            self.cursor.execute(sql)
            self.db.commit()
            self.db.close
        except Exception as e:
            raise







