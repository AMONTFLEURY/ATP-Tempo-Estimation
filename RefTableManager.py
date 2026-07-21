import csv
import math

import pandas as pd

csv_path = "data.csv"
df = pd.read_csv(csv_path, encoding_errors='ignore')


def view_reference_table():
    print(df)

def create_RTable_from_list(temp_df):
    pass

def saveTable():
    df.to_csv(csv_path, index=False)


def add_referenceRow(new_row):
    new_row[0] = int(new_row[0])
    df.loc[len(df)] = new_row
    print(df)


