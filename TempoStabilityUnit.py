import librosa

import RoundChecker
import SystemManager
import TempoEstimator


def stability_check(y, sr, path, tempo):
    matrix = tempo_matrix(y, sr, path)
    flatten_matrix = []
    estimation_matrix = []
    for i in matrix:
        tempo, score, bias = TempoEstimator.cross_checker(i)
        estimation_matrix.append([tempo, score])
    for i in matrix:
        for j in i:
            flatten_matrix.append(j)
    return rolling_star(flatten_matrix, estimation_matrix)


def tempo_matrix(y, sr, path):
    duration = librosa.get_duration(y=y, sr=sr)
    split = trackSplitter(duration)
    tempo_matrix = []
    vector, y, sr = TempoEstimator.getTempoVector(path=path, chunk=(split))
    tempo_matrix.append(vector)
    vector, y, sr = TempoEstimator.getTempoVector(path=path, chunk=(-split))
    tempo_matrix.append(vector)
    vector, y, sr = TempoEstimator.getTempoVector(path=path, chunk=(split + split / 3))
    tempo_matrix.append(vector)
    print(tempo_matrix)
    return tempo_matrix


def check(e_matrix):
    estimations = []
    for i in e_matrix:
        estimations.append(i[0][0])
        estimations.append(i[0][1])
    if 2 < len(set(estimations)):
        print("tempo is unstable")
        return "tempo is unstable"
    pass


def rolling_star(t_matrix, e_matrix):
    winning_tempos = []
    # message = check(e_matrix)
    for row in e_matrix:
        choice = RoundChecker.rolling_star(row[1], row[0])
        if choice == 0:
            choice = 1
        else:
            choice = 0
        winning_tempos.append(row[0][choice])
    huh = SystemManager.stats.mode(winning_tempos)
    cnt = 0
    for i in winning_tempos:
        if i == huh:
            cnt += 1
    if cnt >= 2:
        return huh, 6
    return 999,  check(e_matrix)
    pass


def slice_correcter(tempos):
    if abs(tempos[0] - tempos[1]) < 3.7 > abs(tempos[1] - tempos[2]):
        return sum(tempos) / len(tempos)
    elif 142 < tempos[0] < 167:
        x = min(abs(tempos[0] - 150), abs(tempos[1] - 150), abs(tempos[2] - 150))
        for i in tempos:
            if x == abs(i - 150):
                return i
    elif 1.9 < max(tempos) / min(tempos) < 2.3:
        return tempos[0]
    else:
        x = min(abs(tempos[0] - 120), abs(tempos[1] - 120), abs(tempos[2] - 120))
        for i in tempos:
            if x == abs(i - 120):
                return i
        return


def trackSplitter(duration):
    return round(duration / 2)
