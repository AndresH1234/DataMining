# AIRBNB
En el siguiente README se describen los pasos detallados para correr los componentes del proyecto

Cabe recalcar que se deben descargar las dependencias de python para comenzar ```requirements.txt```

    pip install -r requirements.txt

De la misma forma, se utilizan variables de entorno durante todo el proyecto por lo que se necesita configurar las variables de entorno


## Scripts
Archivos .py utlizados para comprobar o crear.
### modelsImplementation.py
Script con las clases de mis implementaciones de los diferentes modelos. Cada uno cuenta con su constructor, fit, predict
**Para Correr:**

    Este Archivo no puede correrse ya que solo implementa los modelos

## NoteBooks
Creados para el análisis de datos, ingeniería de datos y modelado
### 1_exploratory_data_analysis.ipynb
El notebook sirve para analizar los datos raw
**Para Correr:** Puedes abrir cualquier editor de ipynb como jupyter notebook o vs code con una extensión. Seguido de eso, ejecutar todas las celdas
### 2_data_wrangling.ipynb
El notebook sirve para manejar los datos nulos y los outliers encontrados en el EDA. Aquí se crea el archivo processed
**Para Correr:** Puedes abrir cualquier editor de ipynb como jupyter notebook o vs code con una extensión. Seguido de eso, ejecutar todas las celdas
### 3_feature_engineering.ipynb
El notebook sirve para crear nuevas variables y transformar los datos de las variables antiguas. Aquí se crea el archivo de ml
**Para Correr:** Puedes abrir cualquier editor de ipynb como jupyter notebook o vs code con una extensión. Seguido de eso, ejecutar todas las celdas
### 4_model_trainging.ipynb
El notebook sirve para crear los distintos modelos, entrenarlos y evaluarlos. Se da una conclusión al final del archivo con la descripción del mejor modelo. Usa el archivo ml y las clases de modelImplementation.py
**Para Correr:** Puedes abrir cualquier editor de ipynb como jupyter notebook o vs code con una extensión. Seguido de eso, ejecutar todas las celdas

> **Nota:** La conclusión y el mejor modelo se encuentran en 4_model_trainging.ipynb.