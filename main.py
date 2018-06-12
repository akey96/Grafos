#!/usr/bin/python3
# coding: utf-8

from project.controller.graph import AdminAgency, Bus


if __name__ == "__main__":
    admin = AdminAgency()

    # Route defined for graph
    admin.addRoute('LPZ', 'ORU', 3)
    admin.addRoute('ORU', 'PT',  5)
    admin.addRoute('ORU', 'CBA', 4)
    admin.addRoute('PT',  'CHQ', 3)
    admin.addRoute('PT',  'TJA', 4)
    admin.addRoute('TJA', 'CHQ', 3)
    admin.addRoute('TJA', 'SCZ', 8)
    admin.addRoute('SCZ', 'CBA', 5)

    admin.addBus( Bus(1, 50, False, 'CBA') )
    admin.addBus( Bus(2, 50, False, 'CBA') )
    admin.addBus( Bus(3, 50, False, 'CBA') )
    admin.addBus( Bus(4, 50, False, 'CBA') )
    admin.addBus( Bus(5, 30, True, 'CBA') )
    admin.addBus( Bus(6, 30, True, 'CBA') )
    admin.addBus( Bus(8, 30, True, 'CBA') )
    admin.addBus( Bus(7, 30, True, 'CBA') )

    #print(admin.getListBuses())
    #print(list(admin.getMap().edges.data()))
    print(admin)