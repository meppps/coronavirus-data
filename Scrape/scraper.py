# Scrape Data
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import requests

url = 'https://www.worldometers.info/coronavirus/'

import requests

# pretend to be a browser to avoid 403
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)

dfs = pd.read_html(r.text)

df = dfs[0]

print(df)