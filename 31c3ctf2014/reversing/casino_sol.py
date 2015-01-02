#!/usr/bin/python2
#12/27/2014
#morgan

import telnetlib
import sys
import time

def combine(list1, list2):
    indexes = [10,9,8,7,6,5,4,3,2,1,0]
    for i in indexes:
        sub2 = list2[0:i]
        sub1 = list1[-i:]
        if sub2 == sub1:
            return list1+list2[i:]
    return list1+list2

def send_guess(tc_ans,lis,index):
    for i in range(index,index+5):#sending 5 each time
        print "account"
        tc_ans.write("account\n")
        ret = tc_ans.read_until("\n")
        account = ret.strip().split()[-2]
        if int(account) > 1000000:
            print "flag"
            tc_ans.write("flag\n")
            ret = tc_ans.read_until("\n")
            print ret,
            sys.exit()
        print ret,
        bet = "I bet " + account + " and guess "+str(lis[i])
        print bet,
        tc_ans.write(bet+"\n")
        ret = tc_ans.read_until("\n")
        print ret,

def main():
    lis = []
    index = 0
    tc_ans = None

    while True:
        tmp = []
        tc = telnetlib.Telnet("188.40.18.77",2000)
        ret = tc.read_until("\n")
        #print ret,
        for i in range(10):
            #print "I bet 1 and guess 1"
            tc.write("I bet 1 and guess 1\n")
            ret = tc.read_until("\n")
            #print ret,
            num = ret.strip().split()[-1]
            #print num
            tmp.append(num)

        ret = tc.read_until("\n")
        #print ret,
        lis = combine(lis,tmp)
        print lis

        if index == 0:
            tc_ans = telnetlib.Telnet("188.40.18.77",2000)
            ret = tc_ans.read_until("\n")
            print ret,
            bet = "I bet 1 and guess 1"
            print bet,
            tc_ans.write(bet+"\n")
            ret = tc_ans.read_until("\n")
            print ret,
            num = ret.strip().split()[-1]
            index  = lis.index(num)+1
            #print "the first index is",index
        send_guess(tc_ans,lis,index)
        index += 5
        time.sleep(20)
    ret = tc.read_until("\n")
    #print ret,

if __name__ == "__main__":
    main()
