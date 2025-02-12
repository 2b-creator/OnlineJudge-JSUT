def calc(score, judger_max_score):
    ret = []
    for i in score:
        ret.append(i/judger_max_score*50)
    ret.append((score[0]+score[1])/judger_max_score*50)
    return ret
