#!/usr/bin/python3
# coding: utf-8

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
        cad += f'{"": ^4}{"timeOfArrival": <10} : {self.__timeOfArrival} \n'
        return cad