import requests, json, tkinter as tk, math, random
from tkinter import ttk

# can do the quiz on capitals, countries and regular big cities
# for capitals and countries: get all the information needeed and put it on text file along with the time it was updated. update every month
# for countries: another option is to use geonames[randomNumber] and ask questions about it
# for cities: use random.choice and featureClass=P includes populated places (cities)


def isCorrect(string):
    special_characters_and_numbers = set("!\"#$%&'()*+,./:;<=>?@[\\]^_`{|}~0123456789")
    if string  == "":
        return False
    for i in string:#
        if special_characters_and_numbers.__contains__(i):
            return False
    return True

def kelvin_to_celcius(temp):
    return temp-273
def kelvin_to_farenheit(temp):
    return ((temp - 273) * 1.8) + 32


def getTemperature(nameCity):

        api_key = "b863c11271f7dea5f27b82a64ba7f25e"

        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        complete_url = base_url + "appid=" + api_key + "&q=" + nameCity

        response = requests.get(complete_url)

        x = response.json()
    
        correct  = isCorrect(nameCity)
        try:
            if x["cod"] != "404": # if the temperature is found
                y = x["main"]
                current_temperature = y["temp"]
            
                print("in celsius: ",kelvin_to_celcius(current_temperature))
                print("in farenheit: ", kelvin_to_farenheit(current_temperature))
 
                return current_temperature # in kelvin
        except:
            return None      
        return None

def create_star(canvas, center_x, center_y, size, points, fill_color, outline_color):
    angle_between_points = math.pi / points
    star_points = []

    starting_angle = math.pi / 2

    for i in range(2 * points):
        angle =  i * angle_between_points
        radius = size if i % 2 == 0 else size / 2
        x = center_x + radius * math.sin(angle)
        y = center_y - radius * math.cos(angle)
        star_points.append((x, y))

    return (canvas.create_polygon(star_points, fill=fill_color, outline=outline_color, tag="star"))

def getListFavoriteCities():
   
    list = set()
    file = open("weatherAPP/favourite.txt")
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        list.add(line)
        print("new entry: " , line)
    
    return list

def writeNewFavoriteCities(new):
    file = open("weatherAPP/favourite.txt", 'w')
    
    toWrite = [item + "\n" for item in new]        
    file.writelines(toWrite)#
    file.close()

def getTriangleCoordinates(height,length,side): # side is a boolean false if toward righ
    x1 = length*side
    y1 = 0
    x2 = x1
    y2 = height
    x3 = length-x1
    y3 = height/2
    coordinates = [x1, y1, x2, y2, x3, y3]
    return coordinates

def calculate_population_score(actual_population, guessed_population):
    
    calculate = True
    for i in guessed_population:
        if i not in "0123456789":
            calculate = False
    if not guessed_population.strip():
        return 0
    if not calculate:
        return 0
    #print("the type osf :", type(actual_population))
    actual_population = int(float(actual_population))
    guessed_population = int(float(guessed_population))    # Calculate the absolute percentage error
    error_percentage = abs((guessed_population - actual_population) / actual_population) * 100
    
    # Determine the base score based on the error percentage
    if error_percentage <= 0.5:
        base_score = 100
    elif error_percentage <= 2:#
        base_score = 90
    elif error_percentage <= 5:
        base_score = 80
    elif error_percentage <= 10:
        base_score = 70
    else:
        base_score = max(5, 50 - int((error_percentage - 10) / 2))  # Decrease score, but not below 5 points

    # Calculate streak bonus
    #streak_bonus = (streak_count - 1) * 10 if streak_count >= 2 else 0

    # Final score
    total_score = base_score #+ streak_bonus

    return total_score

def calculate_positions_score(xTrue,yTrue,xGuess,yGuess):
        distance = calculateDistance(xTrue,xGuess,yTrue,yGuess)
        score = 5000 * math.exp(-distance / 50)
        score = round(score)
        return score

def calculateDistance(x1,x2,y1,y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    distance = round(distance)
    return distance

def getStyle():
    style = ttk.Style()
    backG = "#F9F7F7"

    primaryColor = "#3F72AF"
    secondColor = "#112D4E"
    thirdColor = "#DBE2EF"
    fourthColor = "#3c5370"
    fontName = "verdana"
    
    # Configure the style for the custom button
    style.configure('SearchCity.TButton',
        font=(fontName, 20, 'bold'),    # Font style, size, and weight
        foreground=secondColor,        # Text color
        background=secondColor,               # Background color (may not apply on all systems)
        padding=10)
    
    style.map('SearchCity.TButton',
        foreground=[('pressed', secondColor), ('active', secondColor)])
    
    style.configure('CountryQuiz.TButton',
        font=(fontName, 20, 'bold'),    # Font style, size, and weight
        foreground=primaryColor,        # Text color
        background=backG,               # Background color (may not apply on all systems)
        padding=10)                     # Padding inside the button

    # Additional customization when the button is pressed or hovered over
    style.map('CountryQuiz.TButton',
        foreground=[('pressed', secondColor), ('active', secondColor)],
        background=[('pressed', thirdColor), ('active', thirdColor)])
    
    style.configure('CheckGuess.TButton',
                        font=(fontName, 12),            # Font style and size
                        foreground=secondColor,         # Text color
                        background=primaryColor,        # Background color (may not apply on all systems)
                        padding=6)                      # Padding inside the button

        # Additional customization for button states
    style.map('CheckGuess.TButton',
        foreground=[('pressed', primaryColor), ('active', primaryColor)],
        background=[('pressed', '!disabled', secondColor), ('active', secondColor)])
    
    
    
    
    return style
