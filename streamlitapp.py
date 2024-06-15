import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def get_local_time(timezone_offset):
    utc_time = datetime.now(timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %d %B %Y, %I:%M %p")

def get_forecast_data(city, country, state, api_key):
    location_query = f"{city},{country}"
    if state:
        location_query = f"{city},{state},{country}"

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location_query}&appid={api_key}&units=metric"
    res = requests.get(url)
    data = res.json()

    if res.status_code == 200:
        forecast_data = []
        for forecast in data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'], timezone.utc) + timedelta(seconds=data['city']['timezone'])
            temp = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            description = forecast['weather'][0]['description']
            wind = forecast['wind']['speed']
            pressure = forecast['main']['pressure']
            forecast_data.append({
                'Forecast Time': forecast_time.strftime("%A, %d %B %Y, %I:%M %p"),
                'Temperature (°C)': temp,
                'Humidity (%)': humidity,
                'Description': description,
                'Wind Speed (m/s)': wind,
                'Pressure (hPa)': pressure
            })
        return forecast_data
    else:
        return None

def plot_forecast_graph(df):
    # Plotting Temperature and Humidity over Time
    plt.figure(figsize=(10, 6))
    plt.plot(df['Forecast Time'], df['Temperature (°C)'], marker='o', linestyle='-', color='b', label='Temperature (°C)')
    plt.plot(df['Forecast Time'], df['Humidity (%)'], marker='o', linestyle='-', color='g', label='Humidity (%)')
    plt.title('5-Day Weather Forecast')
    plt.xlabel('Forecast Time')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Convert the plot to an image and return
    st.pyplot(plt)

def main():
    st.title("Weather Forecast")
    st.write("Enter the details below to fetch the 5-day weather forecast:")

    city = st.text_input("Enter City:")
    country = st.text_input("Enter Country (use 2-letter ISO code):").upper()
    state = ""

    if country == "US":
        state = st.text_input("Enter State (if applicable):")

    api_key = st.text_input("API key:")

    if st.button("Fetch Forecast"):
        location_query = f"{city},{country}"

        if state:
            location_query = f"{city},{state},{country}"

        # 5-day forecast data
        forecast_data = get_forecast_data(city, country, state, api_key)
        if forecast_data:
            df = pd.DataFrame(forecast_data)
            st.subheader("5-Day Weather Forecast")
            st.dataframe(df)

            # Plot the forecast graph
            plot_forecast_graph(df)
        else:
            st.error("Unable to fetch forecast data.")

if __name__ == "__main__":
    main()