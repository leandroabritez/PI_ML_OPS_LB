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

