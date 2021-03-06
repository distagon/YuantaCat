#-*- coding: utf-8 -*-

from yuantacat.common.date_utils import DateUtils

import datetime
import logging
import operator

class TimeSeries(object):
    @staticmethod
    def create(records):
        """Create time series from records

        Create time series from records.  If there are more than one records of 
        the same (stmt_date, value), we pick up the latest release date as our 
        time series data.

        Args: 
            records: A list of record (release_date, stmt_date, value).  

        Returns:
            A sorted time series (order by stmt_date).  For example, if records 
            are [
                (datetime.date(2015, 9, 30), datetime.date(2002, 12, 31), 1), 
                (datetime.date(2015, 9, 30), datetime.date(2001, 12, 31), 2), 
                (datetime.date(2015, 8, 31), datetime.date(2001, 12, 31), 3), 
            ], we should returns time series [
                (datetime.date(2001, 12, 31), 2), 
                (datetime.date(2002, 12, 31), 1), 
            ].
        """
        group = {}
        for record in records:
            release_date, stmt_date, value = record
            if stmt_date not in group:
                group[stmt_date] = []
            group[stmt_date].append((release_date, value))

        time_series = []
        for stmt_date in group:
            latest_date, value = sorted(group[stmt_date])[-1]
            if value:
                time_series.append((stmt_date, value))

        return TimeSeries(time_series)

    def __init__(self, time_series):
        self.logger = logging.getLogger(__name__)
        self.time_series = sorted(time_series)
        self.date_utils = DateUtils()

    def get(self):
        return self.time_series

    def get_map(self):
        output = {}
        for stmt_date, value in self.time_series:
            output[stmt_date] = value
        return output

    def scalar(self, c):
        output = []
        for stmt_date, value in self.time_series:
            z = c * float(value) 
            output.append((stmt_date, z))
        return TimeSeries(output)

    def get_inverse(self):
        output = []
        for stmt_date, value in self.time_series:
            try:
                z = 1.0 / float(value) 
                output.append((stmt_date, z))
            except ZeroDivisionError as e:
                self.logger.error(e)
        return TimeSeries(output)

    def get_average(self):
        return self.get_moving_average(2)

    def get_moving_average(self, n):
        output = []
        count = len(self.time_series)
        for i in range(count):
            stmt_date = self.time_series[i][0]
            value_list = [self.time_series[i][1] for i in range(max(i - n + 1, 0), i + 1)]
            try:
                z = float(sum(value_list)) / float(len(value_list))
                output.append((stmt_date, z))
            except ZeroDivisionError as e:
                self.logger.error(e)
        return TimeSeries(output)

    def execute_binary_operation(self, operator, other_time_series):
        output = []
        other_map = other_time_series.get_map()
        for stmt_date, value in self.time_series:
            if stmt_date in other_map:
                try:
                    z = operator(float(value), float(other_map[stmt_date]))
                    output.append((stmt_date, z))
                except ZeroDivisionError as e:
                    self.logger.error(e)
        return TimeSeries(output)

    def __add__(self, other_time_series):
        return self.execute_binary_operation(operator.add, other_time_series)

    def __sub__(self, other_time_series):
        return self.execute_binary_operation(operator.sub, other_time_series)

    def __div__(self, other_time_series):
        return self.execute_binary_operation(operator.truediv, other_time_series)

    def __mul__(self, other_time_series):
        return self.execute_binary_operation(operator.mul, other_time_series)

    def accumulate(self):
        output = []
        accumulated_value = 0.0
        for stmt_date, value in self.time_series:
            accumulated_value += value
            output.append((stmt_date, accumulated_value))
        return TimeSeries(output)

    def accumulate_annually(self):
        if not self.time_series:
            return TimeSeries([])
        output = []
        first_stmt_date, first_value = self.time_series[0]
        current_year = first_stmt_date.year
        accumulated_value = 0.0
        for stmt_date, value in self.time_series:
            if stmt_date.year != current_year:
                current_year = stmt_date.year
                accumulated_value = 0.0
            accumulated_value += value
            output.append((stmt_date, accumulated_value))
        return TimeSeries(output)

    def get_yoy(self):
        output = []
        time_series_map = self.get_map()
        for stmt_date, value in self.time_series:
            prev_stmt_date = self.date_utils.get_last_date_of_month_in_prev_year(stmt_date)
            if prev_stmt_date in time_series_map:
                try:
                    prev_value = time_series_map[prev_stmt_date]
                    yoy = (float(value) - float(prev_value)) / float(prev_value)
                    output.append((stmt_date, yoy))
                except ZeroDivisionError as e:
                    self.logger.error(e)                
        return TimeSeries(output)

    def shift(self):
        output = []
        count = len(self.time_series)
        for i in range(1, count):
            stmt_date, value = self.time_series[i]
            prev_stmt_date, prev_value = self.time_series[i - 1]
            output.append((stmt_date, prev_value))
        return TimeSeries(output)

    def group_by_period(self, period):
        if period == 'Q':
            return self.group_by_quarter()
        elif period == 'Y':
            return self.group_by_year()

    def group_by_quarter(self):
        group_map = {}
        time_series_map = self.get_map()
        for stmt_date, value in self.time_series:
            key = self.date_utils.get_last_date_of_quarter(stmt_date)
            if key not in group_map:
                group_map[key] = []
            group_map[key].append((stmt_date, value))
        output = []          
        for key in group_map:
            output.append((key, TimeSeries(group_map[key])))
        return TimeSeries(output)

    def group_by_year(self):
        group_map = {}
        time_series_map = self.get_map()
        for stmt_date, value in self.time_series:
            key = self.date_utils.get_last_date_of_year(stmt_date)
            if key not in group_map:
                group_map[key] = []
            group_map[key].append((stmt_date, value))
        output = []          
        for key in group_map:
            output.append((key, TimeSeries(group_map[key])))
        return TimeSeries(output)

    def get_max_by_period(self, period):
        output = []
        group = self.group_by_period(period).get()
        for key, group_value in group:
            group_time_series = group_value.get_map()
            output.append((key, max(group_time_series.values())))
        return TimeSeries(output)

    def get_min_by_period(self, period):
        output = []
        group = self.group_by_period(period).get()
        for key, group_value in group:
            group_time_series = group_value.get_map()
            output.append((key, min(group_time_series.values())))
        return TimeSeries(output)

    def annualize(self, period):
        if period == 'Q':
            return self.scalar(4)
        elif period == 'Y':
            return self