import os
import multiprocessing
import pandas as pd
import statistics as stats
from numpy.ma.extras import average
import json
import re
import pandas as pd

H_res = 1920
V_res = 1080
gameRate = 240
frameRate = 120
music_dir_default = "Music2"
music_dir = "Music2"
Unbeatable_dir = "C:/Users/laure/AppData/LocalLow/D-CELL GAMES/UNBEATABLE/CustomSongs/ATPTEST/ATP - TEST () [Easy].txt"


def pullPaths():
    songPaths = []
    songNames = []
    fileScanner = os.scandir("Music2")
    for files in fileScanner:
        fileName = files
        songPaths.append(music_dir+"/" + (fileName.__str__())[11:-2])
        songName = ((fileName.__str__())[11:-2])
        songName = songName.replace(" (SPOTISAVER)", "")
        songName = songName.replace(".mp3", "")
        songNames.append(songName)
        # print(songName)
    return songPaths, songNames


def checkFiles():
    files = os.scandir()
    for i in files:
        print(i)


def getCPUcount():
    return os.cpu_count()


def get_average_deviation(vector):
    total = 0
    avg = average(vector)
    for num in vector:
        total += round(abs(num - avg), 4)
    return total / len(vector)


def splitPathList(fullList, jobs=-1):
    list_of_lists = []
    if jobs == -1:
        cpus = getCPUcount()
    else:
        cpus = jobs

    # creates arrays for the amount of jobs to be done
    # splitting the full list in each cpu list evenly

    for i in range(cpus):
        list_of_lists.append([])

    for i in range(len(fullList)):
        list_of_lists[i % cpus].append(fullList[i])
    return list_of_lists


def compareDynamicTempos(arr1, arr2):
    num = []
    for i in range(len(arr1)):
        if arr1[i] == arr2[i]:
            num.append(arr1[i])
    if len(num) == 0:
        return 0, 0
    else:
        x = stats.mode(num)
        return x, num.count(x)


def findFirstBeat(time_series, currentbeat):
    pass


def cutLetters(string):
    nums = []
    buffer = ""
    for i in range(len(string)):
        index = string[i:i + 12]
        if bool(re.search(r"[0-9]", string[i])):
            buffer += string[i]
        else:
            if not buffer == "":
                if string[i] == '\n' and string[i - 1 - len(buffer)] == '\n' and 170 > int(buffer) > 49:
                    nums.append(buffer)
                else:
                    pass
                buffer = ""
    return nums


def edit_beat_map(new_tempo, path):
    with open(Unbeatable_dir, "r") as file:
        lines = file.readlines()
    beat_len = (round(60000 / new_tempo, 4))
    bls = str(beat_len)
    while len(bls) < 12:
        bls = bls + "0"

    beats = 1
    lines[25] = "213,192," + str(beat_len * beats) + ",5,0,0:0:0:0:\n"
    lines[21] = "0," + bls + ",4,2,0,100,1,0\n"
    for i in range(26, len(lines) - 1):
        lines[i] = beatmapper(lines[i], lines[25], beat_len)

    with open(Unbeatable_dir, "w") as file:
        file.writelines(lines)

    # line[21] =


def beatmapper(line0, base_line, bls=0.0):
    pos = line0[0:8]
    line0 = line0.replace(pos, "")
    timing = re.search(r'\d+', line0)
    timing = timing.group()
    line0 = line0.replace(timing, "")

    gap = (float(timing) / bls)
    pos_timing = pos + str(bls * gap)
    timing2 = re.search(r'\d+', line0[7:])
    timing2 = timing2.group()
    if float(timing2) > 0:
        line0 = line0[7:].replace(timing2, "")
        pos_timing = pos_timing + "," + str(bls * (float(timing2) / bls))

    nextline = pos_timing + line0
    return nextline


#                 if len(buffer) == 1 or string[i] == '\n' or int(buffer) > 170 or bool(re.search(r'[a-zA-Z]', string[i+1])):
test = """002 Mello - Love Lightside (Love Sickubus).mp3
C♯ minor
12A
85
171 - SUPERSONIC.mp3
B major
1B
132
A Stranger I Remain - Maniac Agenda Mix.mp3
D♯ minor
2A
82
Actor's Anteroom -Remastering- (キャラクターセレクト) _ MELTY BLOOD Actress Again Current Code OST.mp3
G minor
6A
87
Akegata.mp3
C♯ major
3B
118
Arcade- Live.mp3
F major
7B
114
As much as possible.mp3
C major
8B
100
Baby Smoove - I Dare U (SPOTISAVER).mp3
D♯ minor
2A
146
BABYMETAL - Gimme Chocolate!! (SPOTISAVER).mp3
E major
12B
110
BABYMETAL - Road of Resistance (SPOTISAVER).mp3
F♯ minor
11A
103
BabyTron - 007.mp3
G minor
6A
101
Base 11.mp3
B minor
10A
150
beabadoobee - Real Man (SPOTISAVER).mp3
C♯ major
3B
130
Beat Eat Nest (Byakuya Theme).mp3
A minor
8A
89
BIBI - Apocalypse (SPOTISAVER).mp3
G♯ minor
1A
101
BIBI - Derre (SPOTISAVER).mp3
E major
12B
125
Billie Eilish - BIRDS OF A FEATHER (SPOTISAVER).mp3
D major
10B
105
bluberry bakwood.mp3
E major
12B
149
Brahman.mp3
G♯ minor
1A
73
Bullet Dance II.mp3
D minor
7A
150
Can't Smash My Invincible Armor!.mp3
B minor
10A
82
Celestial Resort - Good Karma Mix.mp3
A minor
8A
70
Che - bluberry bakwood (SPOTISAVER).mp3
E major
12B
149
Che - CUT OFF YOUR HANDS (SPOTISAVER).mp3
D♯ minor
2A
147
Che - ROLLING STONE (SPOTISAVER).mp3
C♯ minor
12A
83
Che, OsamaSon - WHIPPIN (SPOTISAVER).mp3
C minor
5A
74
Che, Saska - SASKA YOU MADE IT (SPOTISAVER).mp3
C♯ major
3B
152
Cochise - GOOGLE ME (SPOTISAVER).mp3
B major
1B
149
Dance in the Forest - Falcom Sound Team.mp3
D minor
7A
70
Dancefloor in the Blue Sky - Yoiyami Dancers_ Twilight Danmaku Dancers OST.mp3
C minor
5A
140
Diamond Stitching (Bonus).mp3
D major
10B
85
Elegant Summer -Remastering- (遠野邸ホール夜) _ MELTY BLOOD Actress Again Current Code OST.mp3
A minor
8A
105
Evanescence - Bring Me To Life (SPOTISAVER).mp3
E minor
9A
95
Every Day Is Night.mp3
F minor
4A
113
Extras.mp3
D major
10B
124
Falcom Sound Team jdk - Guruguru Majin De Pon (SPOTISAVER).mp3
D major
10B
93
feminine adornments - julie.mp3
E minor
9A
93
FOMDJ.mp3
F♯ minor
11A
140
Free Dominguez - A Stranger I Remain - Maniac Agenda Mix (SPOTISAVER).mp3
D♯ minor
2A
82
Fried By Fluoride - The Love I Lost (SPOTISAVER).mp3
A minor
8A
105
Frontin - OsamaSon.wav
G♯ minor
1A
77
Garoad - Synthestitch (SPOTISAVER).mp3
D minor
7A
130
Garoad - You've Got Me (SPOTISAVER).mp3
E♭ major
5B
74
Girl Like Me.mp3
F♯ minor
11A
138
Girls Be あいさつ Greetings Part I.mp3
E major
12B
115
Girls Be 絶対ダメッ! Absolutely Not!.mp3
D major
10B
87
Girls Be - フーアーユー Who Are You.mp3
E major
12B
96
Going Under OST - hand over fist.mp3
G minor
6A
91
Hasta la Vista - Protect.mp3
A♯ minor
3A
79
Holy Orders ~Be Just Or Be Dead~ -Ky's Theme-.mp3
E minor
9A
120
Houyo.mp3
C♯ major
3B
90
I _3 Techno.mp3
F minor
4A
135
I’m Just Like That.mp3
A major
11B
123
Jamie Paige - Cadmium Colors (SPOTISAVER).mp3
C major
8B
75
Jamie Paige - I Wish That I Could Fall (SPOTISAVER).mp3
E major
12B
140
Jamie Paige, OK Glass - BIRDBRAIN (SPOTISAVER).mp3
D major
10B
80
Jamie Paige, Visualeyes - ROT FOR CLOUT (SPOTISAVER).mp3
D minor
7A
86
Ken Carson - Me N My Kup (SPOTISAVER).mp3
C♯ minor
12A
140
kinoue64 - who are you (SPOTISAVER).mp3
F♯ minor
11A
80
Lady Gaga - Bad Romance (SPOTISAVER).mp3
A minor
8A
119
Lady Gaga, Colby O'Donis - Just Dance (SPOTISAVER).mp3
E major
12B
119
lexycat - glitter.mp3
A♭ major
4B
130
lexycat - medicine (SPOTISAVER).mp3
F major
7B
100
Lil Uzi Vert - 444+222 (SPOTISAVER).mp3
D♯ minor
2A
77
Lil Uzi Vert - Sauce It Up (SPOTISAVER).mp3
C♯ minor
12A
80
Lil Uzi Vert, BABYMETAL - The End (feat. BABYMETAL) (SPOTISAVER).mp3
F major
7B
110
Lotus Juice, Azumi Takahashi, アトラスサウンドチーム - Color Your Night (SPOTISAVER).mp3
C♯ major
3B
95
LUCKI - EXOTIC (SPOTISAVER).mp3
G major
9B
144
Lucy Bedroque - G6 Anthem (SPOTISAVER).mp3
A major
11B
63
Lucy Bedroque - How to Pretend (SPOTISAVER).mp3
D major
10B
95
Lucy Bedroque - Mimosa (2024).mp3
E major
12B
129
Lucy Bedroque - true perspective (SPOTISAVER).mp3
C major
8B
87
Machine Love - Jamie Paige.wav
E♭ major
5B
87
Metro Boomin, Future, Don Toliver - Too Many Nights (feat. Don Toliver & with Future) (SPOTISAVER).mp3
G minor
6A
88
Miki Matsubara - Mayonaka no Door Stay With Me (SPOTISAVER).mp3
F major
7B
108
Modernism Street -Remastering- (不夜の賑わい) _ MELTY BLOOD Actress Again Current Code OST (1).wav
C minor
5A
135
Monochrome.mp3
B minor
10A
101
Monster Hunter Generations Ultimate OST_ Valstrax Theme バルファルク BGM [HQ 4K].mp3
D minor
7A
128
New Tune.mp3
C major
8B
82
no. no. no..mp3
A minor
8A
74
Normal Battle -Labyrinth of Amala-.mp3
E minor
9A
142
Obscure Zone -Remastering- (廃棄空間) _ MELTY BLOOD Actress Again Current Code OST.wav
C minor
5A
150
Only Ever You.mp3
E minor
9A
107
OsamaSon - Frontin (SPOTISAVER).mp3
G♯ minor
1A
77
OsamaSon - Function.mp3
C major
8B
85
OsamaSon - Get Away.mp3
A minor
8A
77
OsamaSon - off that! (SPOTISAVER).mp3
C♯ major
3B
80
OsamaSon - Room 156 (SPOTISAVER).mp3
B minor
10A
78
osamason - text back.mp3
A♯ minor
3A
78
OsamaSon - Whats Happening.mp3
A major
11B
147
Paranoid.mp3
G♯ minor
1A
150
Pi'erre Bourne - Ballad (Official Audio).mp3
E minor
9A
101
Pi'erre Bourne - Feds (Official Audio).mp3
F major
7B
133
Pi'erre Bourne - Poof (Official Audio).mp3
C minor
5A
81
Pi'erre Bourne - Romeo Must Die (Official Audio).mp3
A♭ major
4B
71
Pi'erre Bourne - Try Again (Official Audio).mp3
D minor
7A
74
Pink Moscato - PlaqueBoyMax.mp3
F♯ minor
11A
76
PinkPantheress - Pain (SPOTISAVER).mp3
A♭ major
4B
125
PinkPantheress - Stateside (SPOTISAVER).mp3
A♯ minor
3A
123
PinkPantheress, Rachel Chinouriri - Romeo + Rachel Chinouriri (SPOTISAVER).mp3
C minor
5A
79
PinkPantheress, Zara Larsson - Stateside + Zara Larsson (SPOTISAVER).mp3
A♯ minor
3A
124
Playboi Carti - H00DBYAIR.mp3
G♯ minor
1A
140
Playboi Carti - WICKED.mp3
D♯ minor
2A
149
Playboi Carti- Bouldercrest (Piru) [feat. Offset].wav
G minor
6A
142
Pokémon Omega Ruby & Alpha Sapphire - Cobalion, Virizion & Terrakion Battle Music (HQ).mp3
C minor
5A
87
Pokémon Omega Ruby & Alpha Sapphire - Vs Zinnia (Highest Quality) (1).mp3
D major
10B
89
POLTA遠くへ行きたいMV.mp3
E minor
9A
83
Ponpoko in the Distance, Tenchio, postergirlxoxo - Hotel Room 215 (SPOTISAVER).mp3
E minor
9A
103
Protect - Re4 [Official Audio].mp3
D♯ minor
2A
73
Protect - What doesn't kill u (SPOTISAVER).mp3
A♭ major
4B
149
Pull the Trigger.mp3
G minor
6A
146
Pz' - Keep It Tucked (Studio Video).mp3
G♯ minor
1A
143
Queens of the Stone Age - First It Giveth (SPOTISAVER).mp3
A♯ minor
3A
109
Rhythmical Bustle -Remastering- (無人の街並み) _ MELTY BLOOD Actress Again Current Code OST.mp3
G minor
6A
132
Rio Da Yung Og x Babytron- Legendary (Official Video).mp3
F minor
4A
97
Risk It All, Pt.2.mp3
A minor
8A
88
Roar, Roar, Roar!!.mp3
F♯ minor
11A
93
ROLLING STONE - Che.mp3
C♯ minor
12A
83
Romance Sengen.mp3
C minor
5A
78
Roundtripski.mp3
G minor
6A
85
SAKURA-KOI-UTA -Remastering- (桜花繚乱) _ MELTY BLOOD Actress Again Current Code OST.mp3
C minor
5A
106
SA-Rank Battle - Deniz Akbulut.wav
G minor
6A
90
Satellite Lovers - How much I Love you,baby (SPOTISAVER).mp3
A major
11B
93
Sayonara Anata.mp3
G major
9B
108
Scraper Sky High (Hyde Theme).mp3
D major
10B
110
SEAPOOL - PICNIC (SPOTISAVER).mp3
B minor
10A
85
Severe person -Remastering- (遠野邸庭園) _ MELTY BLOOD Actress Again Current Code OST.mp3
F minor
4A
81
Shadow World - ”P4D”ver..mp3
A major
11B
116
She is inside, He is outside.mp3
D minor
7A
97
ShinMegamiTensieV OST - Battle -Daat- Vengeance.mp3
E minor
9A
95
ShinMegamiTensieV OST -Battle -Daat-.mp3
E minor
9A
88
Signs Of Love.mp3
A♯ minor
3A
105
Sip In My Room.mp3
D major
10B
72
skaiwater - blink twice (SPOTISAVER).mp3
C♯ major
3B
70
Soutaiseiriron - Kininaru Ano Ko (SPOTISAVER).mp3
B minor
10A
96
Soutaiseiriron - Moonlight Ginga (SPOTISAVER).mp3
C major
8B
82
Soutaiseiriron - Sumatra Keibitai (SPOTISAVER).mp3
C major
8B
100
SQUARE UP - jamie paige x peak divide feat. GUMI & rachel lake (1).mp3
A major
11B
85
Stavros Markonis, Foivos - Deluge-ional (SPOTISAVER).mp3
B minor
10A
75
StellerBladeOst - Silent Street _Battle_ - Hyunmin Cho.mp3
A♯ minor
3A
144
StellerBladeOST - Silent Street Battle.mp3
A♯ minor
3A
144
StellerBladeOst - Stalker.mp3
G minor
6A
85
StellerBladeOST -Silent Street Type A.mp3
A♯ minor
3A
144
Strange Dreamer -Remastering- (午前零時の逢瀬) _ MELTY BLOOD Actress Again Current Code OST.mp3
G major
9B
135
SUPER PLAY(スーパープレイムービー).mp3
A minor
8A
75
Super Wrong.mp3
A minor
8A
81
Tears For Fears - Head Over Heels (SPOTISAVER).mp3
A minor
8A
95
The Arctic.mp3
E minor
9A
80
The Dancer's High - Yoiyami Dancers_ Twilight Danmaku Dancers OST.mp3
B minor
10A
87
The theme of Arcueid -Remastering- (死角の辻) _ MELTY BLOOD Actress Again Current Code OST.mp3
D♯ minor
2A
87
Tiffany Day - AMERICAN GIRL (SPOTISAVER).mp3
E♭ major
5B
132
Tiffany Day - NO LUCK (SPOTISAVER).mp3
C major
8B
94
Tiffany Day - PRETTY4U (SPOTISAVER).mp3
D minor
7A
142
Towelket ha odayakana.mp3
C♯ major
3B
123
Troublesome Visitor -Remastering- (遠野邸ホール異変) _ MELTY BLOOD Actress Again Current Code OST.mp3
A minor
8A
82
Turbo.mp3
C♯ major
3B
80
TWICE - HELL IN HEAVEN (SPOTISAVER).mp3
B minor
10A
105
TWICE - THIS IS FOR (Extended) (SPOTISAVER).mp3
C♯ minor
12A
128
TWICE - THIS IS FOR (SPOTISAVER).mp3
C♯ minor
12A
128
TWICE - What is Love (SPOTISAVER).mp3
A♭ major
4B
85
Ultraviolet.mp3
G minor
6A
82
UNBEATABLE OST - WAITING by peak divide & Rachel Lake.wav
E♭ major
5B
89
UNBEATABLE Vocal OST - Track 7 - LONER (1).mp3
A minor
8A
109
uncomfy _feat. OsamaSon_ - xaviersobased.mp3
A major
11B
110
Vampire Hour.mp3
C♯ minor
12A
75
Vlad.mp3
C♯ major
3B
71
worth it.mp3
F♯ minor
11A
120
xaviersobased - red snapper (SPOTISAVER) (1).mp3
G minor
6A
116
xaviersobased - red snapper (SPOTISAVER).mp3
G minor
6A
116
Yasashii guitar.mp3
E♭ major
5B
102
YONLAPA - Misguided Ghost (SPOTISAVER).mp3
B minor
10A
138
YONLAPA - Sweetest Cure (SPOTISAVER).mp3
E major
12B
69
YONLAPA - Velvet Love (SPOTISAVER).mp3
A major
11B
105
Your Love Is a Drug.mp3
C minor
5A
74
YT - Lonely (SPOTISAVER).mp3
G♯ minor
1A
72
Yui Horie - silky heart (SPOTISAVER).mp3
B major
1B
135
Σtella - Adagio (SPOTISAVER).mp3
D minor
7A
100
スマイリーを探して.mp3
E major
12B
85
モーニングコール.mp3
E major
12B
129
ライフ・ゴーズ・オン.mp3
B minor
10A
90
ラブレイバー.mp3
D major
10B
65
リュベンス - 天使さんMusic Video.mp3
B♭ major
6B
120
リュベンス - 風を止めないでMusic Video.mp3
F major
7B
74
僕と夕陽 - kanekoayano.wav
C♯ minor
12A
123
平田志穂子 - Backside Of The TV (SPOTISAVER).mp3
C minor
5A
100
平田志穂子 - Signs Of Love (SPOTISAVER).mp3
A♯ minor
3A
105
平田志穂子, Lotus Juice - Dance! (SPOTISAVER).mp3
E minor
9A
134
最終列車は25時.mp3
B major
1B
130
来兎 - Blood Drain -Again- (Eltnum Theme) (SPOTISAVER).mp3
A minor
8A
95
炉心融解 feat.鏡音リン Meltdown feat.Kagamine Rin.mp3
C♯ minor
12A
82
避けられぬ戦い (P3R ver.).mp3
G♯ minor
1A
90
避けられぬ戦い.mp3
G♯ minor
1A
90
abc100"""
