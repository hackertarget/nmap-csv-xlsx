# the bones of this script was sourced on StackExchange 
#
# https://stackoverflow.com/questions/42092263/combine-multiple-csv-files-into-a-single-xls-workbook-python-3
#
# a simple script to combine multiple csv's into an XLSX spreadsheet with a sheet per csv

# 
# ~/$ python3 csv-to-xlsx.py 192.168.0.0_24.csv 10.0.0.0_8.csv
#

import pandas as pd
import sys
import os

writer = pd.ExcelWriter('default.xlsx') # output name

# add custom formatting
workbook = writer.book
workbook.formats[0].set_font_size(9)   # set default font size

header_format = workbook.add_format()
header_format.set_font_color('black')
header_format.set_bg_color('#cccccc')
header_format.set_bold()

# create sheet per csv on command line
for csvfilename in sys.argv[1:]:
    df = pd.read_csv(csvfilename)
    filename = os.path.splitext(csvfilename)[0]

    # header is False here, as it is written using the header_format below
    df.to_excel(writer,sheet_name=filename,startrow=1, index=False, header=False)
    
    for column in df:
        col_idx = df.columns.get_loc(column)
        writer.sheets[filename].set_column(col_idx, col_idx, 15)

    # write header with header_format
    worksheet = writer.sheets[filename]
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
writer.save()
