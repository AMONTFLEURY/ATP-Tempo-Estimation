import csv
import math

import pandas as pd
from librosa.beat import tempo

import SystemManager
import TempoEstimator

csv_path = "data.csv"
csv_path2 = "data_refT.csv"
df = pd.read_csv(csv_path, encoding_errors='ignore')
df_model = pd.read_csv(csv_path2)
columns = [
    'Title', 'Tempo', 'SR x .5', 'SR x 1', 'SR x 2', 'Onset SR x 1', '60 Window', 'beat len', 'DTF1', 'DTF2'
]


def view_reference_table():
    print(df_model)


def view_training_data():
    print(df)


def song_lookup(name=''):
    found = df[df['Title'].str.contains(name)]
    print(found)


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
                                     'SR x .5': (current_group['SR x .5'].mode()[0]),
                                     'SR x 1': (current_group['SR x 1'].mode())[0],
                                     'SR x 2': (current_group['SR x 2'].mode()[0]),
                                     'Onset SR x 1': (current_group['Onset SR x 1'].mode()[0]),
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


def saveData():
    df.to_csv(csv_path, index=False)


def add_datapoint():
    #     Checks if a song name is already in data.cvs
    #      if not, get its vector, then allow the user to set it's tempo
    paths, names = SystemManager.pullPaths()
    temp = pd.DataFrame(columns=columns)
    for i in range(len(names)):
        x = ((names[i])[4:16]).encode('ascii', errors='replace').decode('ascii')
        found = df[df['Title'].str.contains(x, regex=False)]
        if len(found) == 0:
            print("Not Found \n" + names[i])
            vector, y, sr = TempoEstimator.getTempoVector(paths[i])
            print(vector)
            tempo = input("tempo: ")
            new_row = [
                names[i],
                int(tempo),
                vector[1],
                vector[2],
                vector[3],
                vector[4],
                vector[5],
                vector[6],
                vector[7],
                vector[8]
            ]

            temp.loc[len(temp)] = new_row
            print(temp.iloc[-1])
            # df.loc[len(df)] = new_row
            # print(df.loc[len(df) - 1])

            x = input("Looks good?\n1. Yes\n2. NO!!!!!\n")
            if x != '1':
                temp.iat[-1, 1] = 0
            if x == 'x':
                break
            print((names[i]) + " was added")
            df.loc[len(df)] = new_row
            saveData()


    print("new songs added-->\n" + temp)


def add_referenceRow(new_row):
    new_row[0] = int(new_row[0])
    df.loc[len(df)] = new_row
    print(df)


def get_table_slices(estimated_tempo, scope=10):
    floor = estimated_tempo - scope
    ceiling = estimated_tempo + scope
    df_slice1 = df_model[df_model['Tempo'].between(floor, ceiling)]
    if estimated_tempo <= 85 or estimated_tempo > 130:
        if estimated_tempo > 130:
            estimated_tempo = estimated_tempo / 2
        else:
            estimated_tempo = estimated_tempo * 2
        estimated_tempo = math.floor(estimated_tempo)
        floor = estimated_tempo - scope
        ceiling = estimated_tempo + scope
        df_slice2 = df_model[df_model['Tempo'].between(floor, ceiling)]
    else:
        df_slice2 = None

    return df_slice1, df_slice2
