#!/usr/bin/python3
# coding: utf-8

from project.controller.graph import AdminAgency, Bus


if __name__ == "__main__":
    admin = AdminAgency()

    admin.addRoot('LPZ', 'ORU', 3)
    admin.addRoot('ORU', 'PT',  5)
    admin.addRoot('ORU', 'CBA', 4)
    admin.addRoot('PT',  'CHQ', 3)
    admin.addRoot('PT',  'TJA', 4)
    admin.addRoot('TJA', 'CHQ', 3)
    admin.addRoot('TJA', 'SCZ', 8)
    admin.addRoot('SCZ', 'CBA', 5)

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