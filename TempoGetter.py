import librosa
import statistics as stats
import SystemManager


def estimate_Tempo_From_Tempo(tempo, sr_multiplier=1.0, y=None, sr=None, mp3Path="None"):
    if y is None:
        y, sr = librosa.load(mp3Path, sr=None, mono=True, duration=60, offset=30)
    tempo, beatFrames = librosa.beat.beat_track(y=y, sr=sr * sr_multiplier, start_bpm=tempo)
    return round(tempo[0])
    pass


def getTempo(mp3Path):
    y, sr = librosa.load(mp3Path, sr=None, mono=True, duration=20, offset=30)
    z = librosa.get_duration(y=y, sr=sr)
    y_harmonic, y_percussive = librosa.effects.hpss(y=y)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr * 4, tightness=300, trim=False, units="time")
    # x = librosa.frames_to_time(beat_frames, sr= sr)
    tempo = tempo.round()


def getRawTempo(mp3Path=None, srm=1, y=None, sr=None):
    if sr == None:
        y, sr = librosa.load(mp3Path, sr=None, mono=True, offset=15, duration=130)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr * srm)

    return round(tempo[0], 4)


def get_onsets(mp3Path, hopLength=512, startBPM=120):
    y, sr = librosa.load(mp3Path, sr=None, mono=True)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr * 0.5)
    return onset_env


def get_Dtempo_from_onset(mp3Path, sr_multiplier=1.0):
    y, sr = librosa.load(mp3Path, sr=None, mono=True)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr * sr_multiplier)
    dtempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr,
                                   aggregate=None)
    dynamicTempoArray = [(dtempo[50]), dtempo[100], dtempo[1000], dtempo[1500], dtempo[2000], dtempo[2500],
                         dtempo[5000],
                         dtempo[-1000], dtempo[-2000], dtempo[-2700]]
    for i in range(len(dynamicTempoArray)):
        dynamicTempoArray[i] = round(dynamicTempoArray[i])
    # print(SystemManager.get_average_deviation(dynamicTempoArray))
    # dynamicTempoArray.append(sum(dynamicTempoArray)/len(dynamicTempoArray))
    return dynamicTempoArray, dtempo


def get_Dtempo(mp3Path = "", onset=False, sr_multiplier=1.0, interval=300, y= None, sr=0, starting_tempo=120):
    dynamicTempoArray = []
    if y is None:
        y, sr = librosa.load(mp3Path, sr=None, mono=True)

    if onset == False:
        dTempo = librosa.feature.tempo(y=y, sr=sr * sr_multiplier,
                                       aggregate=None, start_bpm=starting_tempo, ac_size=20)
    else:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr * sr_multiplier)
        dTempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr,
                                       aggregate=None, start_bpm=starting_tempo, ac_size=20)
        # print("From Onset")
    frames = round(len(dTempo) / interval)
    for i in range(frames):
        dynamicTempoArray.append(dTempo[interval * i])

    for i in range(len(dynamicTempoArray)):
        dynamicTempoArray[i] = round(dynamicTempoArray[i])
    # print(SystemManager.get_average_deviation(dynamicTempoArray))
    # dynamicTempoArray.append(sum(dynamicTempoArray)/len(dynamicTempoArray))
    return dynamicTempoArray, dTempo


def get_tempo_from_onset(mp3Path, sr_multiplier=1.0, y = None, sr=None, tempo = 120):
    if y is None:
        y, sr = librosa.load(mp3Path, sr=None, mono=True)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr * sr_multiplier, )
    tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
    return round(tempo[0], 4)


def getBeatTime(mp3Path="", sr_multiplier=1.0, y=None, sr=None, tempoE = 120):
    if y is None:
        y, sr = librosa.load(mp3Path, sr=None, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr * 1, start_bpm=tempoE)
    beats = librosa.frames_to_time(beats, sr=sr)
    return round(beats[tempoE] - beats[0], 4), round(beats[-1] - beats[-tempoE], 4)

def DTA_Getter(path = "", y =None, sr = None, starting_tempo = 120):
    # print(path)
    if path != "":
        y, sr = librosa.load(path, mono=True, sr=None)

    # each cell of the holder includes [Initial/Starting Tempo, Mode, Average Deviation]
    holder = []
    starting_tempo = starting_tempo - 10
    increment = 1
    tempo1 = 0

    # intailizing the holder array for the while loop to work
    dynam_tempo_array0, all_dTypos0 = get_Dtempo(mp3Path=path, sr=sr, y=y, onset=False, sr_multiplier=1,
                                                             starting_tempo=starting_tempo, interval=200)
    # Gets average deviation
    avg_dev0 = SystemManager.get_average_deviation(dynam_tempo_array0)
    # just to get the mode
    mode = stats.mode(dynam_tempo_array0)
    holder.append([starting_tempo, mode, avg_dev0])
    # While start
    while tempo1 == 0:
        starting_tempo += increment
        dynam_tempo_array0, all_dTypos0 = get_Dtempo(mp3Path=path, sr=sr, y=y, onset=False,
                                                                 sr_multiplier=0.5,
                                                                 starting_tempo=starting_tempo, interval=200)
        avg_dev0 = SystemManager.get_average_deviation(dynam_tempo_array0)
        mode = stats.mode(dynam_tempo_array0)
        holder.append([starting_tempo, mode, avg_dev0])

        # Checks if the latest holder in the cell is greater than the previous
        # if it is then the previous cell has the is at the lowest point and
        # that index will be stored,
        if holder[-1][2] > holder[-2][2]:
            return holder[-1]