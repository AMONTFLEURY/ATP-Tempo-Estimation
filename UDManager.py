import pandas as pd
from numba import none

pd.set_option('display.max_rows', None)

csv_path = "Userdata.csv"
df = pd.read_csv(csv_path)


def view_user_data():
    print(df)


def add_row(new_data, vector_for_data=None):
    if vector_for_data == None:
        new_row = [new_data[1], new_data[0]]
        for data in new_data[2]:
            new_row.append(data)
        df.loc[len(df)] = new_row
    else:
        # Title,index,Tempo,SR x .5,SR x 1,SR x 2,Onset SR x 1,60 Window,beat len,DTF1,DTF2
        new_row = [new_data[1],
                   new_data[0],
                   new_data[2],
                   vector_for_data[1],
                   vector_for_data[2],
                   vector_for_data[3],
                   vector_for_data[4],
                   vector_for_data[5],
                   vector_for_data[6],
                   vector_for_data[7],
                   vector_for_data[8]]
        df.loc[len(df)] = new_row
        # print((df.loc[len(df) - 1]).to_string())

    # print(df)


def saveTable():
    dfnew = df.sort_values(by=['Title'], ascending=False)
    dfnew.to_csv(csv_path, index=False)


def check_for_index(title):
    if 1 <= (df['Title'] == title).sum():
        # print(df[df['Title'] == title].to_string())
        return df[df['Title'] == title], True
    else:
        return None, False


def print_UserData():
    print(df)
