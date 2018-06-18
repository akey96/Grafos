#!/usr/bin/python3
# coding: utf-8
import networkx as nx
from project.controller.exception import CapacityNotAllowed, IndexDemandIncorrect
from functools import total_ordering
from copy import deepcopy
from collections import OrderedDict


class RouteBus():
    def __init__(self, route, timeOfDeparture, timeOfArrival):
        self.__route = route
        self.__timeOfDeparture = timeOfDeparture
        self.__timeOfArrival = timeOfArrival
    def getRoute(self):
        return self.__route
    def getTimeOfDeparture(self):
        return self.__timeOfDeparture
    def getTimeOfArrival(self):
        return self.__timeOfArrival

    def __repr__(self):
        cad = f'{"": ^4}{"Route Bus":-^30}\n'
        cad += f'{"": ^4}{"route": <10} : {self.__route} \n'
        cad += f'{"": ^4}{"timeOfDeparture": <10} : {self.__timeOfDeparture} \n'
        cad += f'{"": ^4}{"timeOfArrival": <10} : {self.__timeOfArrival} \n\n'
        return cad

@total_ordering
class Bus():
    capacity = 50
    hourStart = 6
    hoursWork = 20
    cont = -1

    def __init__( self,  position ):
        Bus.cont += 1
        self.__numberBus = Bus.cont
        self.__numberPassenger = 0
        self.__position = position
        self.__hoursWork = 20
        self.__listOfRoutesBus = []

    def addRouteToListRoutesBuses(self, routeBus):
        self.__listOfRoutesBus.append(routeBus)
    def getListRoutesBuses(self):
        return self.__listOfRoutesBus

    def getHoursWork(self):
        return self.__hoursWork

    def subHoursWork(self, n ):
        self.__hoursWork -= n

    def getNumberBus(self):
        return self.__numberBus

    @staticmethod
    def getCapacity():
        return Bus.capacity


    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getNumberPassenger(self):
        return self.__numberPassenger

    def addPassenger(self, n ):
        if self.__numberPassenger + n > Bus.capacity:
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
        cad += f'{"capacity": <10} : {Bus.capacity} \n'
        cad += f'{"position": <10} : {self.__position} \n'
        cad += f'{"numberPassenger": <10} : {self.__numberPassenger} \n'
        cad += f'{"hoursWork": <10} : {self.__hoursWork} \n'
        cad += f'{"listOfRoutesBus": <10} : \n'
        for routeBus in self.__listOfRoutesBus:
            cad += f'{routeBus.__repr__()} \n'
        cad+="\n"
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

    def __costeRoute(self, route):
        coste = 0
        for i in range(1,len(route)):
            begin = route[i-1]
            end = route[i]
            coste += self.__graph[begin][end]['weight']
        return coste

    def __busFree(self, costeRoute, beginBus):
        index = -1
        for i in range(len(self.__listBuses)):
            if self.__listBuses[i].getHoursWork() >= costeRoute and self.__listBuses[i].getPosition() == beginBus:
                index = i
                break
        return index

    def __asingBus(self, costeRoute, indexBus, updateLocation, route):
        #if route == [ 'LPZ','ORU']:
        #    print("entro ",self.__listBuses[indexBus] )
        timeOfDeparture =(Bus.hourStart + Bus.hoursWork) - self.__listBuses[indexBus].getHoursWork()
        timeOfArrival = timeOfDeparture + costeRoute
        routeBus = RouteBus(route,timeOfDeparture, timeOfArrival)
        self.__listBuses[indexBus].addRouteToListRoutesBuses(routeBus)
        self.__listBuses[indexBus].subHoursWork(costeRoute)
        self.__listBuses[indexBus].setPosition(updateLocation)


    def routeDirect(self):
        #caminos = []
        for begin in self.__dicDemandsForDay.keys():
            for end in self.__dicDemandsForDay[begin].keys():
                while self.__dicDemandsForDay[begin][end] >=  Bus.getCapacity():
                    route = nx.dijkstra_path(self.__graph, begin, end)
                    #caminos.append(route)
                    costeRoute = self.__costeRoute(route)
                    indexBus = self.__busFree(costeRoute, begin)

                    if indexBus != -1:
                        self.__asingBus( costeRoute,indexBus,end, route)
                        self.__dicDemandsForDay[begin][end] -= Bus.getCapacity()
                    else:
                        break
        self.__orderingDictDemand()
        #return caminos

    def routePartital(self):

        """
        inicio = locataionBus
        fin = maoyor de demadnda[inicio]
        while capacidad sea numpasa < capacidad
            ## agarrar el mayor numero de pasajero posible
            # mientras las horas de trabajp sea menor a 20
            inicio = fin
            fin = maoyor de demadnda[inicio]

        """

        caminos = []
        for begin in self.__dicDemandsForDay.keys():
            pass
            #print( begin,  self.__dicDemandsForDay[begin] )
            #for end in self.__dicDemandsForDay[begin].keys():

    def assignRoutesToAllBuses(self):
        self.routeDirect()

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

