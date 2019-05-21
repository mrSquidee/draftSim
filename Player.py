import random
import json
import csv
import math
from pymongo import MongoClient
from mtgsdk import Card
import math

client = MongoClient("localhost", 27017)
db = client["cubeRank"]
cards = client["cards"]

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
        # self.arch = {
        #     "WU": 0,
        #     "UB": 0,
        #     "BR": 0,
        #     "RG": 0,
        #     "GW": 0,
        #     "WB": 0,
        #     "UR": 0,
        #     "BG": 0,
        #     "RW": 0,
        #     "GU": 0
        # }

    def setBooster(self, booster):
        self.pickFrom = booster

    def randPick(self):
        random.shuffle(self.pickFrom)
        self.pool.append(self.pickFrom.pop())

    def update(self):
        total = 0
        for color in self.colorR:
            total += self.colorR[color]
        avr = total/5
        for color in self.colorR:
            self.colorR[color] -= avr
        total = 0
        # for arch in self.arch:
        #     total += self.arch[arch]
        # avr = total/10
        # for arch in self.arch:
        #     self.arch[arch] -= avr


    def inputPick(self, cardIndex):
        self.pool.append(self.pickFrom[cardIndex])
        self.pickFrom.remove(self.pickFrom[cardIndex])

    def updateAdders(self, recentPick, recentRank):
        color = recentPick.get('mana_cost')
        if(color == None):
            color = '{0}'
        for pip in color:
            if(pip in self.colorR):
                self.colorR[pip] += recentRank/75

        # TODO: add archetypes somewhere somehow
        # for arch in rankings['archetypes']:
        #     for i in arch:
        #         if(i in recentPick.get('text', '')):
        #             self.arch[arch] += recentRank * 0.02

    def addScore(self, card):
        rankAdding = 0
        curColor = card.get('color_identity', ['C'])
        for color in curColor:
            if(color in self.colorR):
                rankAdding += self.colorR[color]

        # curArch = ''
        # for arch in rankings['archetypes']:
        #     for i in arch:
        #         if(i in card.get('text', '')):
        #             rankAdding += self.arch[arch]

        return rankAdding

    def pick(self):
        best = self.pickFrom[0]
        cur = self.pickFrom[0]
        bestRank = float(db.cards.find_one({'Name':best['name']})['Pick Percentage'])
        bestWOAdders = bestRank
        for cur in self.pickFrom:
            curRank = float(db.cards.find_one({'Name':cur['name']})['Pick Percentage'])
            curWOAdders = curRank
            curRank += self.addScore(cur)
            if(curRank >= bestRank):
                best = cur
                bestRank = curRank
                bestWOAdders = curWOAdders

        self.updateAdders(best, bestWOAdders)


        self.pickFrom.remove(best)
        self.pool.append(best)
        self.update()
