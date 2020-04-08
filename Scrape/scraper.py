
# Scrape data and insert into mongodb

def scrape():
  
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

  # Google developer API key
  from config import api_key



  # Scrape corona data -> DF -> JSON
  url = 'https://www.worldometers.info/coronavirus/'

  # pretend to be a browser to avoid 403
  header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
  }

  r = requests.get(url, headers=header)

  dfs = pd.read_html(r.text)

  df = dfs[0]
  print(df)

  
  # Make geocoding api calls for coords

  countries = list(df['Country,Other'])
  countryCount = 0
  coordinates = []
  for country in countries:
      url = (f'https://maps.googleapis.com/maps/api/geocode/json?address={country}&key={api_key}')
      if country not in ['World','Total:']:
          print(country)
          try:
              response = requests.get(url).json()
              result = response['results'][0]['geometry']['location']
              loc = [result['lat'],result['lng']]
              print(loc)
          except:
              print('Failed Request')
              loc = [0,0]
          coordinates.append(loc)
          time.sleep(3)
      else:
          loc = [0,0]
          coordinates.append(loc)
      
      
      countryCount +=1 

  # Append coords to df
  df['Coords'] = coordinates


  # Connect to database
  conn = 'mongodb://localhost:27017'
  client = pymongo.MongoClient(conn)
  db = client.corona_db
  collection = db.corona_data
  # results = db.corona_data.find()[0]


  # Convert to json and insert
  df.to_json('countries.json')

  # Insert document into collection
  with open('countries2.json') as f:
    countries_data = json.load(f)

  collection.insert_one(countries_data)

scrape()
