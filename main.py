from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Definir la función PlayTimeGenre
@app.get("/play_time_genre/{genero}")
def PlayTimeGenre(genero: str):
    # Cargar el DataFrame resultante del proceso anterior
    result_grouped = pd.read_csv('def_PlayTimeGenre.csv')

    # Filtrar por el género específico
    genre_data = result_grouped[result_grouped['genres'] == genero]

    if not genre_data.empty:
        # Encontrar el año con más horas jugadas
        max_year_idx = genre_data['sumatoria_horas'].idxmax()
        max_year = genre_data.loc[max_year_idx, 'year']
        max_hours = genre_data.loc[max_year_idx, 'sumatoria_horas']

        # Convertir a tipos nativos
        max_year = int(max_year)
        max_hours = int(max_hours)

        return f"Año de lanzamiento con más horas jugadas para Género '{genero}': {max_year}"
    else:
        raise HTTPException(status_code=404, detail=f"No hay información para el género '{genero}'.")




# Definir la función developer
@app.get("/developer/{developer}")
def developer(developer: str):

    data = pd.read_csv('steam_games.csv')

    # Filtrar por el desarrollador
    developer_data = data[data['developer'] == developer]

    # Crear una lista para almacenar los DataFrames de cada año
    dfs = []

    # Obtener años únicos
    unique_years = developer_data['year'].unique()

    for year in unique_years:
        # Filtrar por año
        year_data = developer_data[developer_data['year'] == year]

        # Contar la cantidad de items
        item_count = len(year_data)

        # Calcular el contenido free
        free_content_percentage = (year_data['price'].fillna(0) == 0).mean() * 100

        # Crear un DataFrame para el año actual solo si hay registros
        if item_count > 0:
            year_df = pd.DataFrame({
                'año': [year],
                'cantidad de items': [item_count],
                'contenido free': [free_content_percentage]
            })

            # Agregar el DataFrame al a lista
            dfs.append(year_df)

    # Verificar si hay DataFrames en la lista antes de concatenar
    if dfs:
        # Concatenar todos los DataFrames en uno solo
        result_df = pd.concat(dfs, ignore_index=True)
    else:
        # Si no hay registros, crear un DataFrame vacío
        result_df = pd.DataFrame(columns=['año', 'cantidad de items', 'contenido free'])

    return result_df.to_json(orient='records')


# Definir la función userdata
@app.get("/userdata/{userdata}")
def userdata(user_id):
    # Leer el archivo ef_userdata.csv
    result_df = pd.read_csv('def_userdata.csv')

    # Filtrar el DataFrame para el usuario específico
    user_data = result_df[result_df['user_id'] == user_id]

    # Verificar si el usuario existe
    if user_data.empty:
        return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

    # Obtener los valores requeridos y convertir de numpy.int64 a tipos nativos de Python
    dinero_gastado = float(user_data['sum_price'].values[0])
    recomendacion_pct = float(user_data['recommend_percentage'].values[0])
    cantidad_items = int(user_data['count_item'].values[0])

    # Formatear el porcentaje de recomendación
    recomendacion_pct_str = f"{recomendacion_pct * 1:.2f}%"

    # Construir el diccionario de resultados
    result_dict = {
        "Usuario X": user_id,
        "Dinero gastado": f"{dinero_gastado:.2f} USD",
        "% de recomendación": recomendacion_pct_str,
        "cantidad de items": cantidad_items
    }

    # Utilizar JSONResponse para manejar la serialización
    return JSONResponse(content=result_dict)


# Definir la función userforgenre
@app.get("/UserForGenre/{UserForGenre}")
def UserForGenre(genero: str):
    # Convertir el género a minúsculas
    genero = genero.lower()

    # Cargar el archivo def_userforgenre.csv
    def_userforgenre = pd.read_csv('def_userforgenre.csv')

    # Filtrar el DataFrame por el género dado
    genre_data = def_userforgenre[def_userforgenre['Genre'].str.lower() == genero]

    if not genre_data.empty:
        # Encontrar el usuario con más horas jugadas
        max_user = genre_data.loc[genre_data['horas_year'].idxmax()]['User_id']

        # Obtener las horas jugadas por año
        horas_por_año = eval(genre_data.loc[genre_data['User_id'] == max_user, 'horas_year'].iloc[0])

        # Construir el resultado final
        resultado = {
            "Usuario con más horas jugadas para Género " + genero.capitalize(): max_user,
            "Horas jugadas": horas_por_año
        }
        return resultado
    else:
        return {"Mensaje": "No se encontraron datos para el género proporcionado."}

# Definir la función recomendacion_juego
@app.get("/recomendacion_juego/{recomendacion_juego}")
def recomendacion_juego(input_id, num_recommendations=5):
    # Cargar el DataFrame
    df = pd.read_csv('def_recommend_games.csv')

    # Llenar valores NaN con 0
    df_filled = df.fillna(0)

    # Encontrar el índice del juego de entrada en el DataFrame
    input_index = df.index[df['id'] == input_id].tolist()[0]

    # Calcular la similitud del coseno entre el juego de entrada y todos los demás juegos
    similarity_scores = cosine_similarity(df_filled.iloc[input_index, 5:].values.reshape(1, -1), df_filled.iloc[:, 5:])

    # Obtener los índices de los juegos más similares
    similar_game_indices = similarity_scores.argsort()[0][-num_recommendations-1:-1][::-1]

    # Obtener los títulos de los juegos más similares
    recommendations = df.iloc[similar_game_indices]['title'].tolist()

    return recommendations
