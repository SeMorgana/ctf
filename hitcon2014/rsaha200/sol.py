#8/16/2014
#http://en.wikipedia.org/wiki/Coppersmith%27s_Attack#Franklin-Reiter_Related_Message_Attack
import gmpy
import telnetlib

def main():
    tn = telnetlib.Telnet("54.64.40.172",5454)

    for i in range(10):
        ret = tn.read_until("\n")
        ret2 = tn.read_until("\n")
        ret3 = tn.read_until("\n")
        print ret[:-1]
        print ret2[:-1]
        print ret3[:-1]

        n = int(ret[:-1])
        c1 = int(ret2)
        c2 = int(ret3)
        f = (c2 + 2*c1 -1) % n
        g = (c2 - c1 +2) % n

        m = gmpy.divm(f,g,n)

        print '\nsending:  ',m
        tn.write(str(m)+"\n")
        feedback = tn.read_until("\n")
        print feedback
    print m
    print ""
    print hex(int(m)).rstrip("L").lstrip("0x").decode("hex")

if __name__ == "__main__":
    main()
