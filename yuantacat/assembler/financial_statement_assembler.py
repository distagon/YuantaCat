#-*- coding: utf-8 -*-

from yuantacat.assembler.content_screener import ContentScreener
from yuantacat.common.string_utils import StringUtils
from yuantacat.common.lxml_utils import LxmlUtils

import lxml.html

class FinancialStatementAssembler():
    def __init__(self, base_xpath_param, column_name_pos=0):
        self.base_xpath = self.__init_base_xpath(base_xpath_param)
        self.column_name_pos = column_name_pos
        self.content_screener = ContentScreener()
        self.string_utils = StringUtils()
        self.lxml_utils = LxmlUtils()

    def __init_base_xpath(self, base_xpath_param):
        if base_xpath_param == 'basic':
            return '//html/body/div[@id="SysJustIFRAMEDIV"]/table/tr/td/table/tr/td/table'
        elif base_xpath_param == 'form':
            return '//html/body/div[@id="SysJustIFRAMEDIV"]/table/tr/td/form/table/tr/td/table'

    def assemble(self, param):
        content, stock_symbol = param['content'], param['stock_symbol']
        self.content_screener.screen(param)
        html_object = self.__get_html_object(content)
        relative_html_object = self.__traverse_to_relative_html_object(html_object)
        column_name_list = self.__assemble_column_name_list(relative_html_object)
        row_list = self.__assemble_row_list(relative_html_object)
        return {
            'stock_symbol' : stock_symbol,
            'column_name_list' : column_name_list,
            'row_list' : row_list,
        }

    def __get_html_object(self, content):
        content = self.string_utils.normalize_string(content)
        content = content.replace(u'<br>', u'')
        return lxml.html.fromstring(content)

    def __traverse_to_relative_html_object(self, html_object):
        relative_html_object_list = html_object.xpath(self.base_xpath)
        assert len(relative_html_object_list) > 0, 'invalid base_xpath (table_tags)'

        return relative_html_object_list[0]
        
    def __assemble_column_name_list(self, relative_html_object):
        # traverse and sanity check
        tr_tags = relative_html_object.xpath('./tr')
        assert len(tr_tags) > self.column_name_pos, 'invalid tr_tags'

        td_texts = tr_tags[self.column_name_pos].xpath('./td/text()')

        # the first entry should be account
        column_name_list = [td_texts[0]]

        # the rest should be stmt_date
        for text in td_texts[1:]:
            stmt_date = self.string_utils.from_local_string_to_date(text)
            column_name_list.append(stmt_date)

        return column_name_list

    def __assemble_row_list(self, relative_html_object):
        tr_tags = relative_html_object.xpath('./tr')
        assert len(tr_tags) > self.column_name_pos + 1, 'invalid tr_tags'

        return [self.__assemble_row(tr_tag) for tr_tag in tr_tags[self.column_name_pos + 1:]]

    def __assemble_row(self, relative_html_object):
        td_tags = relative_html_object.xpath('./td')
        td_texts = self.lxml_utils.get_text_list(td_tags)

        # return empty row if empty
        if not td_texts:
            return []

        # the first entry should be account
        row = [td_texts[0].strip()]

        # the rest should be stmt_date
        for number_string in td_texts[1:]:
            number = self.string_utils.normalize_number(number_string)
            row.append(number)

        return row
