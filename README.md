Github User Search
Objetivo
Realizar una app en Django que permita realizar búsquedas de usuarios de Github a través de nombre de usuario (https://api.github.com/users/).
Alcance
La app debe cumplir los siguientes hitos:
Dado un nombre de usuario, quiero realizar la búsqueda en github, recibiendo el perfil del usuario o un mensaje en caso de que no exista.
Cada búsqueda debe ser guardada en la base, con los datos del usuario.
Para cada usuario, se debe guardar la cantidad de veces que se busco.
Quiero ver el historial de búsquedas que se generaron.
Quiero poder buscar las personas guardadas que estén disponibles a contratación (hireable).
Comentarios
Todas las rutas deben estar autenticadas a través de JWT.
Base de datos mysql.
Hacer pruebas de la API desde Postman.
Usar ListAPIView para listar las búsquedas.
