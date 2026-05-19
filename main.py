import librosa
import librosa.display
import os
import math
import soundfile
import audioread
# import Audio
import numpy as np
import matplotlib.pyplot as plt
import array as arr
import time

import SystemManager

pathList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs= 4)
for jobs in CPU_list:
    print(jobs)