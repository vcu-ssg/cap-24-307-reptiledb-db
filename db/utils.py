"""
utils for working with reptile database
"""
import os
import csv
import chardet
from loguru import logger

csv.field_size_limit(1000000)

def load_file( filename ):
    """ load file into structure """

    # Open the file in binary mode and read a chunk of data
    with open(filename, 'rb') as file:
        rawdata = file.read()

    # Detect the encoding
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    logger.debug(f"{filename} detected encoding: {encoding}")

    # Initialize an empty list to store the data
    data = []

    # Specify the delimiter (in this case, it's a comma)
    delimiter = '\t'
    encoding = 'utf-16'

    # Open the CSV file for reading
    with open(filename, newline='', encoding=encoding ) as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile, delimiter=delimiter )
        
        # Iterate over each row in the CSV file
        for row in csvreader:
            # Append the row as a list to the 'data' list
            data.append(row)

    return data

