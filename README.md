# PI_ML_OPS_LB
Repositorio de Proyecto Individual 01 para Henry

Ciclo completo de proyecto de Machine Learning 

## Empresa: STEAM
 Plataforma multinacional de videojuegos. 

## Objetivo 
Crear un sistema de recomendación de videojuegos para usuarios.


## Extracción de datos 

La base de datos se puede descargar del siguiente link: 
https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj

Donde se encuentran 3 archivos comprimidos con WinRar, que alojan a archivos en formato JSON cada uno. 
- user_items.json.gz
- user_reviews.json.gz
- steam_games.json.gz

Se descomprimen los archivos manualmente.

se usan diferentes metodos para leer los .JSON en cada caso, dado que algunos archivos no tienen las seperaciones estandar con doble comilla '', ergo, se debe utilizar una lectura literal con el modulo ast para poder leer el archivo. 

### Analasis primario (EDA)

Se realiza un analisis golbal, mostrando los encabezados de los dataframes para entender mejor su disposición. Se eliminan aquellas filas donde todos los datos sean nulos, se verifica si alguna columna es redudnate para ser eliminada tambien. 




### Extraccones en JSON 

Identificar los diferentes endpoints que me piden, para analizar las columnas necesarias y descartar las que no se usen. Para de esta forma trabajar con archivos más livianos. 
De igual forma, verificar antes de eliminar las columnas, que ninguna de ellas sea de aparente utilidad para los endpoints que son entrenados con machine learning. 