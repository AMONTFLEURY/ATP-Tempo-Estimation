import SystemManager
import multiprocessing

import TempoEstimator

pathList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs= 4)
# for jobs in CPU_list:
#     print(jobs)
tempoList = []
def getTempos(Cpu_list):

    for job in range(len(Cpu_list[3])):
        try:
            process_0 = multiprocessing.Process(target= TempoEstimator.getRawTempo(Cpu_list[0][job]))
            process_1 = multiprocessing.Process(target= TempoEstimator.getRawTempo(Cpu_list[1][job]))
            process_2 = multiprocessing.Process(target= TempoEstimator.getRawTempo(Cpu_list[2][job]))
            process_3 = multiprocessing.Process(target= TempoEstimator.getRawTempo(Cpu_list[3][job]))

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
    # print(TempoEstimator.getRawTempo(CPU_list[1][1]))
    for song in pathList:
        TempoEstimator.getRawTempo(song)
