from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Definir la función PlayTimeGenre
@app.get("/play_time_genre/{genero}")
def PlayTimeGenre(genero: str):
    # Cargar el DataFrame resultante del proceso anterior
    result_grouped = pd.read_csv('PlayTimeGenre.csv')

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

    data = pd.read_csv('../PI_ML_OPS_data util/steam_games.csv')

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

    return print(result_df)

