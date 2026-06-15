TempoTable = [[101],[102],[103],[103.3594, 105.4688, 105.4688, 105], [151.9991, 99.384, 99.384, 150],]


# slow tempo location finder, will find the
def table_locator(query):
    curr = 0
    while query != TempoTable[curr][-1]:
        curr += 1
    return curr

def getCell(index):
    return TempoTable[index]