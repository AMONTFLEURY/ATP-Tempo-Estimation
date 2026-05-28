from numpy.ma.core import floor
from numpy.ma.extras import average
import time
import SystemManager
from multiprocessing import Pool
import librosa
import TempoEstimator
import TempoGetter

pathList, songList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs=4)
# for jobs in CPU_list:
#     print(jobs)
tempoList = []




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
    with Pool(6) as p:
        for result in p.imap(TempoEstimator.estimate, pathList):
            print(result)

    end = time.time()
    print(f"Time elapsed: {end - start} seconds")
