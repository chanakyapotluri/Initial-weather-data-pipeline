import requests
import sqlite3

API_URL = "https://api.open-meteo.com/v1/forecast"
DB_NAME = "weather.db"


def fetch_weather_data():
    params = {
        "latitude": 39.7589,
        "longitude": -84.1916,
        "current_weather": True
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    data = response.json()
    return data["current_weather"]


def save_weather_data(weather):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weather_time TEXT,
        temperature REAL,
        windspeed REAL,
        winddirection REAL
    )
    """)

    cursor.execute("""
    INSERT INTO weather_data (
        weather_time,
        temperature,
        windspeed,
        winddirection
    )
    VALUES (?, ?, ?, ?)
    """, (
        weather["time"],
        weather["temperature"],
        weather["windspeed"],
        weather["winddirection"]
    ))

    connection.commit()
    connection.close()


def show_latest_records():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM weather_data
    ORDER BY id DESC
    LIMIT 5
    """)

    rows = cursor.fetchall()

    print("\nLatest 5 records:")
    for row in rows:
        print(row)

    connection.close()


def main():
    try:
        weather = fetch_weather_data()
        save_weather_data(weather)
        print("Weather data saved successfully!")
        show_latest_records()

    except requests.exceptions.RequestException as error:
        print("API request failed:", error)

    except Exception as error:
        print("Something went wrong:", error)


main()