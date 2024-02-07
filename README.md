# PI_ML_OPS_LB
Repositorio de Proyecto Individual 01 para Henry

Ciclo completo de proyecto de Machine Learning 

## Empresa: STEAM
Plataforma multinacional de videojuegos. 

## Objetivo 
Crear un sistema de recomendación de videojuegos para usuarios.

## Extracción de datos 

La base de datos se puede descargar del siguiente [enlace](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj), donde se encuentran 3 archivos comprimidos con WinRar, que alojan a archivos en formato JSON cada uno. 
 
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

Estos pasos forman parte del proceso necesarios para preparar los datos antes de desarrollar cada uno de los endpoints solicitados. 

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

## Recomendación de Juegos

El endpoint `recomendacion_juego` recomienda una lista de juegos similares dado el ID de un juego de entrada. Utiliza un modelo de aprendizaje automático basado en similitud del coseno.

#### Pasos Relevantes:

1. **Preprocesamiento de Datos:**
   - Se carga el archivo `steam_games.csv` que contiene información sobre los juegos en Steam.
   - Se seleccionan las columnas relevantes para el modelo, como el título del juego, el ID, el desarrollador, el precio y las etiquetas.
   - Se eliminan registros con valores nulos en columnas importantes para el análisis, como el título, el ID, el desarrollador y el precio, ya que estos campos son fundamentales para identificar y comparar los juegos.
   - Se eliminan las columnas no necesarias para el sistema de recomendación, como el género, las especificaciones y el año de lanzamiento, ya que estas características no son utilizadas en el cálculo de similitud del coseno. Además, se decidió descartar la columna de género en favor de la columna de etiquetas, ya que esta última incluye información más detallada y relevante sobre los juegos.

2. **Entrenamiento del Modelo:**
   - Se binarizan las etiquetas de las características de los juegos utilizando `MultiLabelBinarizer` de Scikit-learn, lo que convierte las etiquetas de texto en variables binarias utilizables para el análisis.
   - Se calcula la similitud del coseno entre los juegos utilizando la matriz de características binarizadas. El coseno de la similitud mide la similitud entre dos vectores en un espacio multidimensional y se utiliza comúnmente en sistemas de recomendación para encontrar la similitud entre elementos.
   - Se implementa una función para recomendar juegos similares basados en la entrada del usuario.

#### Decisión sobre Similitud del Coseno:

La similitud coseno es una medida de la similitud existente entre dos vectores en un espacio que posee un producto interior con el que se evalúa el valor del coseno del ángulo comprendido entre ellos. Esta función trigonométrica proporciona un valor igual a 1 si el ángulo comprendido es cero, es decir si ambos vectores apuntan a un mismo lugar. Cualquier ángulo existente entre los vectores, el coseno arrojaría un valor inferior a uno. Si los vectores fuesen ortogonales el coseno se anularía, y si apuntasen en sentido contrario su valor sería -1. De esta forma, el valor de esta métrica se encuentra entre -1 y 1, es decir en el intervalo cerrado [-1,1].

La similitud del coseno se eligió como medida de similitud porque es eficaz para encontrar la similitud entre vectores de alta dimensionalidad, como en nuestro caso, donde cada juego está representado por múltiples etiquetas binarias. Además, el coseno de la similitud es independiente de la magnitud de los vectores, lo que significa que solo se tiene en cuenta la dirección de los vectores, no su escala.

#### Selección de Columnas y Eliminación de Otras:

Se seleccionaron las columnas relevantes como el título del juego, el ID, el desarrollador, el precio y las etiquetas porque contienen información crucial para determinar la similitud entre los juegos. Se decidió descartar la columna de género en favor de la columna de etiquetas, ya que esta última incluye información más detallada y relevante sobre los juegos, proporcionando una representación más completa de las características de cada juego.


# Desarrollo de API con FastAPI y Render

Este repositorio contiene el código para una API desarrollada con FastAPI y desplegada en Render. La API proporciona varios endpoints para interactuar con datos relacionados con juegos de la plataforma Steam.

## Uso de FastAPI y Pruebas Locales

FastAPI es un marco web moderno y rápido para crear APIs con Python. Se utiliza para desarrollar aplicaciones web de alto rendimiento con Python de forma sencilla y rápida. Se eligió FastAPI para desarrollar los endpoints debido a su facilidad de uso, su excelente rendimiento y su integración con bibliotecas populares de Python.

Antes de implementar los endpoints en Render, se realizaron pruebas locales utilizando FastAPI. Esto permitió verificar el funcionamiento correcto de los endpoints y resolver cualquier problema antes de desplegar la aplicación en producción.

## Uso de Entornos Virtuales (venv) y Requerimientos

Se utilizó un entorno virtual (`venv`) para gestionar las dependencias del proyecto de manera aislada del sistema operativo. Esto garantiza que las bibliotecas y versiones utilizadas en el proyecto no entren en conflicto con otras aplicaciones o proyectos de Python en el mismo sistema.

Se mantuvo un archivo de requerimientos (`requirements.txt`) que enumeraba todas las bibliotecas y versiones necesarias para ejecutar la aplicación. Esto facilitó la instalación de las dependencias en el entorno virtual y aseguró que todas las bibliotecas requeridas estuvieran disponibles para el desarrollo y la ejecución de la aplicación.

## Pruebas con FastAPI y Despliegue en Render

Cada endpoint desarrollado se probó inicialmente utilizando FastAPI en el entorno local. Esto implicaba ejecutar la aplicación en el servidor local y enviar solicitudes HTTP a los endpoints para verificar su funcionamiento y validar los resultados esperados.

Una vez que los endpoints fueron probados con éxito en FastAPI, se procedió a desplegar la aplicación en Render para su uso en producción. Render es una plataforma en la nube que facilita el despliegue de aplicaciones web y APIs. Al utilizar Render, se pudo escalar la aplicación de forma fácil y eficiente para manejar cargas de trabajo variables y picos de tráfico.

## Configuración de Render y Utilización de GitHub

Para desplegar la aplicación en Render, se configuró un nuevo servicio en la plataforma y se proporcionó el repositorio de GitHub donde se alojaba el código fuente de la aplicación. Render se integró con GitHub para permitir despliegues automáticos cada vez que se realizaban cambios en el repositorio.

Para optimizar el despliegue en Render y reducir el tamaño de los archivos desplegados, se utilizó un archivo `.gitignore` para excluir archivos y directorios no necesarios para la ejecución de la aplicación en producción. De esta manera, se aseguró que solo los archivos necesarios para la ejecución de la aplicación estuvieran presentes en el servidor Render, lo que mejoró la eficiencia y la seguridad del despliegue.

Esta estrategia de desarrollo y despliegue permitió garantizar el buen funcionamiento de los endpoints tanto en el entorno de desarrollo como en producción, ofreciendo una experiencia de usuario consistente y confiable.

# Documentación

Para más información se proporcionan links de la documentación oficial y los enlaces de acceso al repositorio, como así también al deploy de render donde se pueden acceder a los endpoints desarrollados. 

https://docs.render.com/

https://fastapi.tiangolo.com/

https://github.com/leandroabritez/PI_ML_OPS_LB/tree/main

https://pi-ml-ops-lb.onrender.com/docs#