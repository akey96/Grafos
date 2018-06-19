#!/usr/bin/python3
# coding: utf-8


from functools import total_ordering
from project.controller.exception import CapacityNotAllowed



@total_ordering
class Bus():
    capacity = 50
    hourStart = 6
    hoursWork = 20
    cont = -1

    def __init__( self,  position ):
        Bus.cont += 1
        self.__numberBus = Bus.cont
        self.__free_seats = Bus.capacity
        self.__position = position
        self.__hoursWork = Bus.hoursWork
        self.__listOfRoutesBus = []

    def getNumberBus(self):
        return self.__numberBus

    def addRouteToListRoutesBuses(self, routeBus):
        self.__listOfRoutesBus.append(routeBus)

    def getListRoutesBuses(self):
        return self.__listOfRoutesBus

    def getHoursWork(self):
        return self.__hoursWork

    def subHoursWork(self, n ):
        self.__hoursWork -= n

    def getFree_seatss(self):
        return self.__numberBus

    @staticmethod
    def getCapacity():
        return Bus.capacity


    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getFree_seats(self):
        return self.__free_seats

    def removePassengerOfBus(self, n):
        if self.__free_seats + n > Bus.capacity:
            raise CapacityNotAllowed()
        self.__free_seats += n

    def addPassengerToBus(self, n):
        if self.__free_seats-n < 0:
            raise CapacityNotAllowed()
        self.__free_seats -= n


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
        cad += f'{"free_seats": <10} : {self.__free_seats} \n'
        cad += f'{"hoursWork": <10} : {self.__hoursWork} \n'
        cad += f'{"listOfRoutesBus": <10} : \n'
        for routeBus in self.__listOfRoutesBus:
            cad += f'{routeBus.__repr__()} \n'
        return cad