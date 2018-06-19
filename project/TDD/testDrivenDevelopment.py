
#!/usr/bin/python3
# coding: utf-8

import unittest


from project.controller.adminAgency import AdminAgency
from project.controller.bus import Bus
from project.controller.exception import CapacityNotAllowed, IndexDemandIncorrect
import networkx as nx

class TestBus(unittest.TestCase):

    def setUp(self):
        self.bus1 = Bus(1,50,False,"CBA")

    def test_01_overflow_bus(self):
        self.assertRaises(CapacityNotAllowed, self.bus1.addPassengerToBus, 100)

    def test_02_overflow_bus(self):
        self.assertRaises(CapacityNotAllowed, self.bus1.removePassengerOfBus, 100)


class TestAdminAgency( unittest.TestCase ):

    def setUp(self):
        self.map = AdminAgency()
        self.map.addRoute('LPZ', 'ORU', 3)
        self.map.addRoute('ORU', 'PT', 5)
        self.map.addRoute('ORU', 'CBA', 4)
        self.map.addRoute('PT', 'CHQ', 3)
        self.map.addRoute('PT', 'TJA', 4)
        self.map.addRoute('TJA', 'CHQ', 3)
        self.map.addRoute('TJA', 'SCZ', 8)
        self.map.addRoute('SCZ', 'CBA', 5)

        self.map.addBus(Bus(1, 50, False, 'CBA'))
        self.map.addBus(Bus(3, 50, False, 'CBA'))
        self.map.addBus(Bus(2, 50, False, 'CBA'))
        self.map.addBus(Bus(4, 50, False, 'CBA'))
        self.map.addBus(Bus(5, 30, True, 'CBA'))
        self.map.addBus(Bus(6, 30, True, 'CBA'))
        self.map.addBus(Bus(7, 30, True, 'CBA'))
        self.map.addBus(Bus(8, 30, True, 'CBA'))


        self.map.addDemand('LPZ', 'ORU', 50 )
        self.map.addDemand('LPZ', 'PT',  24 )
        self.map.addDemand('LPZ', 'CBA', 70 )
        self.map.addDemand('LPZ', 'CHQ', 35 )
        self.map.addDemand('LPZ', 'SCZ', 67 )
        self.map.addDemand('LPZ', 'TJA', 34 )

        self.map.addDemand('ORU', 'LPZ', 75 )
        self.map.addDemand('ORU', 'PT',  100 )
        self.map.addDemand('ORU', 'CBA', 50 )
        self.map.addDemand('ORU', 'CHQ', 35 )
        self.map.addDemand('ORU', 'TJA', 85 )
        self.map.addDemand('ORU', 'SCZ', 105 )


    def test_01_is_graph_undirect(self):
        self.assertIsInstance(self.map.getMap(), nx.Graph )

    def test_02_map_have_nodes_correct(self):
        nodes = ['LPZ', 'ORU', 'PT', 'CBA', 'CHQ', 'TJA', 'SCZ']
        self.assertEqual(list( self.map.getMap().nodes ), nodes )

    def test_03_map_have_edges_correct(self):
        edges = [('LPZ', 'ORU', {'weight': 3}),
                 ('ORU', 'PT', {'weight': 5}),
                 ('ORU', 'CBA', {'weight': 4}),
                 ('PT', 'CHQ', {'weight': 3}),
                 ('PT', 'TJA', {'weight': 4}),
                 ('CBA', 'SCZ', {'weight': 5}),
                 ('CHQ', 'TJA', {'weight': 3}),
                 ('TJA', 'SCZ', {'weight': 8})]
        self.assertEqual( list(self.map.getMap().edges.data()), edges )

    def test_04_is_route_where_locking(self):
        self.map.lockingRoute('LPZ', 'ORU')
        edges = [('ORU', 'PT', {'weight': 5}),
                 ('ORU', 'CBA', {'weight': 4}),
                 ('PT', 'CHQ', {'weight': 3}),
                 ('PT', 'TJA', {'weight': 4}),
                 ('CBA', 'SCZ', {'weight': 5}),
                 ('CHQ', 'TJA', {'weight': 3}),
                 ('TJA', 'SCZ', {'weight': 8})]
        self.assertEqual(list(self.map.getGraph().edges.data()), edges)

    def test_05_is_route_where_unlocking(self):

        edges = [('LPZ', 'ORU', {'weight': 3}),
                 ('ORU', 'PT', {'weight': 5}),
                 ('ORU', 'CBA', {'weight': 4}),
                 ('PT', 'CHQ', {'weight': 3}),
                 ('PT', 'TJA', {'weight': 4}),
                 ('CBA', 'SCZ', {'weight': 5}),
                 ('CHQ', 'TJA', {'weight': 3})]
        self.map.lockingRoute('LPZ', 'ORU')
        self.map.lockingRoute('TJA', 'SCZ')
        self.map.unlockingRoute('LPZ', 'ORU')
        self.assertEqual(list(self.map.getGraph().edges.data()), edges)

    def test_06_is_add_all_buses(self):
        self.assertEqual( len(self.map.getListBuses()), 8 )



    def test_07_addDemand_is_correct(self):
        dic = {'LPZ': {'CBA': 70, 'SCZ': 67, 'ORU': 50, 'CHQ': 35, 'TJA': 34, 'PT': 24},
               'ORU': {'SCZ': 105, 'PT': 100, 'TJA': 85, 'LPZ': 75, 'CBA': 50, 'CHQ': 35}
               }

        self.assertDictEqual(self.map.getDictDemandForDay(), dic)



    def test_08_setDemand_is_incorrect(self):
        self.assertRaises(IndexDemandIncorrect, self.map.setDemand, 'sad', 'asd', 456 )

    def test_09_setDemand_is_correct(self):
        dic = {'LPZ': {'CBA': 70, 'SCZ': 67, 'ORU': 50, 'CHQ': 35, 'TJA': 34, 'PT': 24},
               'ORU': {'CBA': 456, 'SCZ': 105, 'PT': 100, 'TJA': 85, 'LPZ': 75, 'CHQ': 35}
               }
        self.map.setDemand('ORU', 'CBA', 456)
        self.assertDictEqual(self.map.getDictDemandForDay(), dic)


if __name__ == "__main__":
    unittest.main()