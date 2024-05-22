import btree
# import fontdatac
# import json
# font_ditc={'1':fontdatac.one,'2':fontdatac.two,'3':fontdatac.three,'4':fontdatac.four,'5':fontdatac.five,
#           '6':fontdatac.six,'7':fontdatac.seven,'8':fontdatac.eight,'9':fontdatac.nine,'0':fontdatac.zero,
#           'A':fontdatac.A,'B':fontdatac.B,'C':fontdatac.C,'D':fontdatac.D,'E':fontdatac.E,
#           'F':fontdatac.F,'G':fontdatac.G,'H':fontdatac.H,'I':fontdatac.I,'J':fontdatac.J,
#           'K':fontdatac.K,'L':fontdatac.L,'M':fontdatac.M,'N':fontdatac.N,'O':fontdatac.O,
#           'P':fontdatac.P,'Q':fontdatac.Q,'R':fontdatac.R,'S':fontdatac.S,'T':fontdatac.T,
#           'U':fontdatac.U,'V':fontdatac.V,'W':fontdatac.W,'X':fontdatac.X,'Y':fontdatac.Y,
#           'Z':fontdatac.Z,' ':fontdatac.block0,'a':fontdatac.a,'b':fontdatac.b,'c':fontdatac.c,
#           'd':fontdatac.d,'e':fontdatac.e,'f':fontdatac.f,'g':fontdatac.g,'h':fontdatac.h,
#           'i':fontdatac.i,'j':fontdatac.j,'k':fontdatac.k,'l':fontdatac.l,'m':fontdatac.m,
#           'n':fontdatac.n,'o':fontdatac.o,'p':fontdatac.p,'q':fontdatac.q,'r':fontdatac.r,
#           's':fontdatac.s,'t':fontdatac.t,'u':fontdatac.u,'v':fontdatac.v,'w':fontdatac.w,
#           'x':fontdatac.x,'y':fontdatac.y,'z':fontdatac.z,'@':fontdatac.xiao,'#':fontdatac.ku,'$':fontdatac.ai,
#           '%':fontdatac.feng,'^':fontdatac.cat,'&':fontdatac.dog,
#           }
def update_db(state_name:bytes,value:bytes):
    try:
        f = open("mydb", "r+b")
    except OSError:
        f = open("mydb", "w+b")
    db = btree.open(f)
    db[state_name]=value
    db.flush()
    db.close()
    f.close()
def read_db(state_name:bytes):
    try:
        f = open("mydb", "r+b")
    except OSError:
        f = open("mydb", "w+b")
    db = btree.open(f)
    try:
        value=db[state_name]
    except:
        f.close()
        db.close()
        return [False,0]
    else:
        f.close()
        db.close()
        return [True,value]
def init_db():
    try:
        f = open("mydb", "r+b")
    except OSError:
        f = open("mydb", "w+b")
    db = btree.open(f)
    db[b'start_code_state']=b'1'
    db[b'light_state']=b'1'
    db[b'duty']=b'0'
    db[b'sound_state']=b'1'
    db[b'num_data']=b'0000'
    db[b'pairing']=b'0'
    # for i in font_ditc:
    #     print(i)
    #     db[i]=json.dumps(font_ditc[i])
    db.flush()
    db.close()
    f.close()
if not (bool(read_db(b'light_state')[0]) and bool(read_db(b'sound_state')[0]) and bool(read_db(b'start_code_state')[0]) and bool(read_db(b'duty')[0]) and bool(read_db(b'num_data')[0])):
    print('initdb')
    init_db()