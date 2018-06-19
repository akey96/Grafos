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

    def __hour(self, n):
        if n>9:
            return f'{n}:00 hrs'
        else:
            return f'0{n}:00 hrs'


    def __repr__(self):
        cad = f'{"": ^4}{"Route Bus":-^40}\n'
        cad += f'{"": ^4}{"route": <15} : {self.__route} \n'
        cad += f'{"": ^4}{"timeOfDeparture": <15} : {self.__hour(self.__timeOfDeparture)} \n'
        cad += f'{"": ^4}{"timeOfArrival": <15} : {self.__hour(self.__timeOfArrival)} \n'
        return cad