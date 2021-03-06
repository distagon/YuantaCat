#-*- coding: utf-8 -*-

from yuantacat.analyzer.profitability_analyzer import ProfitabilityAnalyzer
from yuantacat.report.data_creator import DataCreator

class ProfitabilityDataCreator():
    def __init__(self):
        self.data_creator = DataCreator()

    def create(self, param):
        create_param = {
            'stock_symbol' : param['stock_symbol'], 
            'data' : self.__build_data_param(param),
            'category_field' : 'date',
            'base_path' : self.__build_base_path(param),
        }
        return self.data_creator.create(create_param)

    def __build_data_param(self, param):
        analyzer = ProfitabilityAnalyzer(stock_symbol=param['stock_symbol'], period=param['period'])
        gross_profit_margin = analyzer.get_gross_profit_margin().get()
        operating_profit_margin = analyzer.get_operating_profit_margin().get()
        net_profit_before_tax_margin = analyzer.get_net_profit_before_tax_margin().get()
        net_profit_margin = analyzer.get_net_profit_margin().get()

        # Cash Conversion Cycle (CCC)
        dio = analyzer.get_dio().get()
        dso = analyzer.get_dso().get()
        dpo = analyzer.get_dpo().get()
        ccc = analyzer.get_cash_conversion_cycle().get()

        return {
            'gross_profit_margin' : { 
                'value' : gross_profit_margin,
                'format' : 'percentage',
            },
            'operating_profit_margin' : {
                'value' : operating_profit_margin,
                'format' : 'percentage',
            },
            'net_profit_before_tax_margin' : {
                'value' : net_profit_before_tax_margin,
                'format' : 'percentage',
            },
            'net_profit_margin' : {
                'value' : net_profit_margin,
                'format' : 'percentage',
            },
            'dio' : {
                'value' : dio,
                'format' : 'float',
            },
            'dso' : {
                'value' : dso,
                'format' : 'float',
            },
            'dpo' : {
                'value' : dpo,
                'format' : 'float',
            },
            'ccc' : {
                'value' : ccc,
                'format' : 'float',
            },
        }

    def __build_base_path(self, param):
        if param['period'] == 'Y':
            return './report/chart/data/profitability/yearly/'
        elif param['period'] == 'Q':
            return './report/chart/data/profitability/quarterly/'
