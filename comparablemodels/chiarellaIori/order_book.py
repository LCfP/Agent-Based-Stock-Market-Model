# -*- coding: utf-8 -*-
"""
Orderbook object
Author: Blake LeBaron
Date: June 2016
Orderbook is a single instance of this object

Order book is implmented in a discretized fixed price range
Orders are linked lists of (quant, time) data pairs at each price
This allows for generalized order sizes, and keeps track of entry time on
the book.

Book is initialized with orders near one discrete tick off mid price
"""

import numpy as np


class orderBook:
    def __init__(self, minP, maxP, deltaP):
        # price ranges on order book
        self.minPrice = minP
        self.maxPrice = maxP
        self.midPrice = (maxP + minP) / 2.
        # discreteness in book
        self.deltaPrice = deltaP
        # discrete prices
        self.priceVec = np.arange(minP, maxP + deltaP, deltaP)
        self.nPrice = len(self.priceVec)
        # set up lists of lists for bids and asks
        self.bids = []
        self.asks = []
        for i in range(self.nPrice):
            self.bids.append([])
            self.asks.append([])
        # generate best bid
        pmid = self.discretePrice(self.midPrice)
        self.bestBidDex = pmid[0] - 1
        self.bestBid = self.realPrice(self.bestBidDex)
        # drop 5 orders in at best bid
        for i in range(5):
            self.bids[self.bestBidDex].append((1., 0))
        # drop 45 random orders near best bid
        for i in range(45):
            self.bids[self.bestBidDex - np.random.randint(1, self.bestBidDex / 4)].append((1., 0))
        # now set up best asks
        self.bestAskDex = pmid[0] + 1
        self.bestAsk = self.realPrice(self.bestAskDex)
        for i in range(5):
            self.asks[self.bestAskDex].append((1., 0))
        for i in range(45):
            self.asks[self.bestAskDex + np.random.randint(1, self.bestAskDex / 4)].append((1., 0))

    # take price and return (index, descrete price)
    def discretePrice(self, price):
        iPrice = int((price - self.minPrice) / self.deltaPrice)
        iPrice = max(iPrice, 0)
        iPrice = min(iPrice, self.nPrice - 1)
        dPrice = self.minPrice + self.deltaPrice * iPrice
        return (iPrice, dPrice)

    # take discrete price and return real price
    def realPrice(self, iPrice):
        return self.minPrice + self.deltaPrice * iPrice

    # add bid orders to the book
    def addBid(self, price, quant, t):
        # default no trade flag
        tradePrice = -1.
        # discretize prices
        ptup = self.discretePrice(price)
        iPrice = ptup[0]
        dPrice = ptup[1]
        # price < best ask then add to bid side
        if dPrice < self.bestAsk:
            # push (order,t) onto book at iPrice
            self.bids[iPrice].append((quant, t))
            # if better than bestBid, then update best
            if (dPrice > self.bestBid):
                self.bestBid = dPrice
                self.bestBidDex = iPrice
        # price > best ask, then execute trade at best ask
        else:
            # pop first in order off best ask
            tradeInfo = self.asks[self.bestAskDex].pop(0)
            tradePrice = self.bestAsk
            tradeQ = tradeInfo[0]
            # walk up the book to find new best ask
            for j in range(self.bestAskDex, self.nPrice):
                if (self.asks[j] != []):
                    break
            # reached end of book, set price there, and fill with order (emergency)
            if (self.asks[j] == []):
                self.bestAsk = self.priceVec[j]
                self.bestAskDex = j
                self.asks[j].append((1., t))
            # best ask at first occupied order
            else:
                self.bestAsk = self.priceVec[j]
                self.bestAskDex = j
        return tradePrice

    # repeat all this for adding an ask
    def addAsk(self, price, quant, t):
        tradePrice = -1.
        ptup = self.discretePrice(price)
        iPrice = ptup[0]
        dPrice = ptup[1]
        if dPrice > self.bestBid:
            self.asks[iPrice].append((quant, t))
            if (dPrice < self.bestAsk):
                self.bestAsk = dPrice
                self.bestAskDex = iPrice
        else:
            tradeInfo = self.bids[self.bestBidDex].pop(0)
            tradePrice = self.bestBid
            tradeQ = tradeInfo[0]
            for j in range(self.bestBidDex, -1, -1):
                if (self.bids[j] != []):
                    break
            if (self.bids[j] == []):
                self.bestBid = self.priceVec[j]
                self.bestBidDex = j
                self.bids[j].append((1., t))
            else:
                self.bestBid = self.priceVec[j]
                self.bestBidDex = j
        return tradePrice

    # cleanse book of old orders
    def cleanBook(self, t, tau):
        # sweep through book
        for i in range(self.nPrice):
            # check time on first (oldest) order
            if (self.bids[i] != []):
                # if old, then pop it off
                if (t - self.bids[i][0][1]) > tau:
                    self.bids[i].pop(0)
            # same for ask side
            if (self.asks[i] != []):
                if (t - self.asks[i][0][1] > tau):
                    self.asks[i].pop(0)
        # make sure there is some order at the end
        if self.bids[0] == []:
            self.bids[0].append((1., t))
        if self.asks[self.nPrice - 1] == []:
            self.asks[self.nPrice - 1].append((1., t))
        # reset best bid and ask prices
        i = self.nPrice - 1
        while self.bids[i] == []:
            i -= 1
        self.bestBidDex = i
        self.bestBid = self.realPrice(i)
        i = 0
        while self.asks[i] == []:
            i += 1
        self.bestAskDex = i
        self.bestAsk = self.realPrice(i)

    # utility to print the order book
    def printBook(self):
        for i in range(self.nPrice):
            if (self.bids[i] != []):
                print(self.realPrice(i), self.bids[i])
        print("------")
        for i in range(self.nPrice):
            if (self.asks[i] != []):
                print(self.realPrice(i), self.asks[i])