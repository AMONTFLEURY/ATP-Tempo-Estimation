import pandas as pd
from numba import none

pd.set_option('display.max_rows', None)

csv_path = "Userdata.csv"
df = pd.read_csv(csv_path)

def view_user_data():
    print(df)


def add_row(new_data):
    new_row = [new_data[1], new_data[0]]
    for data in new_data[2]:
        new_row.append(data)
    df.loc[len(df)] = new_row
    # print(df)


def saveTable():
    dfnew = df.sort_values(by=['Title'], ascending=False)
    dfnew.to_csv(csv_path, index=False)


def check_for_index(title):
    if 1 <= (df['Title'] == title).sum():
        # print(df[df['Title'] == title].to_string())
        return df[df['Title'] == title],
    else:
        return None,


def print_UserData():
    print(df)

