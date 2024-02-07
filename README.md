# PI_ML_OPS_LB
Repositorio de Proyecto Individual 01 para Henry

Ciclo completo de proyecto de Machine Learning 

## Empresa: STEAM
Plataforma multinacional de videojuegos. 

## Objetivo 
Crear un sistema de recomendación de videojuegos para usuarios.

## Extracción de datos 

La base de datos se puede descargar del siguiente [enlace](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj), donde se encuentran 3 archivos comprimidos con WinRar, que alojan a archivos en formato JSON cada uno. 

Donde se encuentran 3 archivos comprimidos con WinRar, que alojan a archivos en formato JSON cada uno. 
- user_items.json.gz
- user_reviews.json.gz
- steam_games.json.gz

Se descomprimen los archivos manualmente.

Se usan diferentes métodos para leer los .JSON en cada caso, dado que algunos archivos no tienen las separaciones estándar con doble comilla '', por lo tanto, se debe utilizar una lectura literal con el módulo `ast` para poder leer el archivo.

## ETL (Extracción, Transformación y Carga) y EDA (Análisis Exploratorio de Datos) de steam_games

### Extracción de Datos

El archivo `ETL_EDA_steam_games.ipynb` realiza las siguientes tareas:

1. **Extracción de Datos:** 
   - Lee un archivo JSON línea por línea.
   - Utiliza `json.loads` para cargar cada línea como un objeto JSON.
   - Almacena los objetos JSON en una lista.
   - Convierte la lista de objetos JSON a un DataFrame de Pandas para su mejor manipulación.

2. **Limpieza de Datos:**
   - Elimina filas con valores nulos en todas las columnas.
   - Elimina columnas que no serán necesarias para los futuros endpoints.
   - Elimina filas con valores nulos en columnas específicas.
   - Reemplaza valores específicos en la columna 'price' por 0.
   - Convierte la columna 'price' a tipo numérico.
   - Reemplaza los valores NaN por 0 solo en la columna 'price'.
   - Verifica y maneja duplicados en la columna 'title'.
   - Convierte la columna 'release_date' a formato de fecha y extrae el año.
   - Guarda el DataFrame modificado en un archivo CSV.

3. **Exploración de Datos (EDA):**
   - Muestra las primeras filas del DataFrame para verificar la lectura.
   - Muestra un resumen estadístico del DataFrame.
   - Calcula tablas de frecuencia para variables categóricas.
   - Realiza un análisis de valores perdidos para identificar posibles datos faltantes.

Estos pasos forman parte del proceso de ETL (Extracción, Transformación y Carga) y EDA (Análisis Exploratorio de Datos) necesarios para preparar los datos antes de aplicar algoritmos de aprendizaje automático. Los scripts proporcionan una base sólida para el preprocesamiento de datos en el proyecto de recomendación de juegos de Steam.

## ETL (Extracción, Transformación y Carga) y EDA (Análisis Exploratorio de Datos) de user_reviews

### Extracción de Datos

El archivo `ETL_EDA_user_reviews.ipynb` realiza las siguientes tareas:

1. **Extracción de Datos:** 
   - Lee un archivo JSON línea por línea utilizando el módulo `ast` para leer el archivo JSON con el formato adecuado.
   - Convierte la lista de objetos JSON a un DataFrame de Pandas para su mejor manipulación.

2. **Limpieza de Datos:**
   - Elimina filas con valores nulos en todas las columnas.
   - Aplica el análisis de sentimiento a los comentarios de los usuarios y agrega el resultado al DataFrame.

3. **Análisis de Sentimiento:**
   - Utiliza la librería `TextBlob` para analizar el sentimiento de los comentarios de los usuarios.
   - Define una función `analyze_sentiment` para clasificar el sentimiento como positivo, negativo o neutral.
   - Aplica la función `analyze_sentiments_for_reviews` a cada fila del DataFrame para analizar el sentimiento de los comentarios de los usuarios.
   - Calcula y muestra la frecuencia de los diferentes sentimientos.

Estos pasos forman parte del proceso de ETL (Extracción, Transformación y Carga) y EDA (Análisis Exploratorio de Datos) necesarios para preparar los datos de los usuarios antes de aplicar algoritmos de aprendizaje automático en el proyecto de recomendación de juegos de Steam.

## ETL (Extracción, Transformación y Carga) y EDA (Análisis Exploratorio de Datos) de user_items

### Extracción de Datos

El archivo `ETL_EDA_user_items.ipynb` realiza las siguientes tareas:

1. **Extracción de Datos:** 
   - Lee un archivo JSON línea por línea utilizando el módulo `ast` para leer el archivo JSON con el formato adecuado.
   - Convierte la lista de objetos JSON a un DataFrame de Pandas para su mejor manipulación.

2. **Limpieza de Datos:**
   - Elimina filas con valores nulos en todas las columnas.
   - Elimina columnas no necesarias como 'items_count', 'steam_id' y 'user_url'.
   - Elimina las claves innecesarias dentro de los diccionarios de la columna 'items' utilizando la función `remove_keys`.
   - Crea una nueva columna llamada 'items_cleaned' que contiene los diccionarios de la columna 'items' sin las claves 'item_name' y 'playtime_2weeks'.
   - Elimina la columna original 'items' después de la limpieza.

Estos pasos forman parte del proceso de ETL (Extracción, Transformación y Carga) y EDA (Análisis Exploratorio de Datos) necesarios para preparar los datos de los ítems de usuario antes de aplicar algoritmos de aprendizaje automático en el proyecto de recomendación de juegos.


## Endpoints

Se han creado archivos independientes para cada endpoint, incluyendo los archivos .csv que se requieren para leer en cada caso y los scripts de prueba para verificar el funcionamiento adecuado de cada uno. Una vez verificado, se estructuran todos los endpoints dentro del archivo `main.py`, que utiliza FastAPI y render para exponer cada una de las funciones.


### Developer

El endpoint `developer` realiza el análisis de la cantidad de items y el porcentaje de contenido gratuito por año según la empresa desarrolladora.

#### Pasos Relevantes:
1. **Carga de Datos:** Se carga el archivo `steam_games.csv` que contiene información sobre los juegos en Steam.
2. **Filtrado por Desarrollador:** Se filtran los datos para seleccionar solo aquellos juegos desarrollados por la empresa especificada.
3. **Agrupación por Año:** Se agrupan los datos por año de lanzamiento.
4. **Cálculo del Contenido Gratuito:** Se calcula el porcentaje de contenido gratuito para cada año considerando el precio de los juegos.
5. **Resultados:** Se devuelve un DataFrame con los años, la cantidad de items y el porcentaje de contenido gratuito para cada año.

### Userdata

El endpoint `userdata` devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y la cantidad de items.

#### Pasos Relevantes:
1. **Carga de Datos:** Se cargan los archivos `user_items.csv` y `user_reviews.csv`, que contienen información sobre las compras de usuarios y las reviews respectivamente.
2. **Filtrado por Usuario:** Se filtran los datos para seleccionar solo aquellos correspondientes al usuario especificado.
3. **Cálculo del Dinero Gastado:** Se suma el precio de todas las compras realizadas por el usuario.
4. **Cálculo del Porcentaje de Recomendación:** Se analizan las reviews del usuario para determinar el porcentaje de recomendación.
5. **Conteo de Items:** Se cuenta la cantidad de items comprados por el usuario.
6. **Resultados:** Se devuelve un diccionario con la información del usuario, incluyendo el dinero gastado, el porcentaje de recomendación y la cantidad de items.

### UserForGenre

El endpoint `UserForGenre` devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

#### Pasos Relevantes:
1. **Carga de Datos:** Se carga el archivo `steam_games.csv` para obtener información sobre los juegos y `user_items.csv` para obtener información sobre las horas jugadas por usuario.
2. **Filtrado por Género:** Se filtran los datos para seleccionar solo aquellos juegos del género especificado.
3. **Agrupación por Usuario:** Se agrupan los datos por usuario para calcular las horas jugadas totales.
4. **Selección del Usuario con Más Horas Jugadas:** Se identifica el usuario que acumula más horas jugadas para el género especificado.
5. **Agrupación de Horas Jugadas por Año:** Se agrupan las horas jugadas por año de lanzamiento de los juegos del género especificado para el usuario seleccionado.
6. **Resultados:** Se devuelve un diccionario con el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.


