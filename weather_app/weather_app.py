import tkinter as tk
import requests

# fetch weather data
def fetch_weather():
    city = city_var.get()
    if city:
        api_key = "YOUR_WEATHERSTACK_API_KEY"
        base_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
        response = requests.get(base_url)
        data = response.json()
        if data.get("current"):
            temperature = data["current"]["temperature"]
            description = data["current"]["weather_descriptions"][0]
            weather_info = f"Weather in {city.capitalize()}:\nTemperature: {temperature}°C\nDescription: {description.capitalize()}"
            weather_label.config(text=weather_info)
        else:
            weather_label.config(text="City not found")
    else:
        weather_label.config(text="Enter a city")

# main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x250")

# label for title
title_label = tk.Label(
    root, 
    text="Weather App", 
    font=("Helvetica", 20))
title_label.pack()

# label for city entry
city_label = tk.Label(
    root, 
    text="Enter a city:", 
    font=("Helvetica", 16))
city_label.pack()

# input for city name
city_var = tk.StringVar()
city_entry = tk.Entry(
    root, 
    textvariable=city_var, 
    font=("Helvetica", 16))
city_entry.pack()

# search button to fetch weather data
search_button = tk.Button(
    root, 
    text="Search City", 
    command=fetch_weather, 
    font=("Helvetica", 16))
search_button.pack()

# label to display weather information
weather_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 16))
weather_label.pack()

# main loop
root.mainloop()
