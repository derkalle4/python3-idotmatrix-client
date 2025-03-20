import requests
from PIL import Image, ImageDraw
import numpy

digits = {
    "-": [
        "    ",
        "    ",
        "    ",
        "1111",
        "    ",
        "    ",
        "    "
    ],
    "0": [
        "1111",
        "1  1",
        "1  1",
        "1  1",
        "1  1",
        "1  1",
        "1111"
    ],
    "1": [
        "  1 ",
        " 11 ",
        "  1 ",
        "  1 ",
        "  1 ",
        "  1 ",
        " 111"
    ],
    "2": [
        "1111",
        "1  1",
        "   1",
        "1111",
        "1   ",
        "1   ",
        "1111"
    ],
    "3": [
        "1111",
        "1  1",
        "   1",
        " 111",
        "   1",
        "1  1",
        "1111"
    ],
    "4": [
        "   1",
        "  11",
        " 1 1",
        "1  1",
        "1111",
        "   1",
        "   1"
    ],
    "5": [
        "1111",
        "1   ",
        "1   ",
        "111 ",
        "   1",
        "1  1",
        "1111"
    ],
    "6": [
        "1111",
        "1   ",
        "1   ",
        "1111",
        "1  1",
        "1  1",
        "1111"
    ],
    "7": [
        "1111",
        "1  1",
        "   1",
        "  1 ",
        " 1  ",
        " 1  ",
        " 1  "
    ],
    "8": [
        "1111",
        "1  1",
        "1  1",
        "1111",
        "1  1",
        "1  1",
        "1111"
    ],
    "9": [
        "1111",
        "1  1",
        "1  1",
        "1111",
        "   1",
        "1  1",
        "1111"
    ]
}
colors = {
    "b": "#000000",   # Black
    "y1": "#e5ff00",  # Light yellow
    "y2": "#e6bd09",  # Medium yellow
    "y3": "#e6a307",   # Dark yellow
    "w": "#FFFFFF",   # White 
    "g": "#AAAAAA",   # Dark gray 
    "gD":"#4f4f4f", # gray dark
    "y": "#FFFF00",   # Yellow (thunder)
    "c": "#00FFFF",   # Light blue (rain)
    "bl":"#0088ff", #blue
    
}


patterns = {
    "sun": [
        ["b", "b", "b", "b", "b", "b", "b", "b"],
        ["b", "b", "y1", "y1", "y1", "y3", "b", "b"],
        ["b", "y1", "y1", "y1", "y1", "y2", "y3", "b"],
        ["b", "y1", "y1", "y1", "y1", "y2", "y3", "b"],
        ["b", "y1", "y1", "y1", "y2", "y2", "y3", "b"],
        ["b", "y3", "y2", "y2", "y2", "y3", "y3", "b"],
        ["b", "b", "y3", "y3", "y3", "y3", "b", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "moon": [
        ["b", "b", "b", "b", "b", "b", "b", "b"],
        ["b", "b", "g", "g", "g", "gD", "b", "b"],
        ["b", "g", "gD", "gD", "g", "g", "gD", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "g", "g", "g", "gD", "gD", "g", "b"],
        ["b", "g", "gD", "g", "gD", "gD", "g", "b"],
        ["b", "b", "g", "g", "g", "g", "b", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "cloudy": [
        ["b", "b", "b", "b", "b", "b", "b", "b"],
        ["b", "b", "b", "g", "g", "g", "b", "b"],
        ["b", "g", "g", "w", "w", "w", "g", "b"],
        ["b", "g", "w", "w", "w", "w", "g", "b"],
        ["g", "w", "w", "w", "g", "g", "w", "g"],
        ["g", "w", "w", "g", "w", "w", "w", "g"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "partly cloudy": [
        ["b", "b", "b", "b", "y", "y", "b", "b"],
        ["b", "b", "b", "y", "y", "y", "y", "b"],
        ["b", "g", "g", "y", "y", "y", "y", "y"],
        ["g", "w", "w", "g", "g", "y", "y", "y"],
        ["g", "w", "w", "w", "w", "g", "g", "b"],
        ["g", "w", "w", "w", "w", "w", "g", "b"],
        ["g", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "partly cloudy night": [
        ["b", "b", "b", "b", "gD", "gD", "b", "b"],
        ["b", "b", "b", "gD", "gD", "gD", "gD", "b"],
        ["b", "g", "g", "gD", "gD", "gD", "gD", "gD"],
        ["g", "w", "w", "g", "g", "gD", "gD", "gD"],
        ["g", "w", "w", "w", "w", "g", "g", "b"],
        ["g", "w", "w", "w", "w", "w", "g", "b"],
        ["g", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "fog": [
        ["b", "b", "b", "b", "b", "b", "b", "b"],
        ["g", "g", "g", "g", "gD", "gD", "gD", "gD"],
        ["gD", "gD", "gD", "g", "g", "g", "g", "g"],
        ["g", "g", "g", "g", "g", "gD", "gD", "gD"],
        ["gD", "gD", "g", "g", "g", "g", "g", "g"],
        ["g", "g", "g", "g", "gD", "gD", "gD", "gD"],
        ["gD", "gD", "gD", "g", "g", "g", "g", "g"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "raining": [
        ["b", "b", "b", "g", "g", "g", "b", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["g", "g", "g", "g", "g", "g", "g", "g"],
        ["g", "g", "g", "g", "g", "g", "g", "g"],
        ["b", "bl", "b", "bl", "b", "bl", "b", "b"],
        ["b", "b", "bl", "b", "bl", "b", "bl", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "snowing": [
        ["b", "b", "b", "g", "g", "g", "b", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["g", "g", "g", "g", "g", "g", "g", "g"],
        ["g", "g", "g", "g", "g", "g", "g", "g"],
        ["b", "w", "b", "w", "b", "w", "b", "b"],
        ["b", "b", "w", "b", "w", "b", "w", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
    "thundering": [
        ["b", "b", "b", "g", "g", "g", "b", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["g", "g", "g", "y1", "g", "g", "y1", "g"],
        ["g", "g", "y1", "g", "g", "y1", "g", "g"],
        ["b", "b", "b", "y1", "b", "b", "y1", "b"],
        ["b", "b", "y1", "b", "b", "y1", "b", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
     "windy": [
        ["b", "b", "b", "g", "g", "g", "b", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["b", "g", "g", "g", "g", "g", "g", "b"],
        ["g", "g", "g", "y1", "g", "g", "y1", "g"],
        ["g", "g", "y1", "g", "g", "y1", "g", "g"],
        ["b", "b", "b", "y1", "b", "b", "y1", "b"],
        ["b", "b", "y1", "b", "b", "y1", "b", "b"],
        ["b", "b", "b", "b", "b", "b", "b", "b"],
    ],
}


def get_current_weather_data(city_query, api_key):
    url = f"https://api.weatherapi.com/v1/current.json?q={city_query}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        raise ValueError("API could not get info on given city query, or invalid API key.")


def get_current_weather_data_forecast(city_query, api_key):  
    #2 days, just in case the actual hour +6 is the next day
    url = f"https://api.weatherapi.com/v1/forecast.json?q={city_query}&days=2&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        raise ValueError("API could not get info on given city query, or invalid API key.")

    for y, row in enumerate(pattern):
        for x, pixel in enumerate(row):
            if pixel == "1":
                draw.point((x + x_offset, y + y_offset), fill=(255,255,255))

def draw_colored_pattern(draw, x_offset, y_offset, key):
    if key not in patterns:
        raise ValueError(f"The pattern '{key}' is not defined.")
    pattern = patterns[key]
    for y, row in enumerate(pattern):
        for x, pixel in enumerate(row):
            if pixel in colors:
                draw.point((x + x_offset, y + y_offset), fill=colors[pixel])

def get_weather_category(condition_code,is_day):
    weather_switch = {
            "sun": [1000],
            "partly cloudy": [1003],
            "cloudy": [1006, 1009],
            "fog": [1030, 1135, 1147],
            "raining": [
                1063, 1150, 1153, 1180, 1183, 1186, 1189, 1192, 1195, 1240,
                1243, 1246, 1273, 1276
                ],
            "snowing": [
                1066, 1114, 1117, 1168, 1171, 1204, 1207, 1210, 1213, 1216,
                1219, 1222, 1225, 1255, 1258, 1279, 1282
                ],
            "thundering": [1087, 1273, 1276, 1279, 1282],
            "windy": [1114, 1117]
            }
    if is_day == 0:
        # If it is night , we change the category
        weather_switch["moon"] = weather_switch.pop("sun", [1000])
        weather_switch["partly cloudy night"] = weather_switch.pop("partly cloudy", [1003])

    for category, codes in weather_switch.items():
        if condition_code in codes:
            return category
    return "unknown"


def get_weather_img(city_query:str, api_key, pixels:int=16) -> str:
    # Get weather data
    data_api = get_current_weather_data(city_query, api_key)

    current_weather_code = data_api["current"]["condition"]["code"]
    is_day = data_api["current"]["is_day"]

    weather_category = get_weather_category(current_weather_code,is_day)
    temperature_celsius = int(round(data_api["current"]["temp_c"])) 

    # Do pixel img
    img = Image.new('RGB', (pixels, pixels), color='black')
    draw = ImageDraw.Draw(img)

    # Extract the celsius digits
    first_digit = str(temperature_celsius).zfill(2)[0]
    second_digit = str(temperature_celsius).zfill(2)[1]

    # Draw temperature and weather
    draw_digit(draw, 3, 8, first_digit)
    draw_digit(draw, 9, 8, second_digit)
    draw_colored_pattern(draw, 4, 0, weather_category)

    # Save the img
    file_path = "weather.png"
    img.save(file_path)

    return file_path,


def get_weather_gif(city_query:str, api_key:str, pixels:int=16) -> str:
    data_api = get_current_weather_data_forecast(city_query, api_key=api_key)
    current_hour = int(data_api["location"]["localtime"].split()[1].split(":")[0])

    hourly_forecast = data_api["forecast"]["forecastday"][0]["hour"]
    #Array for all the images
    images=[]
    #range must be max 6 because specs
    for i in range(6):
        #Checking if the next hour is in the same day or next
        hour_index = (current_hour + i) % 24
        if current_hour + i < 24:  # Same day
            hour_data = data_api["forecast"]["forecastday"][0]["hour"][hour_index]
        else:  # Next day
            hour_data = data_api["forecast"]["forecastday"][1]["hour"][hour_index]

        condition_code = hour_data["condition"]["code"]
        is_day = hour_data["is_day"]

        #Celsius temperature
        temperature_celsius = int(round(hour_data["temp_c"]))

        weather_category = get_weather_category(condition_code, is_day)

        # Create the pixel image
        img = Image.new('RGB', (pixels, pixels), color=1)
        draw = ImageDraw.Draw(img)

        # Extract the Celsius digits
        first_digit = str(temperature_celsius).zfill(2)[0]
        second_digit = str(temperature_celsius).zfill(2)[1]
        # Determine the digit color (red for the first image, white for others)

        draw.rectangle([0, 15, i, 15], fill=(255, 255, 255))  #horizontal line to draw the hour, each point is the index of the hour

        draw_digit(draw, 3, 8, first_digit)
        draw_digit(draw, 9, 8, second_digit)
        draw_colored_pattern(draw, 4, 0, weather_category)

        # Save the gif with a unique name
        if img.getbbox():
            images.append(img)
        else:
            print(f"IMG {i} is empty, it will not be added")

    # Run the command with the new image

    images_array = [numpy.array(img) for img in images]

    gif_path = "weather_forecast.gif"

    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=[1000, 1000, 1000, 1000, 1000, 1000], loop=0)
    return gif_path


