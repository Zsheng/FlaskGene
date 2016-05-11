# coding=utf-8
import sys


def NWDistance(seedSequence, candidateSequence):
    s = -1  # 错配
    m = 1  # 匹配
    g = -2  # 空缺
    seedSequence = seedSequence.strip()
    candidateSequence = candidateSequence.strip()
    if len(seedSequence) == 0:
        print "Error, seed sequence length equal zero."
        sys.exit(1)
    elif len(candidateSequence) == 0:
        print "Error, candidate sequence length equal zero."
        sys.exit(1)

    sLen = len(seedSequence)
    cLen = len(candidateSequence)
    table = []
    # 构建一个二位矩阵，填充第一行第一列（m*g/n*g）
    for m in range(0, len(seedSequence) + 1):
        table.append([m * g])
    table[0] = []
    for n in range(0, len(candidateSequence) + 1):
        table[0].append(n * g)

    # 两个循环，从第一行开始确定该空格的值，其中该值为max(上，左，左上+（匹配的分数或不匹配的分数）)
    for i in range(sLen):
        for j in range(cLen):
            table[i + 1].append(
                    max(
                            table[i][j] + (m if seedSequence[i] == candidateSequence[j] else s),
                            table[i][j + 1] + g,
                            table[i + 1][j] + g,
                    )
            )

    # 回溯
    # 若ai=bj，则回溯到左上角单元格
    # 若ai≠bj，回溯到左上角、上边、左边中值最大的单元格，若有相同最大值的单元格，优先级按照左上角、上边、左边的顺序
    # 若当前单元格是在矩阵的第一行，则回溯至左边的单元格
    # 若当前单元格是在矩阵的第一列，则回溯至上边的单元格
    i = sLen - 1
    j = cLen - 1
    NewSeed = seedSequence[i]
    NewCandidate = candidateSequence[j]
    if len(seedSequence) <= 1 or len(candidateSequence) <= 1:
        print "Error, too short!"
        sys.exit(1)
    while True:
        if i == 0 and j == 0:
            break
        if seedSequence[i] == candidateSequence[j]:
            if table[i - 1][j - 1] + 1 > table[i - 1][j] - 2 and table[i - 1][j - 1] + 1 > table[i][j - 1] - 2:
                i = i - 1
                j = j - 1
                NewSeed = u"%s%s" % (seedSequence[i], NewSeed)
                NewCandidate = u"%s%s" % (candidateSequence[j], NewCandidate)
            else:
                if table[i][j + 1] > table[i + 1][j]:
                    i = i - 1
                    NewSeed = u"%s%s" % (seedSequence[i], NewSeed)
                    NewCandidate = u"%s%s" % ('-', NewCandidate)
                else:
                    j = j - 1
                    NewSeed = u"%s%s" % ('-', NewSeed)
                    NewCandidate = u"%s%s" % (candidateSequence[j], NewCandidate)
        else:
            if table[i - 1][j - 1] + 1 > table[i - 1][j] - 2 and table[i - 1][j - 1] + 1 > table[i][j - 1] - 2:
                i = i - 1
                j = j - 1
                NewSeed = u"%s%s" % (seedSequence[i], NewSeed)
                NewCandidate = u"%s%s" % (candidateSequence[j], NewCandidate)
            else:
                if table[i][j + 1] > table[i + 1][j]:
                    i = i - 1
                    NewSeed = u"%s%s" % (seedSequence[i], NewSeed)
                    NewCandidate = u"%s%s" % ('-', NewCandidate)
                else:
                    j = j - 1
                    NewSeed = u"%s%s" % ('-', NewSeed)
                    NewCandidate = u"%s%s" % (candidateSequence[j], NewCandidate)

    # distance
    mismath = 0
    math = 0
    gap = 0
    charZipList = zip(NewSeed, NewCandidate)
    # delete the head gap
    for n in range(len(charZipList)):
        if "-" in charZipList[n]:
            del charZipList[0]
        else:
            break
    # delete the tail gap
    while True:
        lastTuple = charZipList.pop()
        if "-" in lastTuple:
            continue
        else:
            charZipList.append(lastTuple)
            break
    #
    for n in range(len(charZipList)):
        charTuple = charZipList[n]
        if charTuple[0] == charTuple[1]:
            math += 1
        elif "-" in charTuple:
            gapLoc = charTuple.index("-")
            if charZipList[n + 1][gapLoc] == "-":
                continue
            else:
                gap += 1
        else:
            mismath += 1
    distance = round(1.0 - float(math) / float(mismath + math + gap), 4)
    print NewSeed
    print NewCandidate
    return distance

if __name__ == '__main__':
    print NWDistance('atgc', 'atgc')
