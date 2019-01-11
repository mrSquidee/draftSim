import json
import random
from math import floor
from player import Player
from mtgsdk import Card

# Loading Files

cube = json.load(open('cubeSet.json', encoding='utf-8'))
setData = cube['CUBE']
cards = []
with open('miles_cube.txt', 'r') as cubeFile:
    for row in cubeFile:
        cards.append(row[:-2])
boosters = [[], [], []]
numPlayers = 8
players = []
for i in range(0, numPlayers):
    players.append(Player())

# Fills a slot for a booster

def chooseSlot(slot):
    random.shuffle(cards)
    cardName = cards.pop()
    card = Card.where(name=cardName)
    return card

# Makes a booster by choosing slots

def makeBooster(round):
    for i in range(numPlayers):
        newBooster = []
        for slot in setData['booster']:
            nextCard = chooseSlot(slot)
            newBooster.append(nextCard)
        boosters[round].append(newBooster)

# Writes the pools out to files

def writeSet(cardSet, file):
    with open(file, 'w') as writeFile:
        for card in cardSet:
             writeFile.write(card['name'] + '\n')

# Pass packs

def passPacks(pickNum, round):
    curBooster = pickNum
    for player in players:
        curBooster += 1
        if(curBooster >= numPlayers):
            curBooster = curBooster % numPlayers
        player.setBooster(boosters[round][curBooster])

# Boosters get made

for i in range(3):
    makeBooster(i)

# Draft happens

for pickNum in range(45):
    round = floor(pickNum/15)
    passPacks(pickNum, round)
    playerCount = 1
    for player in players:
        player.pick()
        playerCount += 1

# Files get wrote out

playerCount = 1
for player in players:
    printSet(player.pool, 'player' + str(playerCount) + '.txt')
    playerCount += 1
