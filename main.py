import pandas as pd
import requests
import json

earthquakes = pd.read_csv("database.csv")

def locate(index):
#takes the index of earthquake in database or a tuple of the lat and long

    if type(index) is int:

        #locate the lat and long
        lat = float(earthquakes["Latitude"][index])
        long = float(earthquakes["Longitude"][index])

        #make a request to get the country
        url = "http://api.geonames.org/findNearbyPlaceNameJSON?lat=" + str(lat) + "&lng=" + str(long) + "&username=terriwm"
        country_data = requests.get(url)
        country_data = json.loads(country_data.text)

        #check if the api returned a country or nothing if nothing it means it is in the ocean
        try:
            country_name = country_data["geonames"][0]["countryName"]
        except:
            country_name = "Ocean"

        return(country_name)
    elif type(index) is tuple:
        lat = float(index[0])
        long = float(index[1])

        url = "http://api.geonames.org/findNearbyPlaceNameJSON?lat=" + str(lat) + "&lng=" + str(long) + "&username=terriwm"
        country_data = requests.get(url)
        country_data = json.loads(country_data.text)
        try:
            country_name = country_data["geonames"][0]["countryName"]
        except:
            country_name = "Ocean"

        return(country_name)



def most_earthquakes_year():
    years = {}

    #iterate over the database, checking the year of the earthquake and adding to the dictionary
    for i in range(len(earthquakes)):
        year = earthquakes["Date"][i][6:10]

        if type(year) is not None:
            if year in years.keys():
                years[year] += 1
            else:
                years[year] = 0

    #iterate over the dictionary and find the year with the most earthquakes
    year_with_most_earthquakes = earthquakes["Date"][0][6:10]
    for y in years:
        if years[y] > years[year_with_most_earthquakes]:
            year_with_most_earthquakes = y

    return(year_with_most_earthquakes)


def avg_location():
    total_lat = 0
    total_long = 0

    #iterate over the dataset and find sum the latitude and longitude
    for i in range(len(earthquakes)):
        total_lat += float(earthquakes["Latitude"][i])
        total_long += float(earthquakes["Longitude"][i])
    
    #divide the sums by the totlat to get the avg
    avg_lat = total_lat / len(earthquakes["Latitude"])
    avg_long = total_long / len(earthquakes["Longitude"])

    print("The Average location is in: " + locate((avg_lat, avg_long)))

def highest_magnitude():
    highest_mag = 0
    highest_mag_loc = 0

    #iterate over the dataset find the highest magnitude earthquake and store all of its data
    for i in range(len(earthquakes)):
        if float(earthquakes["Magnitude"][i]) > highest_mag:
            highest_mag = float(earthquakes["Magnitude"][i])
            highest_mag_loc = i

    print("The highest magitude earthquake was: " + str(earthquakes["Magnitude"][highest_mag_loc]) + " this earthquake happened on: " + str(earthquakes["Date"][highest_mag_loc]) + " " + str(earthquakes["Time"][highest_mag_loc]) + " in: " + str(locate(highest_mag_loc)))


#use date format DD/MM/YYYY
def earthquake_on_date(date):
    day = date[0:2]
    month = date[3:5]
    year = date[6:len(date)]
    new_date = month + "/" + day + "/" + year

    #reformats the date as the dataset uses mm/dd/yyyy and the correct date format is dd/mm/yyyy
    
    earthquake_on_day_index = None
    for i in range(len(earthquakes)):
        if earthquakes["Date"][i] == new_date:
            earthquake_on_day_index = i
            break

    #do string formating to make the data readable by the human
    if earthquake_on_day_index is not None:
        location = str(locate((float(earthquakes["Latitude"][earthquake_on_day_index]), float(earthquakes["Longitude"][earthquake_on_day_index]))))
        magnitude = str(earthquakes["Magnitude"][earthquake_on_day_index])
        time = str(earthquakes["Time"][earthquake_on_day_index])
        print("There was an earthquake on: " + date + " " + time + " (UTC), in: " + location + ", with magnitude: " + magnitude)
    elif earthquake_on_day_index is None:
        print("There was no earthquake on that day")

def earthquake_causes():
    causes = {}

    #uses the same code from the years function
    for i in range(len(earthquakes)):
        cause = earthquakes["Type"][i]

        if type(cause) is not None:
            if cause in causes.keys():
                causes[cause] += 1
            else:
                causes[cause] = 0
                causes[cause] += 1

    for c in causes:
        print(str(c) + ": " + str(causes[c]))


#ui, pulls all the functions together
while True:
    print("Select a function:")
    print("1. Find Earthquake on a Specific Date")
    print("2. Find the average location of all earthquakes")
    print("3. Find Earthquake Causes")
    print("4. Find Year With Most earthquakes")
    print("5. Find highest Magnitude Earthquake")
    print("E. Exit")
    selection = input()
    if selection == "1":
        print("\n\n\n\n\nUse Date Format DD/MM/YYYY\nFor Example: 01/12/2005\nEnter a Date:")
        date = input()
        earthquake_on_date(date)
        print("\n\n\n\n\n")
    elif selection == "2":
        print("\n\n\n\n\n")
        avg_location()
        print("\n\n\n\n\n")
    elif selection == "3":
        print("\n\n\n\n\nThe causes of earthquakes and how many times they occurred:")
        earthquake_causes()
        print("\n\n\n\n\n")
    elif selection == "4":
        print("\n\n\n\n\n")
        print("The year with the most earthquakes is: " + most_earthquakes_year())
        print("\n\n\n\n\n")
    elif selection == "5":
        print("\n\n\n\n\n")
        highest_magnitude()
        print("\n\n\n\n\n")
    elif selection == "E":
        break
    else:
        print("\n\n\n\n\nEnter a Valid Command\n\n\n\n\n")
