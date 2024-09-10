# Para envío de correos
gloDestinatarios = ["nelson.colman@testgroup.cl", "jeremy.burgos@testgroup.cl", "reportehealenium@gmail.com",
                    "katherine.andrade@testgroup.cl", "ext-martha.hernandez@sbins.cl"]
gloClaveApp = "eocd vcyg angl vmro"

# Tipo de envio email
gloTipoEnvioNoHay = "S"
gloTipoEnvioNoHayMsg = "Envio de correos Si No Hay registros seleccionados: "
gloTipoEnvioNoHayMsg = gloTipoEnvioNoHayMsg + "S=Aunque NO haya registros seleccionados, el correo se envía igual. "
gloTipoEnvioNoHayMsg = gloTipoEnvioNoHayMsg + "N=Si NO hay registros seleccionados, el correo no se envía."

# Filtro de Fecha y Hora
gloMinutosAtrasDesde = 0  # 24 horas, cambiar por 0 para revisión total 
gloMinutosAtrasDesdeMsg = "- Minutos atrás Desde para revisar cambios: " + str(gloMinutosAtrasDesde) + " minutos"
gloMinutosAtrasDesdeMsg = gloMinutosAtrasDesdeMsg + " (Mayor a 0 = Minutos Desde, 0=No se filtra por Fecha)."

# Para conexion a la Base de Datos
gloHost = "localhost"  # Ej. "localhost" si está en tu máquina local -> IP del servidor
gloDatabase = "healenium"
gloUser = "healenium_user"
gloPassword = "YDk2nmNs4s9aCP6K"
#datos Data base 

# Ruta origen de Docker-compose
gloRutaCompose = "C:/zHealenium/healenium-2.0.0/healenium-2.0.0"
