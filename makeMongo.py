import csv
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["cubeRank"]
cards = client["cards"]

with open('cubeTutor.csv', 'r') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    for row in csvReader:
        if(row[0] != 'Card Name'):
            db.cards.insert_one({'Name':row[0], 'Pick Count':row[1], 'Pick Percentage':row[2], 'Cube Count':row[3]})
