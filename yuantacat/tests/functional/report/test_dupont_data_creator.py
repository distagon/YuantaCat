#-*- coding: utf-8 -*-

from yuantacat.report.dupont_data_creator import DupontDataCreator

import unittest

class DupontDataCreatorTest(unittest.TestCase):
    def test_create_1101(self):
        creator = DupontDataCreator()
        creator.create({ 
            'stock_symbol' : '1101',
            'period' : 'Y', 
        })
