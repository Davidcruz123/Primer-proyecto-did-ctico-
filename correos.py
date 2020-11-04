import smtplib


def mail(asunto,mensaje,correo):
    message = mensaje
    subject = asunto
    message = 'Subject:{}\n\n{}'.format(subject, message)  # ojo, el subject debe ir escrito así, sino no lo identifica
    server = smtplib.SMTP('smtp.gmail.com',
                          587)  # Definir objeto smtp...primero se define el servidor de correo.. luego el puerto a usar
    server.starttls()  # Le decimos al programa que vamos a usar el protocolo tls
    server.login('correo@servidor.com', 'xxxxxxx') # server.login(correo-contrasena)
    #NO SE MUESTRAN EL CORREO O LA CONTRASENA POR SEGURIDAD

    server.sendmail("daviducr.2593@gmail.com", correo,message)  # Quien envia el correo,quien lo recibe,mensaje


    server.quit()
