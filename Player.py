import random
import json
import csv
import pandas as pd
import math

# rankings = json.load(open('../cubeRanker/cubeRank.json', encoding='utf-8'))

with open('cubeTutor.csv', 'r') as csvFile:
    csvReader = csv.reader(csv_file, delimiter=',')
    for row in csvReader:


class Player():

    def __init__(self):
        self.pickFrom = []
        self.pickNum = 0
        self.pool = []
        self.colorR = {
            'W': 0,
            'U': 0,
            'B': 0,
            'R': 0,
            'G': 0
        }
        self.arch = {
            "WU": 0,
            "UB": 0,
            "BR": 0,
            "RG": 0,
            "GW": 0,
            "WB": 0,
            "UR": 0,
            "BG": 0,
            "RW": 0,
            "GU": 0
        }

    def setBooster(self, booster):
        self.pickFrom = booster

    def randPick(self):
        card = self.pickFrom[random.randint(0, len(self.pickFrom)-1)]
        self.pickFrom.remove(card)
        self.pool.append(card)

    def update(self):
        total = 0
        for color in self.colorR:
            total += self.colorR[color]
        avr = total/5
        for color in self.colorR:
            self.colorR[color] -= avr
        total = 0
        for arch in self.arch:
            total += self.arch[arch]
        avr = total/10
        for arch in self.arch:
            self.arch[arch] -= avr


    def inputPick(self, cardIndex):
        self.pool.append(self.pickFrom[cardIndex])
        self.pickFrom.remove(self.pickFrom[cardIndex])

    def updateAdders(self, recentPick, recentRank):
        color = recentPick.get('manaCost', '')
        for pip in color:
            if(pip in self.colorR):
                self.colorR[pip] += recentRank * 0.04;

        for arch in rankings['archetypes']:
            for i in arch:
                if(i in recentPick.get('text', '')):
                    self.arch[arch] += recentRank * 0.02

    def addScore(self, card):
        rankAdding = 0

        curColor = card.get('colorIdentity', 'c')
        for color in curColor:
            if(color in self.colorR):
                rankAdding += self.colorR[color]

        curArch = ''
        for arch in rankings['archetypes']:
            for i in arch:
                if(i in card.get('text', '')):
                    rankAdding += self.arch[arch]

        return rankAdding

    def pick(self):
        best = self.pickFrom[0]
        cur = self.pickFrom[0]
        bestRank = rankings['rankings'].get(best['name'], 0)
        for cur in self.pickFrom:
            curRank = rankings['rankings'].get(cur['name'], 0)
            curRank += self.addScore(cur)
            if(curRank >= bestRank):
                best = cur
                bestRank = curRank

        self.updateAdders(best, bestRank)


        self.pickFrom.remove(best)
        self.pool.append(best)
        self.update()
