# Dockerización de aplicaciones

El objetivo de esta esta aplicación es medir la felicidad en twitter, utilizar EMR de Amazon y guardar los resultados en una BBDD MongoDB. Todo esto será empaquetado en contenedores y podrá ser ejecutado utilizando Docker Compose.

## Contenedores

Se utilizaran dos contenedores, ambos creados a partir de imagenes las cuales estan disponibles para su descarga en el repositorio de oficial de Docker (https://hub.docker.com/).

### Mongo

Este contenedor hace de base de datos de la aplicación. Se basa en la imagen oficial de MongoDB sin ninguna modificación.

### Tweetsanalysis

Esta imagen ha sido creada para esta aplicación. En el encargador de ejecutar el código que descarga y analiza los tweests. Se basa en el código creado para la práctica de la asignatura de Sistemas-Distribuidos-de-Procesamiento-de-Datos-I. Sobre este código, se han realizado pequeñas modificaciones para adaptarlo a los requerimientos.

Este contenedor acepta las siguientes variables de entorno:

 * ACCESS_TOKEN_KEY: acces_token_key de la API de Twitter (obligatorio)
 * ACCESS_TOKEN_SECRET: access_token_secret  de la API de Twitter (obligatorio)
 * CONSUMER_KEY: consumer_key de la API de Twitter (obligatorio)
 * CONSUMER_SECRET: consumer_secret de la API de Twitter (obligatorio)
 * MAX_TWEETS: Número máximo de tweets a recolectar (valor por defecto = 100)
 * LOCATION_FILTER: Filtro por geolocalización. Debe tener el formato que indica la API de Twitter para este filtro (por defecto = "")
 * DOWNLOAD_TIME: Tiempo máximo que estará ejecutando la descarga de tweets en segundos (valor por defecto = 60)

 * AWS_ACCESS_KEY_ID: access_key_id utilizado para acceder a la cuanta de AWS donde se ejecutará el procesamiento. (obligatorio)
 * AWS_SECRET_ACCESS_KEY: access_secret_key de la cuenta de AWS anterior (obligatorio)

 * MONGODB_HOST: Host donde se ejecuta el servicio de base de datos donde queremos guardar los resultados (por defecto = "mongo")
 * MONGODB_PORT: Puerto en el que escucha el servicio de base de datos (por defecto = 27017)
 * MONGODB_DB: Nombre de la base de datos donde se guardarán los resultados (por defecto = "tweets_feelings")
