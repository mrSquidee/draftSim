import json
import random
from math import floor
from player import Player
from mtgsdk import Card
from pymongo import MongoClient

# Loading Files

cube = json.load(open('cubeSet.json', encoding='utf-8'))
setData = cube['CUBE']
cards = []
with open('miles_cube.txt', 'r') as cubeFile:
    for row in cubeFile:
        if(row[:2] != '//'):
            cards.append(row[:-1])      

newDraft = False
draftNum = 1

client = MongoClient("localhost", 27017)
db = client["drafts"]
draft = client["draft"]

boosters = [[], [], []]
numPlayers = 8

players = []
for i in range(0, numPlayers):
    players.append(Player())

# Fills a slot for a booster

def chooseSlot(slot):
    random.shuffle(cards)
    cardName = cards.pop()
    card = Card.where(name=cardName).all()
    return dict(vars(card[0]))

# Makes a booster by choosing slots

def makeBooster(pround):
    for _ in range(numPlayers):
        newBooster = []
        for slot in setData['booster']:
            nextCard = chooseSlot(slot)
            newBooster.append(nextCard)
        boosters[pround].append(newBooster)

# Exports the newly made boosters to mongo

def exportBoosters():
    db.draft.insert_one({'draftNum': draftNum, 'playerNum':numPlayers, 'draft':boosters})

# Writes the pools out to files

def writeSet(cardSet, file):
    with open(file, 'w') as writeFile:
        for card in cardSet:
             writeFile.write(card['name'] + '\n')

# Pass packs

def passPacks(pickNum, pround):
    curBooster = pickNum
    for player in players:
        curBooster += 1
        curBooster = curBooster % numPlayers
        player.setBooster(boosters[pround][curBooster])

# Boosters get made

if(newDraft == True):
    for i in range(3):
        makeBooster(i)
    exportBoosters()
else:
    try:
        boosters = db.draft.find_one({'draftNum':draftNum, 'playerNum':numPlayers})['draft']
    except:
        raise NameError('This draft does not exist')
#     boosters = db.drafts.find_one({'draftNum':draftNum})['draft']

# Draft happens

for pickNum in range(45):
    pround = floor(pickNum/15)
    passPacks(pickNum, pround)
    playerCount = 1
    for player in players:
        player.pick()
        playerCount += 1

# Files get wrote out

playerCount = 1
for player in players:
    print(player.colorR)
    writeSet(player.pool, 'drafts/player' + str(playerCount) + '.txt')
    playerCount += 1
