
#!/usr/bin/python3
# coding: utf-8

import unittest


from project.controller.graph import AdminAgency, Bus
from project.controller.exception import CapacityNotAllowed, IndexDemandIncorrect
import networkx as nx

class TestBus(unittest.TestCase):

    def setUp(self):
        self.bus1 = Bus(1,50,False,"CBA")

    def test_01_overflow_bus(self):
        self.assertRaises(CapacityNotAllowed , self.bus1.addPassenger , 100)

    def test_02_overflow_bus(self):
        self.assertRaises(CapacityNotAllowed , self.bus1.subsPassenger, 100)


class TestAdminAgency( unittest.TestCase ):

    def setUp(self):
        self.map = AdminAgency()
        self.map.addRoot('LPZ', 'ORU', 3)
        self.map.addRoot('ORU', 'PT', 5)
        self.map.addRoot('ORU', 'CBA', 4)
        self.map.addRoot('PT', 'CHQ', 3)
        self.map.addRoot('PT', 'TJA', 4)
        self.map.addRoot('TJA', 'CHQ', 3)
        self.map.addRoot('TJA', 'SCZ', 8)
        self.map.addRoot('SCZ', 'CBA', 5)

        self.map.addBus(Bus(1, 50, False, 'CBA'))
        self.map.addBus(Bus(3, 50, False, 'CBA'))
        self.map.addBus(Bus(2, 50, False, 'CBA'))
        self.map.addBus(Bus(4, 50, False, 'CBA'))
        self.map.addBus(Bus(5, 30, True, 'CBA'))
        self.map.addBus(Bus(6, 30, True, 'CBA'))
        self.map.addBus(Bus(7, 30, True, 'CBA'))
        self.map.addBus(Bus(8, 30, True, 'CBA'))


        self.map.addDemand('LPZ', 'ORU', 50 )
        self.map.addDemand('LPZ', 'PT', 24 )
        self.map.addDemand('LPZ', 'CBA', 70 )
        self.map.addDemand('LPZ', 'CHQ', 35 )
        self.map.addDemand('LPZ', 'SCZ', 67 )
        self.map.addDemand('LPZ', 'TJA', 34 )



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

    def test_04_is_root_where_locking(self):
        self.map.lockingRoot('LPZ', 'ORU')
        edges = [('ORU', 'PT', {'weight': 5}),
                 ('ORU', 'CBA', {'weight': 4}),
                 ('PT', 'CHQ', {'weight': 3}),
                 ('PT', 'TJA', {'weight': 4}),
                 ('CBA', 'SCZ', {'weight': 5}),
                 ('CHQ', 'TJA', {'weight': 3}),
                 ('TJA', 'SCZ', {'weight': 8})]
        self.assertEqual(list(self.map.getGraph().edges.data()), edges)

    def test_05_is_root_where_unlocking(self):

        edges = [('LPZ', 'ORU', {'weight': 3}),
                 ('ORU', 'PT', {'weight': 5}),
                 ('ORU', 'CBA', {'weight': 4}),
                 ('PT', 'CHQ', {'weight': 3}),
                 ('PT', 'TJA', {'weight': 4}),
                 ('CBA', 'SCZ', {'weight': 5}),
                 ('CHQ', 'TJA', {'weight': 3})]
        self.map.lockingRoot('LPZ', 'ORU')
        self.map.lockingRoot('TJA', 'SCZ')
        self.map.unlockingRoot('LPZ', 'ORU')
        self.assertEqual(list(self.map.getGraph().edges.data()), edges)

    def test_06_is_add_all_buses(self):
        self.assertEqual( len(self.map.getListBuses()), 8 )



    def test_07_is_addDemand_correct(self):

        self.assertEqual(self.map.getLisDemandForDay()['LPZ']['ORU'], 50)
        self.assertEqual(self.map.getLisDemandForDay()['LPZ']['PT'], 24)
        self.assertEqual(self.map.getLisDemandForDay()['LPZ']['CBA'], 70)
        self.assertEqual(self.map.getLisDemandForDay()['LPZ']['CHQ'], 35)
        self.assertEqual(self.map.getLisDemandForDay()['LPZ']['SCZ'], 67)
        self.assertEqual(self.map.getLisDemandForDay()['LPZ']['TJA'], 34)

    def test_08_is_all_Demand_were_add(self):
        self.assertEqual( self.map.lenDemand(),6 )

    def test_09(self):

        self.assertRaises(IndexDemandIncorrect, self.map.setDemand, 'sad', 'asd', 456 )



if __name__ == "__main__":
    unittest.main()