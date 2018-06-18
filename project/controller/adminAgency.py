#!/usr/bin/python3
# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
import networkx as nx
from project.controller.bus import Bus
from project.controller.routeBus import RouteBus
import matplotlib.pyplot as plt

class AdminAgency():
    
    def __init__(self):
        self.__listBuses = []

        self.__map = nx.Graph()
        self.__graph = None
        self.__graphDemand = nx.MultiDiGraph()

    def getGraphDemand(self):
        return self.__graphDemand

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


    def addRoute(self, nodeBegin, nodeEnd, timeTravel ):
        self.__map.add_edge( nodeBegin, nodeEnd, weight=timeTravel )
        self.__graph = deepcopy( self.__map )


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
        timeOfDeparture = (Bus.hourStart + Bus.hoursWork) - self.__listBuses[indexBus].getHoursWork()
        timeOfArrival = timeOfDeparture + costeRoute
        routeBus = RouteBus(route, timeOfDeparture, timeOfArrival)
        self.__listBuses[indexBus].addRouteToListRoutesBuses(routeBus)
        self.__listBuses[indexBus].subHoursWork(costeRoute)
        self.__listBuses[indexBus].setPosition(updateLocation)


    def routePartital(self):
        for begin in self.__dicDemandsForDay.keys():
            for end in self.__dicDemandsForDay[begin].keys():
                self.__hayarRoutaMasLarga(begin,end)
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


    def lockingRoute( self, nodeBegin, nodeEnd ):
        self.__graph.remove_edge(nodeBegin, nodeEnd)

    def unlockingRoute(self, nodeBegin, nodeEnd ):
        timeTravel = self.__map[nodeBegin][nodeEnd]['weight']
        self.__graph.add_edge( nodeBegin, nodeEnd, weight=timeTravel )



    # ============================== 2da parte

    def __costeRoute2(self, route):
        coste = 0
        for i in range(1,len(route)):
            begin = route[i-1]
            end = route[i]
            coste += self.__graphDemand[begin][end][0]['weight']
        return coste


    def routeDirect2(self):
        for indexBus in range(len(self.__listBuses)):
            invalid = False
            while not invalid :
                pathsOfDemands = nx.single_source_dijkstra_path(self.__graphDemand, self.__listBuses[indexBus].getPosition(), weight=Bus.getCapacity())
                pathsOfDemands = list(pathsOfDemands.values())

                for routeDemand in sorted(pathsOfDemands[1:], key=lambda x : len(x)):
                    costeRouteDemand = self.__costeRoute2(routeDemand)
                    if costeRouteDemand >= Bus.getCapacity():
                        costeRouteGraph = 0
                        routeFinalGraph = []
                        for i in range(1, len(routeDemand)):
                            routeGraph = nx.dijkstra_path(self.__graph, routeDemand[i-1], routeDemand[i])
                            costeRouteGraph += self.__costeRoute(routeGraph)
                            routeFinalGraph.extend(routeGraph) if routeFinalGraph == [] else routeFinalGraph.extend(routeGraph[1:])
                        if costeRouteGraph > self.__listBuses[indexBus].getHoursWork():
                            invalid = True
                        else:
                            self.__asingBus(costeRouteGraph, self.__listBuses[indexBus].getNumberBus(), routeFinalGraph[-1], routeFinalGraph)
                            self.__graphDemand[routeDemand[0]][routeDemand[-1]][0]['weight'] -= self.__listBuses[indexBus].getCapacity()
                        break
                    else:
                        invalid = True

    def __getVecinosOfNode(self, node):
        vecinos = list(self.__graphDemand.neighbors(node))
        valores = {}
        for i in vecinos:
            k = self.__graphDemand[node][i][0]['weight']
            if k > 0:
                valores[i] = k
        valores = OrderedDict(sorted(valores.items(), key=lambda t: t[1], reverse=True))
        return  valores



    def routePartital2(self):
        for indexBus in range(len(self.__listBuses)):
            listadePosiblesRutas = []
            horasTotales = 0

            datos = self.__getARouteBus(indexBus)
            horasTotales += datos[2]
            while self.__listBuses[indexBus].getHoursWork() >= horasTotales:
                self.__asingBus(datos[2], datos[0], datos[3][-1], datos[3])
                #print(datos[4],datos[3][-1])
                self.__graphDemand[datos[4]][datos[3][-1]][0]['weight'] -= datos[1]
                datos = self.__getARouteBus(indexBus)
                horasTotales += datos[2]


            #pathsOfDemands = [ element for element in pathsOfDemands if self.__costeRoute2(element) >0 ]
            #pathsOfDemands = sorted(pathsOfDemands, key=lambda x: self.__costeRoute2(x), reverse=True)

            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def __getARouteBus(self, indexBus):
        DemandsAdjOfBus = self.__getVecinosOfNode(self.__listBuses[indexBus].getPosition())
        routeGraphFinal = []
        costeGraphFinal = 0
        costeDemandFinal = 0
        for sigDemandAdj, sigCosteAdj in DemandsAdjOfBus.items():
            route = nx.dijkstra_path(self.__graph, self.__listBuses[indexBus].getPosition(), sigDemandAdj)
            costeRouteGraph = self.__costeRoute(route)
            if self.__listBuses[indexBus].getNumberPassenger() >= DemandsAdjOfBus[sigDemandAdj] and self.__listBuses[
                indexBus].getHoursWork() >= costeRouteGraph:
                if costeRouteGraph > costeGraphFinal:
                    routeGraphFinal = route
                    costeGraphFinal = costeRouteGraph
                    costeDemandFinal = sigCosteAdj
        return (indexBus,costeDemandFinal, costeGraphFinal, routeGraphFinal, self.__listBuses[indexBus].getPosition()  )


    def addDemand2(self,nodeBegin, nodeEnd, demandPassenger ):
        self.__graphDemand.add_edge(nodeBegin, nodeEnd, weight=demandPassenger)

    def assignRoutesToAllBuses2(self):
        self.routeDirect2()
        self.routePartital2()



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

