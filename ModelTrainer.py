import csv
import math

import pandas as pd

csv_path = "data.csv"
df = pd.read_csv(csv_path, sep='\t')


def create_referenceTable():
    print(df)


def saveTable():
    df.to_csv(csv_path, index=False)


def add_referenceRow(new_row):
    new_row[0] = int(new_row[0])
    df.loc[len(df)] = new_row
    print(df)

