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
    # with Pool(6) as p:
    #     for result in p.imap(TempoEstimator.estimate, pathList):
    #         print(result)
    # print(TempoEstimator.estimate(pathList))
    j = 91
    print(pathList[j])
    for i in range(30, 240, 5):
        DynamicTempoMode, ModeFrequency, ArrayLength, AverageDeviation = TempoEstimator.getTempoFromDynamTempoArray(pathList[j],tempo=i)
        print(DynamicTempoMode)
    print("---------------------------------------------")
    for i in range(30, 240, 5):
        DynamicTempoMode, ModeFrequency, ArrayLength, AverageDeviation = TempoEstimator.getTempoFromDynamTempoArray(
            pathList[j], tempo=i)
        print(AverageDeviation)
    # y, sr = librosa.load(pathList[j])
    # tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # beat_team = librosa.frames_to_time(beats, sr=sr)
    # print(beat_team)
    # temp = 139
    # print(beat_team[temp] - beat_team[0])
    # print(beat_team[temp * 3] - beat_team[temp * 2])
    # print(beat_team[temp * 4] - beat_team[temp * 3])


    # print(tempo)

    # print(SystemManager.findFirstBeat())

    end = time.time()
    print(f"Time elapsed: {end - start} seconds")


