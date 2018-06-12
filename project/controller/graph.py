#!/usr/bin/python3
# coding: utf-8

import networkx as nx
from project.controller.exception import CapacityNotAllowed, IndexDemandIncorrect
from functools import total_ordering
from copy import deepcopy
from collections import OrderedDict

@total_ordering
class Bus():
    
    def __init__( self, numberBus, capacity, isBusCama, position ):
        self.__numberBus = numberBus
        self.__capacity = capacity
        self.__numberPassenger = 0
        self.__isBusCama = isBusCama
        self.__position = position

    def getNumberBus(self):
        return self.__numberBus

    def getCapacity(self):
        return self.__capacity

    def getIsBusCama(self):
        return self.__isBusCama

    def getPosition(self):
        return self.__position

    def getNumberPassenger(self):
        return self.__numberPassenger

    def addPassenger(self, n ):
        if self.__numberPassenger + n > self.__capacity:
            raise CapacityNotAllowed()
        self.__numberPassenger += n

    def subsPassenger( self, n ):
        if self.__numberPassenger -n < 0:
            raise CapacityNotAllowed()
        self.__numberPassenger -= n


    def __eq__(self, other):
        return ((self.__numberBus) == (other.getNumberBus()))

    def __ne__(self, other):
        return not (self==other)

    def __lt__(self, other):
        return ((self.__numberBus) < (other.getNumberBus()))

    def __repr__(self):
        cad = f'{"Bus {}".format(self.__numberBus) :*^30}\n'
        cad += f'{"capacity": <10} : {self.__capacity} \n'
        cad += f'{"isBusCama": <10} : {self.__isBusCama} \n'
        cad += f'{"position": <10} : {self.__position} \n\n'

        return cad



class AdminAgency():
    
    def __init__(self):
        self.__listBuses = []
        self.__dicDemandsForDay = {}
        self.__map = nx.Graph()
        self.__graph = None

    def getMap(self):
        return self.__map
    
    def addBus(self, bus):
        self.__listBuses.append(bus)
        self.__listBuses = sorted(self.__listBuses)

    def getGraph(self):
        return self.__graph

    def setGraph(self, graph):
        self.__graph = graph

    def getListBuses(self):
        return self.__listBuses

    def getDictDemandForDay(self):
        return self.__dicDemandsForDay

    def addRoute(self, nodeBegin, nodeEnd, timeTravel ):
        self.__map.add_edge( nodeBegin, nodeEnd, weight=timeTravel )
        self.__graph = deepcopy( self.__map )


    def __orderingDictDemand(self):
        for k in self.__dicDemandsForDay.keys():
            self.__dicDemandsForDay[k] = OrderedDict(sorted(self.__dicDemandsForDay[k].items(), key=lambda t: t[1], reverse=True))


    def addDemand(self,nodeBegin, nodeEnd, demandPassenger ):

        if not nodeBegin in self.__dicDemandsForDay:
            self.__dicDemandsForDay[nodeBegin] = {}
        self.__dicDemandsForDay[nodeBegin][nodeEnd] = demandPassenger
        self.__orderingDictDemand()



    def lenDemand(self):
        n = 0
        for k in self.__dicDemandsForDay.keys():
            n += len(self.__dicDemandsForDay[k])
        return n

    def setDemand(self, nodeBegin, nodeEnd, demandPassenger ):
        try:
            self.__dicDemandsForDay[nodeBegin][nodeEnd] = demandPassenger
        except KeyError as e:
            raise IndexDemandIncorrect()
        self.__orderingDictDemand()


    def lockingRoute( self, nodeBegin, nodeEnd ):
        self.__graph.remove_edge(nodeBegin, nodeEnd)

    def unlockingRoute(self, nodeBegin, nodeEnd ):
        timeTravel = self.__map[nodeBegin][nodeEnd]['weight']
        self.__graph.add_edge( nodeBegin, nodeEnd, weight=timeTravel )

    def __repr__(self):
        cad = f'{"Admid Agency" :_^40}\n\n'
        for bus in self.__listBuses:
            cad += bus.__repr__()

        cad += f'{"routes map for the graph" :_^40}\n\n'
        for route in list(self.__map.edges.data()):
            begin = route[0]
            end = route[1]
            timeT = route[2]['weight']
            cad += f'{begin: <4}--{end: >4}, with timeTravel of {timeT} hours \n'

        return cad
        



