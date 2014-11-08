#5/17/2014
import telnetlib
import random
from utility import *

tn = telnetlib.Telnet("3dttt_87277cd86e7cc53d2671888c417f62aa.2014.shallweplayaga.me",1234)

X = 'X'
O = 'O'

def get_sym(coor): #sym => symmetric
    if coor == 0:
        return 2
    if coor == 1:
        return 1
    if coor == 2:
        return 0


def get_move(new_O_pos):
    x,y,z = new_O_pos       #x,y are in wrong order
    return (get_sym(x),get_sym(y),get_sym(z))


def get_new_pos(pre,cur):
    for i in cur:
        if not (i in pre):
            return i

        
def is_all_empty(open_all):
    ret = True
    for i in range(9):
        ret = ret and (len(open_all[i]) == 0)
    return ret


def get_next_open(open_all): #open_all: tuple of list of tuples
    valid = []
    for i in range(9):
        if len(open_all[i])>0:
            if i in [0,1,2]:
                z = 0
            elif i in [3,4,5]:
                z = 1
            elif i in [6,7,8]:
                z = 2
            for j in open_all[i]:
                valid.append((j[0],j[1],z))

    index = random.randint(0,len(valid)-1)
    return valid[index]
            #return (open_all[i][0][0],open_all[i][0][1],z)


def get_empty(row1,row_num):
    open_list =[]   #list of tuples
    lis = row1.split()
    if len(lis) == 2:
        open_list.append((row_num,0));
        open_list.append((row_num,1));
        open_list.append((row_num,2));
    elif len(lis) == 3:
        if X in lis:
            index = lis.index(X)
            if index == 0:
                open_list.append((row_num,1))
                open_list.append((row_num,2))
            elif index == 1:
                open_list.append((row_num,0))
                open_list.append((row_num,2))
            elif index == 2:
                open_list.append((row_num,0))
                open_list.append((row_num,1))
        elif O in lis:
            index = lis.index(O)
            if index == 0:
                open_list.append((row_num,1))
                open_list.append((row_num,2))
            elif index == 1:
                open_list.append((row_num,0))
                open_list.append((row_num,2))
            elif index == 2:
                open_list.append((row_num,0))
                open_list.append((row_num,1))
    elif len(lis) == 4:
        if lis[0] == '|':
            open_list.append((row_num,0))
        elif lis[3] == '|':
            open_list.append((row_num,2))
        else:
            open_list.append((row_num,1))
    return open_list


def main():
    score_list = get_score_list()
    turns = 0
    pre_Olist = []  #list of tuples
    cur_Olist = []  #same above
    while True:
        ret = tn.read_until("y\n")
        print ret
        tn.read_until("0")
        row00 = tn.read_until("\n").strip()
        tn.read_until("1") #skip
        row01 = tn.read_until("\n").strip()
        tn.read_until("2") #skip
        row02 = tn.read_until("\n").strip()

        ret = tn.read_until("y\n")
        tn.read_until("0")
        row10 = tn.read_until("\n").strip()
        tn.read_until("1") #skip
        row11 = tn.read_until("\n").strip()
        tn.read_until("2") #skip
        row12 = tn.read_until("\n").strip()

        ret = tn.read_until("y\n")
        tn.read_until("0")
        row20 = tn.read_until("\n").strip()
        tn.read_until("1") #skip
        row21 = tn.read_until("\n").strip()
        tn.read_until("2") #skip
        row22 = tn.read_until("\n").strip()
        
        #print row00
        #print row01
        #print row02
        #print ""
        open0 = (get_empty(row00,0), get_empty(row01,1), get_empty(row02,2))

        #print row10
        #print row11
        #print row12
        #print ""
        open1 = (get_empty(row10,0), get_empty(row11,1), get_empty(row12,2))

        #print row20
        #print row21
        #print row22
        open2 = (get_empty(row20,0), get_empty(row21,1), get_empty(row22,2))

        rows = (row00,row01,row02,row10,row11,row12,row20,row21,row22)

        ret = tn.read_some()
        print ret


        open_all = (open0[0],open0[1],open0[2],open1[0],open1[1],open1[2],open2[0],open2[1],open2[2])
        open_list = convert_open_list(open_all)

        if is_all_empty(open_all):
            ret = tn.read_some()
            print ret
            pre_Olist = []
            cur_Olist = []
            turns = 0
            #return
            continue
        y,x,z = get_next_open(open_all)

        Xlist = get_pos_list(rows,'X')
        Olist = get_pos_list(rows,'O')
        next_move = minimax(Xlist,Olist,open_list)
        print "next move", next_move
        #get_score(score_list,Xlist,Olist)
        

        if turns==0:
            send = "1,1,1"
            cur_Olist = get_pos_list(rows,'O')
            turns += 1
        else:
            pre_Olist = cur_Olist;
            cur_Olist = get_pos_list(rows,'O')
            new_pos = get_new_pos(pre_Olist,cur_Olist)
            #y,x,z = get_move(new_pos)

            y,x,z = next_move

            send = str(x)+","+str(y)+","+str(z) 
        print "sending ",send
        tn.write(send+"\n")
        

if __name__=="__main__":
    main()
