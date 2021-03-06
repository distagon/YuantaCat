#-*- coding: utf-8 -*-

import psycopg2

class PostgresGetCommnad():
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.operation_map = {
            'StockSymbolList' : "select stock_symbol, listing_date, market_category from stock_symbol where release_date in (select max(release_date) from stock_symbol) and cfi_code = 'ESVUFR'",
            'CapitalIncreaseByCash' : u"select release_date, stmt_date, value from capital_increase_history where stock_symbol = %(stock_symbol)s and account = '現金增資'",
            'CapitalIncreaseByEarnings' : u"select release_date, stmt_date, value from capital_increase_history where stock_symbol = %(stock_symbol)s and account = '盈餘轉增資'",
            'CapitalIncreaseBySurplus' : u"select release_date, stmt_date, value from capital_increase_history where stock_symbol = %(stock_symbol)s and account = '公積及其他'",
            'NetProfit' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '經常利益'",
            'Assets' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '資產總額'",
            'Liabilities' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '負債總額'",
            'Equity' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '股東權益總額'",
            'CurrentAssets' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '流動資產'",
            'CurrentLiabilities' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '流動負債'",
            'Inventories' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '存貨'",
            'PrepaidAccounts' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '預付費用及預付款'",
            'CostOfGoodsSold' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '營業成本'",
            'Sales' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '營業收入淨額'",
            'AccountsReceivable' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '應收帳款及票據'",
            'AccountsPayable' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '應付帳款及票據'",
            'CashFlowFromOperatingActivities' : u"select release_date, stmt_date, value from cash_flow where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '來自營運之現金流量'",
            'CashFlowFromInvestingActivities' : u"select release_date, stmt_date, value from cash_flow where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '投資活動之現金流量'",
            'CashFlowFromFinancingActivities' : u"select release_date, stmt_date, value from cash_flow where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '理財活動之現金流量'",
            'OperatingRevenue' : u"select release_date, stmt_date, value from operating_revenue where stock_symbol = %(stock_symbol)s and account = '合併營收'",
            'LongTermLiabilities' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '長期負債'",
            'FixedAssets' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '固定資產'",
            'IncomeBeforeTax' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '稅前淨利'",
            'InterestExpense' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '利息支出'",
            'SellingExpenses' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '營業費用─推銷費用'",
            'AdministrativeExpenses' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '營業費用─管理費用'",
            'GrossProfit' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '營業毛利'",
            'OperatingProfit' : u"select release_date, stmt_date, value from income_statement where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '營業利益'",
            'ShortTermDebt' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '短期借款'",
            'LongTermInvestments' : u"select release_date, stmt_date, value from balance_sheet where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '長期投資'",
            'CashDividends' : u"select release_date, stmt_date, value from dividend_policy where stock_symbol = %(stock_symbol)s and account = '現金股利'",
            'StockDividendsFromRetainedEarnings' : u"select release_date, stmt_date, value from dividend_policy where stock_symbol = %(stock_symbol)s and account = '盈餘配股'",
            'StockDividendsFromCapitalReserve' : u"select release_date, stmt_date, value from dividend_policy where stock_symbol = %(stock_symbol)s and account = '公積配股'",
            'EmployeeStockBonusRatio' : u"select release_date, stmt_date, value from dividend_policy where stock_symbol = %(stock_symbol)s and account = '員工配股率'",
            'StockPrice' : u"select release_date, stmt_date, value from stock_price where stock_symbol = %(stock_symbol)s and account = 'Close'",
            'BookValue' : u"select release_date, stmt_date, value from financial_analysis where stock_symbol = %(stock_symbol)s and period = %(period)s and account = '每股淨值(元)'",
        }

    def get(self, operation, param):
        connection = psycopg2.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute(self.operation_map[operation], param)
        records = cursor.fetchall()
        connection.commit()
        connection.close()
        return records
