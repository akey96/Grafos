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
    admin.addDemand2('LPZ', 'ORU', 90)
    admin.addDemand2('LPZ', 'PT', 45)
    admin.addDemand2('LPZ', 'CBA', 50)
    admin.addDemand2('LPZ', 'CHQ', 30)
    admin.addDemand2('LPZ', 'SCZ', 40)
    admin.addDemand2('LPZ', 'TJA', 30)

    admin.addDemand2('ORU', 'LPZ', 75)
    admin.addDemand2('ORU', 'PT', 28)
    admin.addDemand2('ORU', 'CBA', 45)
    admin.addDemand2('ORU', 'CHQ', 20)
    admin.addDemand2('ORU', 'TJA', 40)
    admin.addDemand2('ORU', 'SCZ', 70)

    admin.addDemand2('CBA', 'SCZ', 60)
    admin.addDemand2('CBA', 'TJA', 45)
    admin.addDemand2('CBA', 'CHQ', 50)
    admin.addDemand2('CBA', 'PT', 30)
    admin.addDemand2('CBA', 'ORU', 30)
    admin.addDemand2('CBA', 'LPZ', 30)

    admin.addDemand2('SCZ', 'LPZ', 30)
    admin.addDemand2('SCZ', 'CBA', 75)
    admin.addDemand2('SCZ', 'ORU', 20)
    admin.addDemand2('SCZ', 'PT', 20)
    admin.addDemand2('SCZ', 'CHQ', 40)
    admin.addDemand2('SCZ', 'TJA', 65)

    admin.addDemand2('PT', 'TJA', 20)
    admin.addDemand2('PT', 'CHQ', 15)
    admin.addDemand2('PT', 'ORU', 35)
    admin.addDemand2('PT', 'LPZ', 50)
    admin.addDemand2('PT', 'CBA', 30)
    admin.addDemand2('PT', 'SCZ', 20)

    admin.addDemand2('CHQ', 'SCZ', 40)
    admin.addDemand2('CHQ', 'CBA', 20)
    admin.addDemand2('CHQ', 'TJA', 100)
    admin.addDemand2('CHQ', 'PT', 40)
    admin.addDemand2('CHQ', 'ORU', 10)
    admin.addDemand2('CHQ', 'LPZ', 30)

    admin.addDemand2('TJA', 'LPZ', 40)
    admin.addDemand2('TJA', 'ORU', 20)
    admin.addDemand2('TJA', 'PT', 30)
    admin.addDemand2('TJA', 'CBA', 90)
    admin.addDemand2('TJA', 'CHQ', 40)
    admin.addDemand2('TJA', 'SCZ', 60)

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

    print(f'{"buses":=^40}\n')
    for bus in admin.getListBuses():
        print(bus)