
# Web Scrape -> Check for db coords -> matchup and feed to client
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import requests
import pymongo
import datetime
import json
import requests
import time

def scrape():
    # Get data
    url = 'https://www.worldometers.info/coronavirus/'

    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text,'lxml')

    trs = soup.find_all('tr')

    # Connect to db
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.corona_db
    collection = db.country_coords
    coordsList = collection.find_one()['countries']

    # Parse data, loop thru countries
    # Loop through countries
    countries = []

    names = []
    totalCasesList = []
    deathsList = []
    recoveredList = []
    activeCasesList = []
    testsList = []
    populationList = []
    coordsData = []
    newCasesList = []
    coordsFound = False

    for i in range(len(trs)):
        # If country row, pull data
        if 'href="country' in str(trs[i]):
            country = str(trs[i]).split('\n')
            name = country[2].split('</a>')[0].split("/\">")[1]
            totalCases = country[3].split('>')[1].split('<')[0]
            deaths = country[5].split("\">")[1].split('<')[0]
            recovered = country[8].split("\">")[1].split('<')[0]
            activeCases = country[10].split("\">")[1].split('<')[0]
            tests = country[14].split("\">")[1].split('<')[0]
            population = country[16].split('>')[2].split('<')[0]
            

            for x in range(len(coordsList)):
                if coordsList[x]['name'] == name:
                    lat = coordsList[x]['lat']
                    lng = coordsList[x]['lng']
                    coordsFound = True
                    break
                else:
                    lat = 0
                    lng = 0
                    
            # if coordsFound == False:
            #     lat = 0
            #     lng = 0
            
            
            try:
                newCases = country[4].split('>+')[1].split('</')[0]
            except:
                newCases = 0

            
            names.append(name)
            totalCasesList.append(totalCases)
            deathsList.append(deaths)
            activeCasesList.append(activeCases)
            recoveredList.append(recovered)
            populationList.append(population)
            testsList.append(tests)
            coordsData.append([lat,lng])
            newCasesList.append(newCases)
            
            

            coordsFound = False
            i+=1

    # Create dictionary of new country stats
    countryDict = {
        'name': names,
        'totalCases': totalCasesList,
        'deaths': deathsList,
        'recovered': recoveredList, 
        'activeCases': activeCasesList,
        'population': populationList,
        'coords': coordsData,
        'newCases': newCasesList,
        'tests': testsList
    }
    updatedData = [countryDict]

    # Update data in db
    collection = db.corona_data
    collection.update_one({},{"$set":{"countries":updatedData}})

scrape()
