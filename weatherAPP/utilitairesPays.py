import requests,json,random, time, traceback
import language_countries
# use either getJSON or searchJson for cities and countries
def getCountryInformationList():
    username = "ol1oly"
    endpoint = 'countryInfoJSON'

    parameters = '&'.join([     # Postal code to search    #consider using countryName and contientName instead of code
    f'username={username}'  # Must include GeoNames username in all API calls
    ])

    url = f'http://api.geonames.org/{endpoint}?{parameters}'
    
    response = requests.get(url)
    print(response.status_code)
    
    data = response.json()

    Allcountry_info = data["geonames"]

    if 'geonames' in data and data['geonames']:
        retour = dict()
        for item in Allcountry_info:
            retour[item["countryCode"]] = item
        return retour
    else:
        return None

def getRandomCountryInformation(continent = None,language = None):
    if continent:
        if continent in cache:
            retourner = cache[continent]
            print("already in it")
        else:
            if continent and continent.lower() in continent_codes:
                code = continent_codes[continent.lower()]  
                retourner = [item for item in AllCountries.values() if item["continent"] == code] 
                cache[continent] = retourner
            else:
                retourner =[item for item in AllCountries.values()]
    elif language and language.lower() in language_country_list:
        retourner = [item for item in AllCountries.values() if item["countryCode"] in language_country_list[language.lower()]]
    
    else:
        retourner =[item for item in AllCountries.values()]
    
    i = random.randint(0,len(retourner)-1)
    #print(retourner[i].get("name"))
    return retourner[i]

def getSpecificCountryInformation(name):
    code = getCountryCodeByName(name)
    if code:
        
        return AllCountries[code]
    
    return None

def putCountryCodesInFile():
    
    file = open("weatherAPP/countrycodes.txt","w",encoding='utf-8')
    for country in AllCountries:
        if country["capital"] and int(country["population"]) >20000:
            file.write(f'{country["countryCode"]} {(country["countryName"].lower())}\n')
    file.close()

def putCapitalsInFile():
    with open("weatherAPP\capitals.txt","w",encoding='utf-8') as file:
        for item in AllCountries.values():
            if item["capital"] and int(item["population"]) >20000:
                file.write((item["countryName"].lower()) + " # " + (item["capital"]) + "\n")
                

    file.close

def GetDicCountryCodes():
    countryCode = dict()
    with open("weatherAPP/countryCodes.txt") as file:
        lines = [line.strip() for line in file.readlines()]
        for item in lines:
            x = item.split(" ",1)
           
            countryCode[x[1]] = x[0]
    return countryCode       
    
def GetDicCapitals():
    capitals = dict()
    with open("weatherAPP/capitals.txt") as file:
        lines = [line.strip() for line in file.readlines()]
        for item in lines:
            x = item.split(" # ",1)    
            capitals[x[0]] = x[1]
         
    return capitals    

def getCountryCodeByName(name):
    return countryCodes[name.lower()]




def get_country_code(lat, lng):

    base_url = "http://api.geonames.org/countryCode"
    params = {
        "lat": lat,
        "lng": lng,
        "username": "ol1oly"
    }

    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Print response content for debugging
    return response.text



def getRandomCapitalInformation(continent = None,language = None):
    retourner = None 
    while retourner is None:
        randomCountry = getRandomCountryInformation(continent,language) 
        retourner = getSpecificCityInformation(randomCountry["capital"],randomCountry["countryName"])
        
    return retourner
def getRandomCityInformation(country = None,continent = None,language = None):
   
    username = "ol1oly"
    parameters = [ f'username={username}',"featureClass=P","style=full","maxRows=100","cities=cities15000"]
    
    if country and country.lower() in countryCodes:
        parameters.append(f'countryBias={countryCodes[country.lower()]}')
    elif continent and continent.lower() in continent_codes:
        country_info = getRandomCountryInformation(continent=continent)
        if country_info:
            code = country_info["countryCode"]
            parameters.append(f'continentCode={continent_codes[continent.lower()]}')
            parameters.append(f'countryBias={code}')
    elif language and language.lower() in language_codes:
        country_info = getRandomCountryInformation(language=language)
        if country_info:
            code = country_info["countryCode"]
            parameters.append(f'countryBias={code}')
    else:
        country_info = getRandomCountryInformation()
        if country_info:
            code = country_info["countryCode"]
            parameters.append(f'countryBias={code}')
    
    parameters = '&'.join(parameters)
    endpoint = "searchJSON"
    url = f'http://api.geonames.org/{endpoint}?{parameters}'
    
    response = requests.get(url)
    data = response.json()
    
    if 'geonames' in data:
        city = random.choice(data['geonames'])
        #print(city)
        #city = data["geonames"][0]
        return {
            'name': city.get('name'),
            'country': city.get('countryName'),
            'population': city.get('population'),
            'latitude': city.get('lat'),
            'longitude': city.get('lng')
        }
    else:
        return None

def getSpecificCityInformation(cityName,countryName =None,continentName=None):
    cityName = cityName.lower()
    username = "ol1oly" 
    endpoint = 'searchJSON'
    parameters = [ f'username={username}',f'name={cityName.title()}',"featureClass = P"]
    if countryName:
        if countryName.lower() in countryCodes:
            parameters.append(f'countryBias={countryCodes[countryName.lower()]}')
    else:
        if continentName:
            if continentName.lower() in continent_codes:
                parameters.append(f'continentCode={continent_codes[continentName.lower()]}')
    parameters = '&'.join(parameters)

    url = f'http://api.geonames.org/{endpoint}?{parameters}'

    response = requests.get(url)
    
    data = response.json()
    cityInformation = data["geonames"]
    #print(cityInformation[0])
    for item in cityInformation:
        if item["name"].lower() == cityName:
            
            return {
                'name': item.get('name'),
                'country': item.get('countryName'),
                'population': item.get('population'),
                'latitude': item.get('lat'),
                'longitude': item.get('lng')
            }             
       
    print("no city with that name was found")
    return None
    
def getSpecifiCapitalInformation(countryName):
    capital = dictonnaryCapitals[str(countryName.lower())]
    if capital:
            return getSpecificCityInformation(capital,countryName)
    


continent_codes = {
    "africa": "AF",
    "antarctica": "AN",
    "asia": "AS",
    "europe": "EU",
    "north america": "NA",
    "oceania": "OC",
    "south america": "SA"
}
language_codes = {
    "english": "en", "french": "fr", "spanish": "es", "arabic": "ar",
    # Add other languages as needed
}
language_country_list = {"french":language_countries.french_speaking_countries,
                         "english": language_countries.english_speaking_countries,
                         "spanish": language_countries.spanish_speaking_countries,
                         "arabic": language_countries.arabic_speaking_countries}


cache = {}
start = time.time()

AllCountries = getCountryInformationList()
countryCodes = GetDicCountryCodes()
dictonnaryCapitals = GetDicCapitals()     

end = time.time()

try:

    print(getSpecificCountryInformation("canada"))
    #print(getSpecificCityInformation("montreal","canada"))
    #print(getRandomCityInformation())
    
    '''print(getRandomCityInformation())
    print(getRandomCityInformation())
    print(getRandomCityInformation())
    print(getRandomCityInformation())
    print(getRandomCityInformation())'''


    
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    print(e)
    #  the line number where the error occurred
    line_number = tb[-1].lineno
    print(f"Error occurred on line {line_number}")

veryend = time.time()

print("fetching data: ", str(end-start))
print("rest: " , veryend-end)
#putCapitalsInFile()
#putCountryCodesInFile()
#print(getSpecificCountryInformation("canada"))

