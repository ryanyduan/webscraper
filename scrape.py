from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series,DataFrame
import csv


#This will appear when I scrape so the server knows who I am
headers = {
    'User-Agent': 'Ryan Duan (Student)',
    'From': 'ryanyduan@gmail.com'
}

#Choose the url
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

result = requests.get(url, headers=headers)
c = result.content

soup = BeautifulSoup(c,'lxml')

#This returns a list of everything inside that div id
summary = soup.find("div",{"id":"mw-content-text"})

#This returns a list of all the tables in summary
tables = summary.find_all('table')

#create new list to store items (every columns in each row)
data = []

#returns a list of all <tr> in tables[0]
rows = tables[0].findAll('tr')


for tr in rows:
    cols = tr.findAll('td')
    for td in cols:
        text = td.find(text=True)  #this checks if there's text in the td
        data.append(str(text)) #make sure to convert to str else pandas will read it as a long str if there's different data types

Ticker = []
Security_Name = []

index = 0

for i in range(len(data)):
    if data[i] == "Information Technology":
        #These indexes are arbitrary it's just the way this specific wikipedia page is set up
        Ticker.append(data[i-3])
        Security_Name.append(data[i-2])
        

#Create the pandas series
Ticker = Series(Ticker)
Security_Name = Series(Security_Name)

graph = pd.concat([Ticker,Security_Name],axis=1)



graph.columns = ['Ticker','Security']
print(graph)

#write it to an excel file (.csv)
graph.to_csv('test.csv')


