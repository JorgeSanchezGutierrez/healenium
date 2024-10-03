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
print("Espere por favor...")

gloLocalizadores = ""

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()
minutos_a_restar = reporte_healenium_param.gloMinutosAtrasDesde
nueva_fecha_hora = fecha_hora_actual - timedelta(minutes=minutos_a_restar)


# print(f"Fecha y hora actual: {fecha_hora_actual}")
# print(f"Fecha y hora después de restar {minutos_a_restar} minutos: {nueva_fecha_hora}")
# Fecha Hora actual

# AREA DE RUTINAS ****************************************************************************************************#
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

    texto01 = (texto01 + "- Total seleccionados por Grupo correo: " +
               str(reporte_healenium_param.gloTotalGrupoCorreo) + ".<br>")
    texto01 = texto01 + "- Total seleccionados por Grupo correo: "
    texto01 = texto01 + reporte_healenium_param.gloTotalGrupoCorreoMsg + "<br>"

    texto01 = texto01 + "-" * 70 + "<br>"
    texto01 = texto01 + ""

    return texto01


def fecha_hora():
    global xFechaHoraHoy_reporte

    # Fecha y Hora del dia
    fecha_hora_actual1 = datetime.now()
    xDia = str(fecha_hora_actual1.strftime("%d"))
    xMes = str(fecha_hora_actual1.strftime("%m"))
    xAno = str(fecha_hora_actual1.year)
    xHH = str(fecha_hora_actual1.strftime("%H"))
    xMM = str(fecha_hora_actual1.strftime("%M"))
    xSS = str(fecha_hora_actual1.strftime("%S"))
    xFH = xAno + "/" + xMes + "/" + xDia + " " + xHH + ":" + xMM + ":" + xSS + " horas"
    xFechaHoraHoy_reporte = xAno + xMes + xDia + "_" + xHH + xMM + xSS
    return xFH
    # Fin


def procesar_jason(xjson1):
    global granURL
    global granContador
    global granContadorProgress
    global gloLocalizadores

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

        granContador += 1

        buscar = "progressbar"
        if buscar in failed_locator['value']:
           granContadorProgress += 1

        # Para buscar luego los Localizadores repetidos
        gloLocalizadores += f"Failed Locator Value: {failed_locator['value']}" + "<br>"
        # Fin

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
    global contador4
    global contador0_envios
    global xFechaHoraHoy

    # Configura la información del correo
    sender_email = "soporte.ti@testgroup.cl"
    receiver_email = reporte_healenium_param.gloDestinatarios
    password = reporte_healenium_param.gloClaveApp

    # Indica Grupo de Correo
    grupocorreo = ""
    if reporte_healenium_param.gloTotalGrupoCorreo > 0:
        grupocorreo = "[" + str(contador4) + " de " + str(int(contador0_envios)) + "] "

    # Crea el mensaje
    message = MIMEMultipart("alternative")
    message["Subject"] = grupocorreo + "Reporte Healenium " + xFechaHoraHoy
    message["From"] = sender_email
    message["To"] = ', '.join(receiver_email)

    # Cuerpo del correo
    eeuca = "<br><br>Localizadores incluidos en este correo:<br><br>" + gloLocalizadores
    eeuca = eeuca + "<br><br>Este es un correo automatico, no responder por favor.<br><br>"
    eeuca = eeuca + "Soporte Técnico<br>Gerencia de Servicios<br>TestGroup"
    contenido_html1 += eeuca

    # Agregar el contenido en formato HTML al mensaje
    msg_html = MIMEText(contenido_html1, 'html')
    message.attach(msg_html)

    # Agregar las imágenes con el identificador cid correspondiente
    for ii, img_ruta in enumerate(imagenes_rutas1):
        if img_ruta != "***":
            with open(img_ruta, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', f'<imagen{ii}>')  # 'cid' que referencia la imagen en el HTML
                img.add_header('Content-Disposition', 'inline', filename=img_ruta)
                message.attach(img)

    # Envía el correo usando el servidor SMTP de Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Correos enviado con éxito")
            print("-------------------------\n")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def inicia_envio_correos():
    global contenido_html
    global mensajeenvio
    global contador3
    global contador4

    contenido_html += "</body></html>"

    if contador2 == 0:
        if reporte_healenium_param.gloTipoEnvioNoHay == "N":
            mensajeenvio = "No hay registros seleccionados, NO se envía correo."

    if mensajeenvio == "OK":
        if contador2 == 0:
            contenido_html += "*** No hay Cambios realizados por Healenium.<br>"

        texto1a = "-" * 70 + "<br><br>"
        contenido_html += f"<p>{texto1a}</p>"

        contenido_html += f"Total de registros leidos . . . : {contador1}"
        contenido_html += "<br>" + f"Total de registros seleccionados: {contador2}"
        contenido_html += "<br>" + f"Total de cambios realizados . . : {granContador}"
        contenido_html += "<br>" + f"Total de cambios progress . . . : {granContadorProgress}<br><br>"

        contador4 += 1

        grupocorreos = ""
        if reporte_healenium_param.gloTotalGrupoCorreo > 0:
            grupocorreos = " " + str(contador4) + " de " + str(int(contador0_envios))

        print("Espere por favor, enviando correo" + grupocorreos + "...")
        print(reporte_healenium_param.gloDestinatarios)
        contenido_html += parametros()
        enviar_correo(contenido_html, imagenes)
    else:
        print(mensajeenvio)

    contador3 = 0
# FIN AREA DE RUTINAS ************************************************************************************************#


# CUERPO DEL PROGRAMA PYTHON *****************************************************************************************#

# Configuración de la conexión con Healenium
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

totalPorLeer = len(resultados)
print("Se procesaran: " + str(totalPorLeer) + " registros...\n")

# Inicializar variables
granURL = ""
granContador = 0
granContadorProgress = 0

imagenes = []
contenido_html = "<html><body>"

contador0 = 0
contador0_envios = 0

contador1 = 0
contador2 = 0
contador3 = 0
contador4 = 0
mensajeenvio = ""

xFechaHoraHoy_reporte = ""
xFechaHoraHoy = fecha_hora()

# Contar seleccionados en forma previa
if reporte_healenium_param.gloTotalGrupoCorreo > 0:
    print("Obteniendo total de seleccionados en forma previa...\n")
    for fila in resultados:
        create_date, elements, uid = fila

        xseguir1 = "N"

        if elements != '{"records":[]}':
            xseguir1 = "S"

        if xseguir1 == "S":
            if reporte_healenium_param.gloMinutosAtrasDesde > 0:
                if create_date < nueva_fecha_hora:
                    xseguir1 = "N"

        if xseguir1 == "S":
            contador0 += 1

    contador0_envios = contador0 / reporte_healenium_param.gloTotalGrupoCorreo

    resto = contador0 % reporte_healenium_param.gloTotalGrupoCorreo
    if resto > 0:
        contador0_envios = int(contador0_envios)
        contador0_envios += 1
# Fin Contar seleccionados

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
        contador3 += 1
        if contador3 == 1:
            imagenes = []
            contenido_html = "<html><body>"
            texto = "Reporte de cambios en la ejecución de automatizaciones.<br><br>"
            contenido_html += texto
            texto = "-" * 70 + "<br>"
            contenido_html += texto
            mensajeenvio = "OK"

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
        i = contador3 - 1
        if i < len(imagenes):  # Asegura que no exceda la cantidad de imágenes
            contenido_html += f'<br><img src="cid:imagen{i}" alt="*********************************************"><br>'
    if reporte_healenium_param.gloTotalGrupoCorreo > 0:
        if contador3 == reporte_healenium_param.gloTotalGrupoCorreo:
            inicia_envio_correos()

if contador3 > 0:
    inicia_envio_correos()

print(f"Total de registros leidos . . . : {contador1}")
print(f"Total de registros seleccionados: {contador2}")
print(f"Total de cambios realizados . . : {granContador}")
print(f"Total de cambios progress . . . : {granContadorProgress}")

# FIN

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
