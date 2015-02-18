"""The module handles multi-sheet excel file with a structure like this:
3rd row - name of the security,
4th row Date, PX_LAST as a closing price, volume, PE_RATIO, RSI_14D, RSI_30D, VOLATILITY_10D, VOLATILITY_150D,
and then Date again for the next security."""
import os
import pandas as pd
import xlrd
import datetime

class XlsxParser:
    def __init__(self):
        self.progress = 0

    def parse_excel(self, path, directory, curious_function=None):
        """It takes path to the xls-file to open, and also takes the directory path to save the resulted csv. files."""
        global parsing_progress
        if os.path.exists(path) is False:
            raise Exception("{} doesn't exist!".format(path))
        if os.path.isdir(directory) is False:
            raise Exception("The directory {} doesn't exist!".format(directory))
        if os.name is 'nt':
            if directory[-1] is not "\\":
                directory += "\\"
        else:
            if directory[-1] is not "/":
                directory += "/"
        book = xlrd.open_workbook(path)
        total_sheets = book.nsheets
        names_sheets = book.sheet_names()
        for exchange in range(0, total_sheets):
            self.progress = 5
            if curious_function is not None:
                curious_function(self.progress)
            print("Processing the sheet number {}... \n".format(exchange))
            current_sheet = book.sheet_by_index(exchange)
            columns_to_save = []
            names_of_columns_to_save = []
            dates = []
            for column in range(0, current_sheet.ncols):
                interesting_part = current_sheet.col_slice(column, 2)
                #print(interesting_part)
                #print("Length of the part is: {}\n".format(len(interesting_part)))
                if interesting_part[0].ctype not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                    names_of_columns_to_save.append(interesting_part[0].value)
                else:
                    if interesting_part[1].value == "PX_LAST":
                        dates = []
                        prices = []
                        for price in range(2, len(interesting_part[2:])):
                            if interesting_part[price].ctype is 2:
                                dates_only = current_sheet.cell(price+2, column-1)
                                if dates_only.ctype is 3:
                                    dates.append(dates_only.value)
                                    prices.append(interesting_part[price].value)
                                else:
                                    # The date is not in proper excel date format, so skip the entire row
                                    continue
                            else:
                                continue
                        this_series = pd.DataFrame(data=prices, index=dates, columns=[names_of_columns_to_save[-1]])
                        columns_to_save.append(this_series)
                        del dates, prices, dates_only
                        del this_series
            data_frame_to_save = pd.DataFrame(columns_to_save[0])
            print("Preliminary data frame shape:{}".format(data_frame_to_save.shape))
            """for cur_series_index in range(0, len(columns_to_save[0:])):
                columns_to_save[cur_series_index].columns = names_of_columns_to_save[cur_series_index]"""
            print("Start Joining....")
            i = 0
            for cur_df in columns_to_save[1:]:
                data_frame_to_save = data_frame_to_save.join(cur_df, how='left')
                i += 1
                print("{} joining completed!".format(i))
            dates2 = []
            for this_date in data_frame_to_save.index.values:
                if isinstance(this_date, float):
                    proper_date = datetime.date(*xlrd.xldate_as_tuple(this_date, book.datemode)[:3])
                else:
                    proper_date = None
                #print("New date:{}".format(proper_date))
                dates2.append(proper_date)
            data_frame_to_save.index = pd.Series(dates2)
            data_frame_to_save.index.name = 'Date'
            data_frame_to_save.to_csv(directory+names_sheets[exchange]+".csv", sep=",")
            print("saved to csv.")
            self.progress += 100/total_sheets
            if curious_function is not None:
                if self.progress > 100:
                    self.progress = 100
                curious_function(self.progress)
