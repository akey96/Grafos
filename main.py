#!/usr/bin/python3
# coding: utf-8

from project.controller.adminAgency import AdminAgency
from project.controller.bus import Bus


if __name__ == "__main__":
    admin = AdminAgency()

    admin.addRoute('LPZ', 'ORU', 3)
    admin.addRoute('ORU', 'PT', 5)
    admin.addRoute('ORU', 'CBA', 4)
    admin.addRoute('PT', 'CHQ', 3)
    admin.addRoute('PT', 'TJA', 7)
    admin.addRoute('TJA', 'CHQ', 3)
    admin.addRoute('TJA', 'SCZ', 8)
    admin.addRoute('SCZ', 'CBA', 5)

    admin.addBus(Bus('LPZ'))
    admin.addBus(Bus('ORU'))
    admin.addBus(Bus('PT'))
    admin.addBus(Bus('CHQ'))
    admin.addBus(Bus('CHQ'))
    admin.addBus(Bus('TJA'))
    admin.addBus(Bus('TJA'))
    admin.addBus(Bus('CBA'))
    admin.addBus(Bus('CBA'))
    admin.addBus(Bus('SCZ'))

    # ============================
    admin.addDemand('LPZ', 'ORU', 90)
    admin.addDemand('LPZ', 'PT', 45)
    admin.addDemand('LPZ', 'CBA', 50)
    admin.addDemand('LPZ', 'CHQ', 30)
    admin.addDemand('LPZ', 'SCZ', 40)
    admin.addDemand('LPZ', 'TJA', 30)

    admin.addDemand('ORU', 'LPZ', 75)
    admin.addDemand('ORU', 'PT', 28)
    admin.addDemand('ORU', 'CBA', 45)
    admin.addDemand('ORU', 'CHQ', 20)
    admin.addDemand('ORU', 'TJA', 40)
    admin.addDemand('ORU', 'SCZ', 70)

    admin.addDemand('CBA', 'SCZ', 60)
    admin.addDemand('CBA', 'TJA', 45)
    admin.addDemand('CBA', 'CHQ', 50)
    admin.addDemand('CBA', 'PT', 30)
    admin.addDemand('CBA', 'ORU', 30)
    admin.addDemand('CBA', 'LPZ', 30)

    admin.addDemand('SCZ', 'LPZ', 30)
    admin.addDemand('SCZ', 'CBA', 75)
    admin.addDemand('SCZ', 'ORU', 20)
    admin.addDemand('SCZ', 'PT', 20)
    admin.addDemand('SCZ', 'CHQ', 40)
    admin.addDemand('SCZ', 'TJA', 65)

    admin.addDemand('PT', 'TJA', 20)
    admin.addDemand('PT', 'CHQ', 15)
    admin.addDemand('PT', 'ORU', 35)
    admin.addDemand('PT', 'LPZ', 50)
    admin.addDemand('PT', 'CBA', 30)
    admin.addDemand('PT', 'SCZ', 20)

    admin.addDemand('CHQ', 'SCZ', 40)
    admin.addDemand('CHQ', 'CBA', 20)
    admin.addDemand('CHQ', 'TJA', 100)
    admin.addDemand('CHQ', 'PT', 40)
    admin.addDemand('CHQ', 'ORU', 10)
    admin.addDemand('CHQ', 'LPZ', 30)

    admin.addDemand('TJA', 'LPZ', 40)
    admin.addDemand('TJA', 'ORU', 20)
    admin.addDemand('TJA', 'PT', 30)
    admin.addDemand('TJA', 'CBA', 90)
    admin.addDemand('TJA', 'CHQ', 40)
    admin.addDemand('TJA', 'SCZ', 60)

    print(f'{"demanda inicial":=^40}\n')
    dic = admin.getGraphDemand()
    for demand in dic.edges.data():
        print(demand)

    print(f'{"":-^40}')
    admin.assignRoutesToAllBuses2()
    print(f'{"":-^40}')

    print(f'{"rutas demandas modificas":=^40}\n')
    dic = admin.getGraphDemand()
    for demand in dic.edges.data():
        print(demand)

    #print(f'{"buses":=^40}\n')
    #for bus in admin.getListBuses():
    #    print(bus)
    print(admin)