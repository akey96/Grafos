#!/usr/bin/python3
# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
import networkx as nx
from project.controller.bus import Bus
from project.controller.routeBus import RouteBus

class AdminAgency():
    
    def __init__(self):
        self.__listBuses = []

        self.__mapGraph = nx.Graph()
        self.__copyOfMapGraph = None
        self.__demandGraph = nx.MultiDiGraph()
        self.__copyOfDemandGraph = nx.MultiDiGraph()

    def getGraphDemand(self):
        return self.__copyOfDemandGraph

    def getMap(self):
        return self.__mapGraph

    def getGraph(self):
        return self.__copyOfMapGraph

    def getListBuses(self):
        return self.__listBuses

    def setGraph(self, graph):
        self.__copyOfMapGraph = graph

    def addBus(self, bus):
        self.__listBuses.append(bus)
        self.__listBuses = sorted(self.__listBuses)

    def addRoute(self, nodeBegin, nodeEnd, timeTravel ):
        self.__mapGraph.add_edge(nodeBegin, nodeEnd, weight=timeTravel)
        self.__copyOfMapGraph = deepcopy(self.__mapGraph)

    def addDemand(self, nodeBegin, nodeEnd, demandPassenger):
        self.__demandGraph.add_edge(nodeBegin, nodeEnd, weight=demandPassenger)
        self.__copyOfDemandGraph = deepcopy(self.__demandGraph)

    def __costeRouteOfGraphMap(self, route):
        coste = 0
        for i in range(1,len(route)):
            begin = route[i-1]
            end = route[i]
            coste += self.__copyOfMapGraph[begin][end]['weight']
        return coste

    def __costeRouteOfGraphDemand(self, route):
        coste = 0
        for i in range(1,len(route)):
            begin = route[i-1]
            end = route[i]
            coste += self.__copyOfDemandGraph[begin][end][0]['weight']
        return coste

    def lockingRoute( self, nodeBegin, nodeEnd ):
        self.__copyOfMapGraph.remove_edge(nodeBegin, nodeEnd)

    def unlockingRoute(self, nodeBegin, nodeEnd ):
        timeTravel = self.__mapGraph[nodeBegin][nodeEnd]['weight']
        self.__copyOfMapGraph.add_edge(nodeBegin, nodeEnd, weight=timeTravel)

    def __defineHours(self, timeOfDeparture ,costeRoute):
        hour = timeOfDeparture + costeRoute
        if hour >= 24 :
            return hour-24
        return hour


    def __asingRouteBus(self, costeRoute, indexBus, location, route):
        timeOfDeparture = (Bus.hourStart + Bus.hoursWork) - self.__listBuses[indexBus].getHoursWork()
        timeOfArrival = self.__defineHours(timeOfDeparture ,costeRoute)

        routeBus = RouteBus(route, timeOfDeparture, timeOfArrival)
        self.__listBuses[indexBus].addRouteToListRoutesBuses(routeBus)
        self.__listBuses[indexBus].subHoursWork(costeRoute)
        self.__listBuses[indexBus].setPosition(location)



    def __getNeighborsOfNodeDemand(self, node):
        neighbors = list(self.__copyOfDemandGraph.neighbors(node))
        dictOfNeighbors = {}
        for neighbor in neighbors:
            weight = self.__copyOfDemandGraph[node][neighbor][0]['weight']
            if weight > 0:
                dictOfNeighbors[neighbor] = weight
        dictOfNeighbors = OrderedDict(sorted(dictOfNeighbors.items(), key=lambda t: t[1], reverse=True))
        return  dictOfNeighbors


    def __getPossibleRouteOfBus(self, indexBus):
        DemandsAdjOfBus = self.__getNeighborsOfNodeDemand(self.__listBuses[indexBus].getPosition())
        routeGraphFinal = []
        costeGraphFinal = 0
        costeDemandFinal = 0
        copyBus = deepcopy(self.__listBuses[indexBus])
        #print(copyBus.getNumberBus())
        for sigDemandAdj, sigCosteAdj in DemandsAdjOfBus.items():
            route = nx.dijkstra_path(self.__copyOfMapGraph,  self.__listBuses[indexBus].getPosition(), sigDemandAdj)
            costeRouteGraph = self.__costeRouteOfGraphMap(route)

            if self.__listBuses[indexBus].getFree_seats() >= DemandsAdjOfBus[sigDemandAdj] and self.__listBuses[indexBus].getHoursWork() >= costeRouteGraph:
                if costeRouteGraph > costeGraphFinal:
                    #print(copyBus.getFree_seats())
                    routeGraphFinal = route
                    costeGraphFinal = costeRouteGraph
                    costeDemandFinal = sigCosteAdj
        return (costeDemandFinal, costeGraphFinal, routeGraphFinal, self.__listBuses[indexBus].getPosition()  )


    def __defineDirectRoutesToBuses(self):
        for indexBus in range(len(self.__listBuses)):
            invalid = False
            while not invalid :
                pathsOfDemands = nx.single_source_dijkstra_path(self.__copyOfDemandGraph, self.__listBuses[indexBus].getPosition(), weight=Bus.getCapacity())
                pathsOfDemands = list(pathsOfDemands.values())

                for routeDemand in sorted(pathsOfDemands[1:], key=lambda x : len(x)):
                    costeRouteDemand = self.__costeRouteOfGraphDemand(routeDemand)
                    if costeRouteDemand >= Bus.getCapacity():
                        costeRouteGraph = 0
                        routeFinalGraph = []
                        for i in range(1, len(routeDemand)):
                            routeGraph = nx.dijkstra_path(self.__copyOfMapGraph, routeDemand[i - 1], routeDemand[i])
                            costeRouteGraph += self.__costeRouteOfGraphMap(routeGraph)
                            routeFinalGraph.extend(routeGraph) if routeFinalGraph == [] else routeFinalGraph.extend(routeGraph[1:])
                        if costeRouteGraph > self.__listBuses[indexBus].getHoursWork():
                            invalid = True
                        else:
                            self.__asingRouteBus(costeRouteGraph, self.__listBuses[indexBus].getNumberBus(), routeFinalGraph[-1], routeFinalGraph)
                            self.__copyOfDemandGraph[routeDemand[0]][routeDemand[-1]][0]['weight'] -= self.__listBuses[indexBus].getCapacity()
                        break
                    else:
                        invalid = True


    def __definePartitalRoutesToBuses(self):
        for indexBus in range(len(self.__listBuses)):
            datasPossibleRouteBus = self.__getPossibleRouteOfBus(indexBus)
            hoursWorksOfPossibleRoute = datasPossibleRouteBus[1]
            numberOfBus = self.__listBuses[indexBus].getNumberBus()
            locationOfPossibleRouteBus = datasPossibleRouteBus[2][-1]
            possibleRoute = datasPossibleRouteBus[2]

            self.__asingRouteBus(hoursWorksOfPossibleRoute, numberOfBus, locationOfPossibleRouteBus, possibleRoute )
            self.__copyOfDemandGraph[datasPossibleRouteBus[3]][datasPossibleRouteBus[2][-1]][0]['weight'] -= datasPossibleRouteBus[0]


    def assignRoutesToAllBuses2(self):
        self.__defineDirectRoutesToBuses()
        self.__definePartitalRoutesToBuses()



    def __repr__(self):
        cad = f'{"Admid Agency" :_^40}\n\n'
        for bus in self.__listBuses:
            cad += bus.__repr__()

        cad += f'{"routes map for the graph" :_^40}\n\n'
        for route in list(self.__mapGraph.edges.data()):
            begin = route[0]
            end = route[1]
            timeT = route[2]['weight']
            cad += f'{begin: <4}--{end: >4}, with timeTravel of {timeT} hours \n'

        return cad

