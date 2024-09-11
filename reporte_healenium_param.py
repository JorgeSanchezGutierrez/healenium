# Para envío de correos
gloDestinatarios = ["nelson.colman@testgroup.cl", "jorge.sanchez@testgroup.cl"]
gloClaveApp = "dyuc aaiz mnfd ownt"

# Tipo de envio email 
gloTipoEnvioNoHay = "S"
gloTipoEnvioNoHayMsg = "Envio de correos Si No Hay registros seleccionados: "
gloTipoEnvioNoHayMsg = gloTipoEnvioNoHayMsg + "S=Aunque NO haya registros seleccionados, el correo se envía igual. "
gloTipoEnvioNoHayMsg = gloTipoEnvioNoHayMsg + "N=Si NO hay registros seleccionados, el correo no se envía."

# Filtro de Fecha y Hora
gloMinutosAtrasDesde = 0
gloMinutosAtrasDesdeMsg = "- Minutos atrás Desde para revisar cambios: " + str(gloMinutosAtrasDesde) + " minutos"
gloMinutosAtrasDesdeMsg = gloMinutosAtrasDesdeMsg + " (0: No se filtra por Fecha / Mayor a 0: Minutos Desde)."

# Grupo de Correos, es decir, cada cuantos seleccionados se envía un correos
gloTotalGrupoCorreo = 0
gloTotalGrupoCorreoMsg = "0: Se genera 1 correo con Todos los cambios seleccionados "
gloTotalGrupoCorreoMsg = gloTotalGrupoCorreoMsg + "/ Valor Mayor a 0: Se genera 1 correo para cada grupo indicado."

# Para conexion a la Base de Datos
gloHost = "localhost"  # Ej. "localhost" si está en tu máquina local
gloDatabase = "healenium"
gloUser = "healenium_user"
gloPassword = "YDk2nmNs4s9aCP6K"

# Ruta origen de Docker-compose
gloRutaCompose = "C:/zHealenium/healenium-2.0.0/healenium-2.0.0"
