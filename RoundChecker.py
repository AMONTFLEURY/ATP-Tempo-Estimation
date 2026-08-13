def check(tempo, score, bias='up'):
    half_time = min(tempo)
    double_time = max(tempo)
    x = double_time / half_time
    if 1.89 < x < 2.19:
        half_time = half_checker(half_time, double_time, 0.5)
    if double_time / half_time == 2:
        return [double_time, half_time]
    else:
        tempo[rolling_star(score, tempo)] = None
        return tempo


def rolling_star(score, tempo):
    if score[0] > score[1]:
        return 1
    elif score[0] < score[1]:
        return 0
    else:
        return tie_breaker(tempo)


def half_checker(half_time, double_time, i):
    if double_time / (half_time + i) == 2:
        return half_time + i
    elif double_time / (half_time - i) == 2:
        return half_time - i
    else:
        return half_time


def tie_breaker(tempo):
    if abs(tempo[0] - 120) > abs(tempo[1] - 120):
        return 1
    else:
        return 0
