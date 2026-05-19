import librosa


def estimate(mp3Path):
    pass


def getTempo(mp3Path):
    y, sr = librosa.load(mp3Path, sr=None, mono=True, duration=20, offset=30)
    z = librosa.get_duration(y=y, sr=sr)
    y_harmonic, y_percussive = librosa.effects.hpss(y=y)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr * 4, tightness=300, trim=False, units="time")
    # x = librosa.frames_to_time(beat_frames, sr= sr)
    tempo = tempo.round()


def getRawTempo(mp3Path):
    y, sr = librosa.load(mp3Path, sr=None, mono=True, offset=15, duration=120)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr * .5, trim=False)
    print("Tempo", tempo)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr, tempo_max=tempo + 20, tempo_min=tempo - 20)
    tempo, beats = librosa.beat.beat_track(onset_envelope=pulse, sr=sr, trim=False)
    return round(tempo[0])
