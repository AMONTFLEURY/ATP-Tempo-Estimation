import csv
import math

import pandas as pd
from librosa.beat import tempo

csv_path = "data.csv"
csv_path2= "data_refT.csv"
df        =  pd.read_csv(csv_path, encoding_errors='ignore')
df_model  = pd.read_csv(csv_path2)




def view_reference_table():
    print(df_model)
def view_training_data():
    print(df)


def create_RTable_from_list():
    # drop title
    # loop from min tempo -> max tempo
    # group all tempos
    # get mode for each col from group
    # save to data_refT
    temp = df_model
    df2 = df.drop(columns=['Title'])
    for i in range(df2['Tempo'].min(), df2['Tempo'].max()):
        current_group = df2.loc[df2['Tempo'] == i]
        if len(current_group) > 0:
            print("--------------------------------------------------- \n", current_group.to_string())

            new_row = pd.DataFrame([{'Tempo': i,
                                     'SR x .5':(current_group['SR x .5'].mode()[0]),
                                     'SR x 1':(current_group['SR x 1'].mode())[0],
                                     'SR x 2':(current_group['SR x 2'].mode()[0]),
                                     'Onset SR x 1':(current_group['Onset SR x 1'].mode()[0]),
                                     '60 Window': (current_group['60 Window'].mode()[0]),
                                     'beat len': (current_group['beat len'].mode()[0]),
                                     'DTF1': (current_group['DTF1'].mode()[0]),
                                     'DTF2': (current_group['DTF2'].mode()[0])}])
            print(new_row.to_string(), "\n")
            temp = pd.concat([temp, new_row])
    print(temp)
    # temp.to_csv(csv_path2, index=False)


def saveTable():
    df_model.to_csv(csv_path2, index=False)


def add_referenceRow(new_row):
    new_row[0] = int(new_row[0])
    df.loc[len(df)] = new_row
    print(df)

def get_table_slices(estimated_tempo, scope = 10):
    floor = estimated_tempo - scope
    ceiling = estimated_tempo + scope
    df_slice1 = df[df['Tempo'].between(floor, ceiling)]
    if estimated_tempo <= 70 or estimated_tempo > 130:
        if estimated_tempo > 130:
            estimated_tempo = estimated_tempo / 2
        else:
            estimated_tempo = estimated_tempo *2
        estimated_tempo = estimated_tempo * 2
        math.floor(estimated_tempo)
        floor = estimated_tempo - scope
        ceiling = estimated_tempo + scope
        df_slice2 = df[df['Tempo'].between(floor, ceiling)]
    else:
        df_slice2 = None

    return df_slice1, df_slice2
