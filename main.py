from numpy.ma.core import floor
from numpy.ma.extras import average
import time
import SystemManager
from multiprocessing import Pool
import librosa
import TempoEstimator
import TempoGetter
import TempoTable

pathList, songList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs=4)
# for jobs in CPU_list:
#     print(jobs)
tempoList = []


def getBeatTimeSpacing(path):
    y, sr = librosa.load(path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_team = librosa.frames_to_time(beats, sr=sr)


if __name__ == "__main__":
    start = time.time()
    # print(TempoGetter.getRawTempo(CPU_list[1][1]))
    # for song in pathList:
    #     (TempoGetter.getRawTempo(song, 1))
    # print("----------------------------------------------------------------")

    # for song in pathList:
    #     print(song)
    #     print(TempoGetter.get_Dtempo_from_onset(song, sr_multiplier=1))
    #     print(TempoGetter.get_Dtempo_from_onset(song, sr_multiplier=0.5))

    # for song in pathList:
    #     print(TempoEstimator.get_tempo_from_onset(song, sr_multiplier=1))

    # for song in pathList:
    #     tempo = TempoGetter.getRawTempo(song, srm=0.5)
    #     print(TempoGetter.estimate_Tempo_From_Tempo(song, tempo=floor(tempo), sr_multiplier=1))
    #
    # print(TempoGetter.get_Dtempo_from_onset(pathList[20], sr_multiplier=1))

    # i = 90
    # timeSer, sr = librosa.load(pathList[i], sr=None, mono=True)
    #
    # print(songList[i])
    # tempo = (TempoGetter.getRawTempo(pathList[i], 2))
    # print(tempo)
    # print(librosa.feature.tempo(y=timeSer, sr=sr))
    # x, y = TempoGetter.get_Dtempo(pathList[i], sr_multiplier=2, onset=True, starting_tempo=tempo, interval=200)
    # # print(len(y))
    # print("average deviation", SystemManager.get_average_deviation(y))
    # print(x)
    # print("------------------------------------------")
    # x, y = TempoGetter.get_Dtempo(pathList[i], sr_multiplier=2, onset=False, starting_tempo=tempo, interval=200)
    # # print(len(y))
    # print("average deviation", SystemManager.get_average_deviation(y))
    # print(x)
    # print("------------------------------------------")
    # x, y = TempoGetter.get_Dtempo(pathList[i], sr_multiplier=.5, onset=False, starting_tempo=92, interval=50)
    # # print(len(y))
    # print("average deviation", SystemManager.get_average_deviation(y))
    # print(x)
    # print("------------------------------------------")
    # print(librosa.get_duration(y=timeSer, sr=sr))
    # print(librosa.get_samplerate(pathList[i]))
    # print(TempoEstimator.estimate(pathList[0]))
    # with Pool(8) as p:
    #     for result in p.imap(TempoEstimator.DynamicTempoAlgo, pathList):
    #         print(result)
    # for i in pathList:
    #     print(TempoEstimator.DynamicTempoAlgo(i))
    # TempoGetter.get_Dtempo(mp3Path=pathList[j])
    # y, sr = librosa.load(pathList[125], sr= None)
    # print(sr)
    # tempo, beats = librosa.beat.beat_track(y=y, sr=sr * 1, start_bpm= 120)
    # beat_team = librosa.frames_to_time(beats, sr=sr)
    # # print(beat_team, len(beat_team))
    # tempo = round(tempo[0])
    # temp = 165
    # print( tempo)
    # print(beat_team[tempo] - beat_team[0])
    # print(beat_team[-1] - beat_team[-tempo])
    # for i in pathList:
    #     y, sr = librosa.load(i, sr=None)
    #     tempo, beats = librosa.beat.beat_track(y=y, sr=sr * 1, start_bpm=120)
    #     beat_team = librosa.frames_to_time(beats, sr=sr)
    #     tempo = round(tempo[0])
    #     x1 = (beat_team[tempo] - beat_team[0])
    #     x2 = (beat_team[-1] - beat_team[-tempo])
    #     print(x2)

    # y, sr = librosa.load(pathList[38])

    # tempo, beats = librosa.beat.beat_track(y=y, sr=sr * 1, start_bpm=120)
    # beat_team = librosa.frames_to_time(beats, sr=sr)
    # print(beat_team, len(beat_team))
    # tempo = round(tempo[0])
    # temp = 165
    # print(tempo)

    # print(beat_team[-1] - beat_team[-tempo])
    # print(beat_team[temp * 3] - beat_team[temp * 2])
    # print(beat_team[temp * 4] - beat_team[temp * 3])

    # print(tempo)

    # print(SystemManager.findFirstBeat())
    # print(TempoEstimator.DynamicTempoAlgo(pathList[j]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[52]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[47]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[38]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[125]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[126]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[20]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[108]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[89]))
    # print(TempoEstimator.DynamicTempoAlgo(pathList[91]))
    # for i in pathList:
    #     vector = TempoEstimator.getTempoVector(i)
    #     vector[3] = TempoEstimator.DTA_checker(vector[3])
    #     print(vector)

    dummy = [151.9991, 99.384, 99.384, 150]
    dummy2 = [103.3594, 105.4688, 105.4688, 105]
    dummy1 = []
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[60])
    # print(pathList[60])
    # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # vector[3] = TempoEstimator.crossChecker(vector, dummy)
    # print(vector, '\n')

    # vector, y, sr = TempoEstimator.getTempoVector(pathList[6])
    # print(pathList[6])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[10])
    # print(pathList[10])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[30])
    # print(pathList[30])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[22])
    # print(pathList[22])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[9])
    # print(pathList[9] )
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[109])
    # print(pathList[109] )
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[118])
    # print(pathList[118] )
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    # start = time.time()
    # print(TempoEstimator.getTempoVectorMP(pathList[9]))
    # end = time.time()
    # print(f"Time elapsed: {end - start} seconds\n")

    #
    # start = time.time()
    # print(pathList[12])
    # vector, y, sr = (TempoEstimator.getTempoVector(pathList[12]))
    # print(vector)
    # end = time.time()
    # print(f"Time elapsed: {end - start} seconds")
    #
    # start = time.time()
    # print(pathList[91])
    # vector, y, sr = (TempoEstimator.getTempoVector(pathList[91]))
    # print(vector)

    with Pool(8) as p:
        for result in p.imap(TempoGetter.getRawTempo, pathList):
            print(result)
    end = time.time()

    print(f"Time elapsed: {end - start} seconds")


    # print(TempoEstimator.DynamicTempoAlgo(pathList[2]))
    # print(TempoGetter.get_Dtempo(pathList[2], sr_multiplier= 4, starting_tempo= 160))
    # TempoEstimator.combinedAlgo(pathList)
