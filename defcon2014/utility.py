#5/17/2014
import copy

def get_score_list():
    score_list = []
    for z in range(3):          #24
        score_list.append([(0,0,z),(0,1,z),(0,2,z)])
        score_list.append([(1,0,z),(1,1,z),(1,2,z)])
        score_list.append([(2,0,z),(2,1,z),(2,2,z)])
        score_list.append([(0,0,z),(1,0,z),(2,0,z)])
        score_list.append([(0,1,z),(1,1,z),(2,1,z)])
        score_list.append([(0,2,z),(1,2,z),(2,2,z)])
        score_list.append([(0,0,z),(1,1,z),(2,2,z)])
        score_list.append([(0,2,z),(1,1,z),(2,0,z)])

    for i in range(2):  #9
        for j in range(2):
            if i == j:
                score_list.append([(i,j,0),(i,j,1),(i,j,2)])

    #another 16
    score_list.append([(0,0,0),(0,1,1),(0,2,2)])
    score_list.append([(1,0,0),(1,1,1),(1,2,2)])
    score_list.append([(2,0,0),(2,1,1),(2,2,2)])
    score_list.append([(0,0,0),(1,0,1),(2,0,2)])
    score_list.append([(0,1,0),(1,1,1),(2,1,2)])
    score_list.append([(0,2,0),(1,2,1),(2,2,2)])
    score_list.append([(0,0,0),(1,1,1),(2,2,2)])
    score_list.append([(0,2,0),(1,1,1),(2,0,2)])

    score_list.append([(0,0,2),(0,1,1),(0,2,0)])
    score_list.append([(1,0,2),(1,1,1),(1,2,0)])
    score_list.append([(2,0,2),(2,1,1),(2,2,0)])
    score_list.append([(0,0,2),(1,0,1),(2,0,0)])
    score_list.append([(0,1,2),(1,1,1),(2,1,0)])
    score_list.append([(0,2,2),(1,2,1),(2,2,0)])
    score_list.append([(0,0,2),(1,1,1),(2,2,0)])
    score_list.append([(0,2,2),(1,1,1),(2,0,0)])
    return score_list

score_list = get_score_list()


def convert_open_list(open_all):
    new_list = []
    for i in range(9):
        if len(open_all[i])>0:
            if i in [0,1,2]:
                z = 0
            elif i in [3,4,5]:
                z = 1
            elif i in [6,7,8]:
                z = 2
            for j in open_all[i]:
                new_list.append((j[0],j[1],z))
    return new_list


#state can be xlist, olist and openlist
def minimax(xlis, olis, openlis): #return the next move (a tuple)
    max_val = -1000
    depth = 0
    best_move = None
    for move in openlis:    #move is a tuple
        tmp = min_value(result(xlis,olis,openlis,move,'X'),depth)#deep copy all the lists, or remove and append
        #print "tmp",tmp
        if tmp > max_val:
            max_val = tmp
            best_move = move
    return best_move


def min_value(state,depth):#return the difference of the score
    depth += 1
    xlis = state[0]
    olis = state[1]
    openlis = state[2]

    if len(openlis) == 0 or depth >=2:
        xs,os = get_score(score_list,xlis,olis) #score_list should be global
        return xs - os
    min_value = 1000
    for move in openlis:
        tmp = max_value(result(xlis,olis,openlis,move,'O'),depth)
        if tmp < min_value:
            min_value = tmp
    return min_value


def max_value(state,depth):#return the difference of the score
    depth += 1
    xlis = state[0]
    olis = state[1]
    openlis = state[2]
    #print "len",len(openlis)

    if len(openlis) == 0 or depth >=2:
        xs,os = get_score(score_list,xlis,olis) #score_list should be global
        return xs - os
    max_value = -1000
    for move in openlis:
        tmp = min_value(result(xlis,olis,openlis,move,'X'),depth)
        if tmp > min_value:
            max_value = tmp
    return max_value


def result(xlis,olis,openlis,move,player):
    openlis2 = copy.deepcopy(openlis)
    openlis2.remove(move)
    xlis2 = copy.deepcopy(xlis)
    olis2 = copy.deepcopy(olis)
    if player == 'X':
        xlis2.append(move)
    if player == 'O':
        olis2.append(move)

    return (xlis2,olis2,openlis2)


def get_score(score_list,xlis,olis): #input:score_list + 2 lists of a tuples; ret:tuple of(x_score,o_score)
    record = [0 for i in range(49)]
    for xi in range(len(xlis)):
        for  si in range(len(score_list)):
            if xlis[xi] in score_list[si]:
                record[si] += 1
    x_score = 0
    for r in record:
        if r == 3:
            x_score += 1

    record = [0 for i in range(49)]
    for oi in range(len(olis)):
        for  si in range(len(score_list)):
            if olis[oi] in score_list[si]:
                record[si] += 1
    o_score = 0
    for r in record:
        if r == 3:
            o_score += 1

    return (x_score,o_score)
    #print "scores ", x_score,o_score


def get_pos_list(rows,sym): #tuple of 9 rows, sym is 'O' or 'X'
    z = 0
    pos_list = []  #list of tuples
    for i in range(0,9,3):
        for j in range(3):
            row = rows[i+j]
            lis = row.split()
            if sym in lis:
                if len(lis) == 3:
                    index = lis.index(sym)
                    pos_list.append((j,index,z))
                elif len(lis) == 4:
                    for k in range(len(lis)):
                        if lis[k] == sym:
                            if k == 0:
                                pos_list.append((j,0,z))
                            if (k==1) or (k==2):
                                pos_list.append((j,1,z))
                            if (k==3) :
                                pos_list.append((j,2,z))
                elif len(lis) == 5:
                    for k in range(len(lis)):
                        if lis[k] == sym:
                            if k==0:
                                pos_list.append((j,0,z))
                            if k==2:
                                pos_list.append((j,1,z))
                            if k==4:
                                pos_list.append((j,2,z))
        z += 1

    return pos_list
