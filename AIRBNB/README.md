# INSTACART Deber1
En el siguiente README se describen los pasos detallados para correr los componentes del proyecto

Cabe recalcar que se deben descargar las dependencias de python para comenzar ```requirements.txt```

    pip install -r requirements.txt

De la misma forma, se utilizan variables de entorno durante todo el proyecto por lo que se necesita configurar las variables de entorno

**Para MySQL:**
MYSQL_HOST: La dirección del host donde está corriendo tu base de datos MySQL.
MYSQL_USER: El nombre de usuario para acceder a la base de datos MySQL.
MYSQL_PASSWORD: La contraseña correspondiente al usuario de MySQL.
MYSQL_PORT: El puerto donde MySQL está escuchando.

**Para Snowflake:**
SNOWFLAKE_USER: El nombre de usuario para conectarte a Snowflake.
SNOWFLAKE_PASSWORD: La contraseña correspondiente al usuario de Snowflake.
SNOWFLAKE_ACCOUNT: El identificador de tu cuenta de Snowflake.
SNOWFLAKE_WAREHOUSE: El nombre del warehouse que usarás para ejecutar las consultas.



## Scripts
Archivos .py utlizados para comprobar o crear.
### transform.py
El script que pasa los datos de csv a MySql. Por lo que se debe tener MySql activado.
**Para Correr:**

    python transform.py

### comprobacion.py
El script se encarga de comprobar si los datos se pasaron correctamente de MySql a SnowFlake.
**Para Correr:**

    python comprobacion.py

### CreateClean.py
El script se utiliza para crear el schema CLEAN en SnowFlake con el formato STAR descrito en /docs
**Para Correr:**

    python CreateClean.py

## NoteBooks
Creados para el análisis de datos
### eda.ipynb
El notebook sirve para analizar el schema RAW de SnowFlake
**Para Correr:** Puedes abrir cualquier editor de ipynb como jupyter notebook o vs code con una extensión. Seguido de eso, ejecutar todas las celdas
### insights.ipynb
El notebook sirve para responder las preguntas y sacar informaciónd el schema CLEAN
**Para Correr:** Puedes abrir cualquier editor de ipynb como jupyter notebook o vs code con una extensión. Seguido de eso, ejecutar todas las celdas

## Mage Ai (Pipelines)
Se crearon dos pipelines. Automatizadas para correr cada mes y así realizar un análisis mensual.
### pipeline_instacartdb
Es la que se encarga de pasar los datos de MySql al schema RAW de SnowFlake. Se creo un Trigger llamado Mensual el cual corre la pipeline automáticamente cada mes
### pipeline_instacartsnowf
Es la que se encarga de pasar los datos del schema RAW al schema CLEAN de SnowFlake. Se creo un Trigger llamado Mensual el cual corre la pipeline automáticamente cada mes.
