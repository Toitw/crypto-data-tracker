import requests
import pandas as pd
import time
from datetime import datetime

# Función para obtener el Crypto Fear and Greed Index
def get_fear_and_greed_index():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url)
    data = response.json()
    return data["data"][0]

# Función para obtener los precios de los criptoactivos desde CoinGecko
def get_crypto_prices(cryptos):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(cryptos),
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    return response.json()

# Lista de criptoactivos a rastrear
cryptos = ["bitcoin", "ethereum", "cardano", "solana", "ripple"]

# Archivo donde se almacenarán los datos
file_name = "crypto_data.csv"

# Función para recopilar y guardar los datos
def collect_and_save_data():
    # Obtener datos
    fear_and_greed = get_fear_and_greed_index()
    prices = get_crypto_prices(cryptos)
    timestamp = datetime.now().isoformat()

    # Crear un diccionario con los datos
    data = {
        'timestamp': timestamp,
        'fear_and_greed_index': fear_and_greed['value'],
        'fear_and_greed_classification': fear_and_greed['value_classification']
    }
    for crypto in cryptos:
        data[f'{crypto}_price'] = prices[crypto]['usd']

    # Crear un DataFrame a partir del diccionario
    df = pd.DataFrame([data])

    # Guardar los datos en el archivo CSV
    try:
        existing_df = pd.read_csv(file_name)
        if not existing_df.empty and existing_df.iloc[-1]['timestamp'] == timestamp:
            # Si ya existe una fila con el mismo timestamp, no hacer nada
            print("Datos ya almacenados para este timestamp.")
            return
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        # El archivo no existe, se crea uno nuevo
        pass

    # Guardar los datos actualizados en el archivo CSV
    df.to_csv(file_name, index=False)

    # Imprimir un mensaje de éxito
    print(f"Datos almacenados correctamente a las {timestamp}")

# Función principal
def main():
    # Ejecutar la recolección y guardado de datos una vez al inicio
    collect_and_save_data()

if __name__ == "__main__":
    main()
