#!/usr/bin/python3
# coding: utf-8

class CapacityNotAllowed(Exception):
    
    def __init__(self):
        super(CapacityNotAllowed, self).__init__()


    def __repr__(self):
        return f'TypeError: Capacity of graph not allowed'


class IndexDemandIncorrect(Exception):

    def __init__(self):
        super(IndexDemandIncorrect, self).__init__()

    def __repr__(self):
        return f'TypeError: IndexDemandIncorrect of list DemandForDay'