#-*- coding: utf-8 -*-

from yuantacat.dao.balance_sheet_dao import BalanceSheetDao
from yuantacat.assembler.financial_statement_assembler import FinancialStatementAssembler

class BalanceSheetQuarterlyAssembler():
    def assemble(self, param):
        assembler = FinancialStatementAssembler('quarterly')
        dao = assembler.assemble(param)
        return BalanceSheetDao(dao['column_name_list'], dao['row_list'], dao['stock_symbol'])

class BalanceSheetYearlyAssembler():
    def assemble(self, param):
        assembler = FinancialStatementAssembler('yearly')
        dao = assembler.assemble(param)
        return BalanceSheetDao(dao['column_name_list'], dao['row_list'], dao['stock_symbol'])
