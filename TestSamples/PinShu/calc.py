def calc(score: list[int], judger_max_score: int) -> list[int]:
    ret = []
    for i in score:
        ret.append(i/judger_max_score*50)
    ret.append((score[0]+score[1])/judger_max_score*50)
    return ret
