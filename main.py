from numpy.ma.core import floor
from numpy.ma.extras import average

import SystemManager
import multiprocessing

import TempoEstimator
import TempoGetter

pathList, songList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs= 4)
# for jobs in CPU_list:
#     print(jobs)
tempoList = []
def getTempos(Cpu_list):

    for job in range(len(Cpu_list[3])):
        try:
            process_0 = multiprocessing.Process(target= TempoGetter.getRawTempo(Cpu_list[0][job]))
            process_1 = multiprocessing.Process(target= TempoGetter.getRawTempo(Cpu_list[1][job]))
            process_2 = multiprocessing.Process(target= TempoGetter.getRawTempo(Cpu_list[2][job]))
            process_3 = multiprocessing.Process(target= TempoGetter.getRawTempo(Cpu_list[3][job]))

            process_0.start()
            process_1.start()
            process_2.start()
            process_3.start()

            process_0.join()
            process_1.join()
            process_2.join()
            process_3.join()
        except:
            pass

if __name__ == "__main__":
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

    for song in pathList:
        tempo = TempoGetter.getRawTempo(song, srm= 0.5)
        print(TempoGetter.estimate_Tempo_From_Tempo(song, tempo= floor(tempo), sr_multiplier=1))