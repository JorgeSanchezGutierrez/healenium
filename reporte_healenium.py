import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import json
import datetime
from datetime import datetime, timedelta

import reporte_healenium_param

print("")
print("Espere por favor, procesando...")

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()
minutos_a_restar = reporte_healenium_param.gloMinutosAtrasDesde
nueva_fecha_hora = fecha_hora_actual - timedelta(minutes=minutos_a_restar)


# print(f"Fecha y hora actual: {fecha_hora_actual}")
# print(f"Fecha y hora después de restar {minutos_a_restar} minutos: {nueva_fecha_hora}")
# Fecha Hora actual


def parametros():
    texto01 = "\n"

    texto01 = texto01 + "-" * 70 + "<br>"
    texto01 = texto01 + "Parámetros:" + "<br>"
    texto01 = texto01 + "- Envio de correos Si No Hay registros seleccionados: "
    texto01 = texto01 + reporte_healenium_param.gloTipoEnvioNoHay + "<br>"
    texto01 = texto01 + "- " + reporte_healenium_param.gloTipoEnvioNoHayMsg + "<br>"
    texto01 = texto01 + "" + "<br>"
    texto01 = texto01 + reporte_healenium_param.gloMinutosAtrasDesdeMsg + "<br>"
    if reporte_healenium_param.gloMinutosAtrasDesde > 0:
        texto01 = texto01 + "- Fecha Hora Desde Filtro: " + str(nueva_fecha_hora) + " horas.<br>"
    texto01 = texto01 + "-" * 70 + "<br>"
    texto01 = texto01 + ""

    return texto01


def fecha_hora():
    # Fecha y Hora del dia
    fecha_hora_actual1 = datetime.now()
    xDia = str(fecha_hora_actual1.strftime("%d"))
    xMes = str(fecha_hora_actual1.strftime("%m"))
    xAno = str(fecha_hora_actual1.year)
    xHH = str(fecha_hora_actual1.strftime("%H"))
    xMM = str(fecha_hora_actual1.strftime("%M"))
    xSS = str(fecha_hora_actual1.strftime("%S"))
    xFH = xAno + "/" + xMes + "/" + xDia + " " + xHH + ":" + xMM + ":" + xSS + " horas"
    return xFH
    # Fin


granURL = ""
granContador = 0
granContadorProgress = 0
def procesar_jason(xjson1):
    global granURL
    global granContador
    global granContadorProgress
    xsalida = ""

    # JSON proporcionado
    json_data = xjson1

    # Convertir la cadena JSON en un diccionario de Python
    data = json.loads(json_data)

    # Iterar a través de todos los registros
    for i, record in enumerate(data['records']):
        class_name = record['className']
        method_name = record['methodName']
        failed_locator = record['failedLocator']
        healed_locator = record['healedLocator']
        screenshot_path = reporte_healenium_param.gloRutaCompose + record['screenShotPath']
        healing_result_id = record['healingResultId']

        # Imprimir la información de cada registro
        xsalida = xsalida + "\n"
        if i > 0:
            xsalida = xsalida + "\n"
	
        granContador = granContador + 1

        buscar = "progressbar"

        if buscar in failed_locator['value']:
           granContadorProgress += 1

        xsalida = xsalida + f"      <br><br>Cambio #{i + 1}:" + "<br>"
        xsalida = xsalida + f"      - Healing Result ID: {healing_result_id}" + "<br>"
        xsalida = xsalida + f"      - Class Name: {class_name}" + "<br>"
        xsalida = xsalida + f"      - Method Name: {method_name}" + "<br>"
        xsalida = xsalida + f"      - Failed Locator Value: {failed_locator['value']}" + "<br>"
        xsalida = xsalida + f"      - Failed Locator Type: {failed_locator['type']}" + "<br>"
        xsalida = xsalida + f"      - Healed Locator Value: {healed_locator['value']}" + "<br>"
        xsalida = xsalida + f"      - Healed Locator Type: {healed_locator['type']}" + "<br>"
        file_path = screenshot_path
        granURL = screenshot_path
        url = f"file:///{file_path.replace(' ', '%20')}"  # Formato de URL para la ruta de archivo
        xsalida = xsalida + f"      - Path de la imagen con cambios (Ver elemento con marco en ROJO):<br>      {url}"
	
    return xsalida


def enviar_correo(contenido_html1, imagenes_rutas1):
    # Configura la información del correo
    sender_email = "reportehealenium@gmail.com"
    receiver_email = reporte_healenium_param.gloDestinatarios
    password = reporte_healenium_param.gloClaveApp

    # Crea el mensaje
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reporte Healenium " + fecha_hora()
    message["From"] = sender_email
    message["To"] = ', '.join(receiver_email)

    # Cuerpo del correo
    eeuca = "<br><br>Este es un correo automatico, no responder por favor.<br><br>"
    eeuca = eeuca + "Soporte Técnico<br>Gerencia de Servicios<br>TestGroup"
    contenido_html1 += eeuca

    # Agregar el contenido en formato HTML al mensaje
    msg_html = MIMEText(contenido_html1, 'html')
    message.attach(msg_html)

    # Agregar las imágenes con el identificador cid correspondiente
   # for i, img_ruta in enumerate(imagenes_rutas1):
   #     if img_ruta != "***":
   #         with open(img_ruta, 'rb') as img_file:
   #             img = MIMEImage(img_file.read())
   #             img.add_header('Content-ID', f'<imagen{i}>')  # 'cid' que referencia la imagen en el HTML
   #             img.add_header('Content-Disposition', 'inline', filename=img_ruta)
   #             message.attach(img)

    # Envía el correo usando el servidor SMTP de Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Correos enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


# Configuración de la conexión
conexion = psycopg2.connect(
    host=reporte_healenium_param.gloHost,
    database=reporte_healenium_param.gloDatabase,
    user=reporte_healenium_param.gloUser,
    password=reporte_healenium_param.gloPassword
)

# Crear un cursor
cursor = conexion.cursor()

# Ejecutar una consulta SQL
cursor.execute("SELECT create_date, elements, uid FROM healenium.report;")

# Obtener los resultados
resultados = cursor.fetchall()

# Inicializar variables
imagenes = []
contenido_html = "<html><body>"

contador1 = 0
contador2 = 0
texto = "Reporte de cambios en la ejecución de automatizaciones.<br><br>"
contenido_html += texto
texto = "-" * 70 + "<br>"
contenido_html += texto
mensajeenvio = "OK"

# Generar contenido del correo
for fila in resultados:
    create_date, elements, uid = fila
    contador1 += 1

    texto1 = ""
    xseguir = "N"

    if elements != '{"records":[]}':
        xseguir = "S"

    if xseguir == "S":
        if reporte_healenium_param.gloMinutosAtrasDesde > 0:
            if create_date < nueva_fecha_hora:
                xseguir = "N"

    if xseguir == "S":
        contador2 += 1

        texto1 = texto1 + f"Registro seleccionado #{contador2}" + "<br>"
        texto1 = texto1 + f"   Fecha de creación: {create_date}" + "<br><br>"

        if elements == '{"records":[]}':
            texto1 = texto1 + f"   Sin cambios." + "<br>"
            imagenes.append("***")
        else:
            texto1 = texto1 + f"   Healenium realizó los siguientes cambios:" + "<br>"
            texto1 = texto1 + procesar_jason(elements) + "<br><br>"
            imagenes.append(granURL)

        contenido_html += f"<p>{texto1}</p>"
        # Agregar la imagen justo debajo del texto
       # i = contador2 - 1
       # if i < len(imagenes):  # Asegura que no exceda la cantidad de imágenes
       #     contenido_html += f'<br><img src="cid:imagen{i}" alt="*********************************************"><br>'

contenido_html += "</body></html>"

if contador2 == 0:
    if reporte_healenium_param.gloTipoEnvioNoHay == "N":
        mensajeenvio = "No hay registros seleccionados, NO se envía correo."

if mensajeenvio == "OK":
    if contador2 == 0:
        contenido_html += "*** No hay Cambios realizados por Healenium.<br>"

    texto1 = "-" * 70 + "<br><br>"
    contenido_html += f"<p>{texto1}</p>"

    contenido_html += f"Total de registros leidos . . . : {contador1}"
    contenido_html += "<br>" + f"Total de registros seleccionados: {contador2}<br><br>"

    print("")
    print("Espere por favor, enviando correos...")
    print(reporte_healenium_param.gloDestinatarios)
    # print("Enviando correo a: " + reporte_healenium_param.gloDestinatarios)
    contenido_html += parametros()
    enviar_correo(contenido_html, imagenes)
else:
    print(mensajeenvio)

print("")
print(f"Total de registros leidos . . . : {contador1}")
print(f"Total de registros seleccionados: {contador2}")
print(f"Total de cambios realizados: {granContador}")
print(f"Total de cambios progress: {granContadorProgress}")

# FIN

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
