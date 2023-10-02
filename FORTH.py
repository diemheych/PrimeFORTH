#PYTHON name
#
#   forth.py
#
#   Copyright © 2021 Chris Meyers and Fred Obermann
#   http://openbookproject.net/py4fun/forth/forth.html
#
#   2023, Modified by Darren Hosking, aka. Calculator Clique
#   Ported to HP Prime, Added many words (math, graphics,...)
#   License added.
#   See:
#   - [diemheych/PrimeFORTH: A simple version of FORTH written in Python for the HP Prime calculator](https://github.com/diemheych/PrimeFORTH)
#   - [HP Prime runs FORTH in Python - YouTube](https://www.youtube.com/watch?v=ILMbia3-VZo)
#
import sys, math
import hpprime
import graphic
import urandom

if sys.version > '3' : raw_input = input  # for both 2.7 and 3.0+

ds       = []          # The data stack
cStack   = []          # The control struct stack
heap     = [0]*2048      # The data heap
heapNext =  0          # Next avail slot in heap
words    = []          # The input stream of tokens
colour   = 0x0000ff
background = 0xffffff
initCode = """: cr 10 emit ; : abs dup 0 < if 0 swap - then ; : constant create , does> @ ; : variable create 1 allot ; : +! DUP @ ROT + SWAP ! ;
: 2DUP OVER OVER ; : 2DROP DROP DROP ; : NIP SWAP DROP ; : 2NIP 2SWAP 2DROP ; : TUCK SWAP OVER ;
 : BL 32 ; : CR 10 EMIT ; : SPACE BL EMIT ; : NEGATE 0 SWAP - ; : DNEGATE 0. 2SWAP D- ; : CELLS CELL * ; : TRUE -1 ; : FALSE 0 ;
 : 0= 0 = ; : 0< 0 < ; : 0> 0 > ; : <= > 0= ; : >= < 0= ; : 0<= 0 <= ; : 0>= 0 >= ; : 1- 1 - ;
: 2+ 2 + ; : 2- 2 - ; : 2/ 2 / ; : 2* 2 * ; : MIN 2DUP < IF DROP ELSE NIP THEN ; : MAX 2DUP > IF DROP ELSE NIP THEN ; : D0= OR 0= ; 1 constant CELL
"""

def main() :
    global words, initCode
    if len(sys.argv) > 1 :
        initCode = open(sys.argv[1]).read()   # load start file
    hpprime.eval("PRINT") # clear terminal screen
    print("Prime FORTH 1.0")
    while True :
        pcode = compile()          # compile/run from user
        if pcode == None : print(""); return
        execute(pcode)

#============================== Lexical Parsing
        
def getWord (prompt="... ") :
    global words, initCode
    while not words :
        try :
            if initCode : lin = initCode; initCode=""
            else        :
                lin = raw_input(prompt)+" "
                print(lin)
        except : return None
        tokenizeWords(lin)

    word = words[0]
    if word == "bye" : return None
    words = words[1:]
    return word

def tokenizeWords(s) :
    global words                                          # clip comments, split to list of words
    words += s.lower().split()  # Use "#" for comment to end of line

#================================= Runtime operation

def execute (code) :
    p = 0
    while p < len(code) :
        func = code[p]
        p += 1
        newP = func(code,p)
        if newP != None : p = newP

def rAdd (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a+b)
def rFloor (cod,p) : a=ds.pop(); ds.append(math.floor(a))
def rMod (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a%b)
def rOneplus (cod,p) : a=ds.pop(); ds.append(a+1)
def rOr (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a|b)
def rAnd (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a&b)
def rMul (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a*b)
def rSub (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a-b)
def rDiv (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(a/b)
def rEq  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a==b))
def rPixon (cod,p) : y=ds.pop(); x=ds.pop(); hpprime.pixon(0,x,y,colour)
def rPixon2 (cod,p) :
    y=ds.pop();
    if y > 0 : y = y * 2 + 1
    x=ds.pop()
    if x > 0 : x = x * 2 + 1
    hpprime.pixon(0,x,y,colour);
    hpprime.pixon(0,x+1,y,colour);
    hpprime.pixon(0,x,y+1,colour);
    hpprime.pixon(0,x+1,y+1,colour)

def rPixon4 (cod,p) :
    y=ds.pop();
    if y > 0 : y = y * 4 + 1
    x=ds.pop()
    if x > 0 : x = x * 4 + 1
    hpprime.fillrect(0,x,y,4, 4, colour, colour);

def rGetpix (cod,p) : y=ds.pop(); x=ds.pop(); ds.append(hpprime.eval("getpix_p({},{})".format(x,y)))

def rGetpix2 (cod,p) :
    y=ds.pop();
    if y > 0 : y = y * 2 + 1
    x=ds.pop()
    if x > 0 : x = x * 2 + 1
    ds.append(hpprime.eval("getpix_p({},{})".format(x,y)))

def rGetpix4 (cod,p) :
    y=ds.pop();
    if y > 0 : y = y * 4 + 1
    x=ds.pop()
    if x > 0 : x = x * 4 + 1
    ds.append(hpprime.eval("getpix_p({},{})".format(x,y)))

def rLastkey (cod,p) : ds.append(int(hpprime.eval("getkey")))

def rKey (cod,p) :
    while 1:
        k = hpprime.eval("getkey")
        if k != -1 : break

    ds.append(int(k))
def rTicks (cod,p) : ds.append(int(hpprime.eval("ticks")))
def rLine (cod,p) : y2=ds.pop(); x2=ds.pop(); y1=ds.pop(); x1=ds.pop(); hpprime.line(0,x1,y1,x2, y2, colour)
def rRect (cod,p) : h=ds.pop(); w=ds.pop(); y=ds.pop(); x=ds.pop(); hpprime.rect(0,x,y,w, h, colour)
def rFillrect (cod,p) : h=ds.pop(); w=ds.pop(); y=ds.pop(); x=ds.pop(); hpprime.fillrect(0,x,y,w, h, colour, colour)
def rCircle (cod,p) : rad=ds.pop(); y=ds.pop(); x=ds.pop(); hpprime.circle(0,x,y,rad, colour)
def rCol (cod,p) : global colour ; colour = ds.pop()
def rGetcol (cod,p) : global colour; ds.append(colour)
def rBg (cod,p) : global background; background = ds.pop()
def rShow (cod,p) : graphic.show()
def rList (cod,p) :
    fname = getWord()+".fth";
    try:
        f = open(fname, "r")
        print(f.read(), end=''); f.close()
    except:
        print(fname+": does not exist")

def rLoad (cod,p) :
    global initCode
    fname = getWord()+".fth"
    try:
        f = open(fname, "r")
        initCode = f.read()
        f.close()
    except:
        print(fname+": does not exist")

def rSleep (cod,p) : a=ds.pop()/1000; hpprime.eval("wait({})".format(a))
def rNeq  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a!=b))
def rGt  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a>b))
def rLt  (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a<b))
def rLtE (cod,p) : b=ds.pop(); a=ds.pop(); ds.append(int(a<=b))
def rSqr (cod,p) : a=ds.pop(); ds.append(math.sqrt(a))
def rCos (cod,p) : a=ds.pop(); ds.append(math.cos(a))
def rRandom (cod,p) : a=ds.pop(); ds.append(urandom.randint(0,a-1))
def rSwap(cod,p) : a=ds.pop(); b=ds.pop(); ds.append(a); ds.append(b)
def rRot(cod,p) : a=ds.pop(); b=ds.pop(); c=ds.pop(); ds.append(b); ds.append(a); ds.append(c)
def rDup (cod,p) : ds.append(ds[-1])
def rDrop(cod,p) : ds.pop()
def rOver(cod,p) : ds.append(ds[-2])
def rDump(cod,p) : print("ds = %s" % ds)
def rDdump(cod,p) : print(rDict)
def rIdump(cod,p) : print(imDict)
def rDot (cod,p) : print(ds.pop(),end=' ')
def rEmit (cod,p) : print(chr(ds.pop()&255),end='')
def rHere(cod,p) : ds.append(heapNext)
def rJmp (cod,p) : return cod[p]
def rJnz (cod,p) : return (cod[p],p+1)[ds.pop()]
def rJz  (cod,p) : return (p+1,cod[p])[ds.pop()==0]
def rRun (cod,p) :
    if cod[p] in rDict:
        execute(rDict[cod[p]])
    else:
        print(cod[p]," unknown")
    return p+1

def rPush(cod,p) : ds.append(cod[p])     ; return p+1
def rCls(cod,p) : graphic.clear_screen(background); hpprime.eval("print")
def rSin(cod,p) : a=ds.pop(); ds.append(math.sin(a))
def rCos(cod,p) : a=ds.pop(); ds.append(math.cos(a))
def rTan(cod,p) : a=ds.pop(); ds.append(math.tan(a))
def rAsin(cod,p) : a=ds.pop(); ds.append(math.asin(a))
def rAcos(cod,p) : a=ds.pop(); ds.append(math.acos(a))
def rAtan(cod,p) : a=ds.pop(); ds.append(math.atan(a))
def rSqrt(cod,p) : a=ds.pop(); ds.append(math.sqrt(a))

def rgtR(cod,p) :
    a=ds.pop()
    cStack.append(("NUMBER",a))

def rRgt(cod,p) :
    name,value=cStack.pop()
    ds.append(value)

def rRat(cod,p) :
    name,value = cStack.pop()
    cStack.append((name,value))
    ds.append(value)

def rJ (cod,p) :
    c1,t1 = cStack.pop()
    c2,t2 = cStack.pop()
    c3,t3 = cStack.pop()
    cStack.append((c3,t3))
    cStack.append((c2,t2))
    cStack.append((c1,t1))
    ds.append(t3)

def rWord (cod,p) :
    word=getWord()
    for c in word :
        ds.append(ord(c))
    ds.append(len(word))

def rType (cod,p) :
    len = ds.pop()
    addr = ds.pop()
    print("addr ",addr,len)
    for i in range(0, len) :
        print(chr(heap[addr+i]&0x7f),end="")

def rImmediate(cod,p) :
    imDict[list(rDict.keys())[-1]] = 1

def rWords(cod,p) :
    for k in sorted(list(rDict.keys())): print(k,end=' ')

def rCreate (pcode,p) :
    global heapNext, lastCreate
    lastCreate = label = getWord()      # match next word (input) to next heap address
    rDict[label] = [rPush, heapNext]    # when created word is run, pushes its address

def rDoes (cod,p) :
    rDict[lastCreate] += cod[p:]        # rest of words belong to created words runtime
    return len(cod)                     # jump p over these

def rAllot (cod,p) :
    global heapNext
    heapNext += ds.pop()                # reserve n words for last create

def rAt  (cod,p) : ds.append(heap[ds.pop()])       # get heap @ address
def rBang(cod,p) : a=ds.pop(); heap[a] = ds.pop()  # set heap @ address
def rComa(cod,p) :                                 # push tos into heap
    global heapNext
    heap[heapNext]=ds.pop()
    heapNext += 1

rDict = {
  '+'  : rAdd, '-'   : rSub, '/' : rDiv, '*'    : rMul,   'over': rOver,
  'dup': rDup, 'swap': rSwap, '.': rDot, 'dump' : rDump,  'drop': rDrop,
  '='  : rEq,  '>'   : rGt,   '<': rLt,
  ','  : rComa,'@'   : rAt, '!'  : rBang,'allot': rAllot,

  'create': rCreate, 'does>': rDoes,
'or' : rOr,
'and' : rAnd,
'emit' : rEmit,
'<>' : rNeq,
'here' : rHere,
'rot' : rRot,
'pixon' : rPixon,
'pixon2' : rPixon2,
'pixon4' : rPixon4,
'getpix' : rGetpix,
'getpix2' : rGetpix2,
'getpix4' : rGetpix4,
'key' : rKey,
'lastkey' : rLastkey,
'ticks' : rTicks,
'line' : rLine,
'rect' : rRect,
'fillrect' : rFillrect,
'circle' : rCircle,
'sleep' : rSleep,
'cls' : rCls,
'col' : rCol,
'getcol' : rGetcol,
'bg' : rBg,
'show' : rShow,
'list' : rList,
'load' : rLoad,
'<>' : rNeq,
'here' : rHere,
'rot' : rRot,
'sin' : rSin,
'cos' : rCos,
'random' : rRandom,
'tan' : rTan,
'asin' : rAsin,
'acos' : rAcos,
'atan' : rAtan,
'sqrt' : rSqrt,
'words' : rWords,
'R@' : rRat,
'1+' : rOneplus,
'>r' : rgtR,
'r>' : rRgt,
'j' : rJ,
'type' : rType,
'word' : rWord,
'ddump' : rDdump,
'idump' : rIdump,
'immediate' : rImmediate,
'lte' : rLtE,
}
#================================= Compile time

def compile() :
    global ds
    pcode = []; prompt = "Ok " if len(ds)==0 else "Ok: "
    while 1 :
        word = getWord(prompt)  # get next word
        if word == None : return None
        cAct = cDict.get(word)  # Is there a compile time action ?
        rAct = rDict.get(word)  # Is there a runtime action ?

        if cAct : cAct(pcode)   # run at compile time
        elif rAct :
            if type(rAct) == type([]) :
                pcode.append(rRun)     # Compiled word.
                pcode.append(word)     # for now do dynamic lookup
            else : pcode.append(rAct)  # push builtin for runtime
        else :
            # Number to be pushed onto ds at runtime
            pcode.append(rPush)
            try : pcode.append(int(word))
            except :
                try: pcode.append(float(word))
                except :
                    pcode[-1] = rRun     # Change rPush to rRun
                    pcode.append(word)   # Assume word will be defined
        if not cStack : return pcode
        prompt = "...    "

def fatal (mesg) : raise mesg

def cColon (pcode) :
    if cStack : fatal(": inside Control stack: %s" % cStack)
    label = getWord()
    cStack.append(("COLON",label))  # flag for following ";"

def cSemi (pcode) :
    if not cStack : fatal("No : for ; to match")
    code,label = cStack.pop()
    if code != "COLON" : fatal(": not balanced with ;")
    rDict[label] = pcode[:]       # Save word definition in rDict
    while pcode : pcode.pop()

def cBegin (pcode) :
    cStack.append(("BEGIN",len(pcode)))  # flag for following UNTIL

def cUntil (pcode) :
    if not cStack : fatal("No BEGIN for UNTIL to match")
    code,slot = cStack.pop()
    if code != "BEGIN" : fatal("UNTIL preceded by %s (not BEGIN)" % code)
    pcode.append(rJz)
    pcode.append(slot)

def cWhile (pcode) :
    if not cStack : fatal("No BEGIN for WHILE to match")
    pcode.append(rJz)

def cRepeat (pcode) :
    if not cStack : fatal("No BEGIN for REPEAT to match")

def cDo (pcode) :
    cStack.append(("DO",len(pcode)))  # flag for following UNTIL
    pcode.append(rSwap)
    pcode.append(rgtR)
    pcode.append(rgtR)

def cLoop (pcode) :
    if not cStack : fatal("No DO for LOOP to match")
    code,slot = cStack.pop()
    if code != "DO" : fatal("LOOP preceded by %s (not DO)" % code)
    pcode.append(rRgt)
    pcode.append(rRgt)
    pcode.append(rSwap)
    pcode.append(rOneplus)
    pcode.append(rOver)
    pcode.append(rOver)
    pcode.append(rEq)
    pcode.append(rJz)
    pcode.append(slot)
    pcode.append(rDrop)
    pcode.append(rDrop)

def cLoopPlus (pcode) :
    if not cStack : fatal("No DO for LOOP to match")
    code,slot = cStack.pop()
    if code != "DO" : fatal("+LOOP preceded by %s (not DO)" % code)
    pcode.append(rRgt)
    pcode.append(rRgt)
    pcode.append(rSwap)
    pcode.append(rRot)
    pcode.append(rAdd)
    pcode.append(rOver)
    pcode.append(rOver)
    pcode.append(rSwap)
    pcode.append(rLt)
    pcode.append(rJz)
    pcode.append(slot)
    pcode.append(rDrop)
    pcode.append(rDrop)

def cI (pcode) :
    pcode.append(rRat)

def cJ (pcode) :
    pcode.append(rRgt)
    pcode.append(rRgt)
    pcode.append(rRgt)
    pcode.append(rDup)
    pcode.append(rgtR)
    pcode.append(rSwap)
    pcode.append(rgtR)
    pcode.append(rSwap)
    pcode.append(rgtR)

def cIf (pcode) :
    pcode.append(rJz)
    cStack.append(("IF",len(pcode)))  # flag for following Then or Else
    pcode.append(0)                   # slot to be filled in

def cElse (pcode) :
    if not cStack : fatal("No IF for ELSE to match")
    code,slot = cStack.pop()
    if code != "IF" : fatal("ELSE preceded by %s (not IF)" % code)
    pcode.append(rJmp)
    cStack.append(("ELSE",len(pcode)))  # flag for following THEN
    pcode.append(0)                     # slot to be filled in
    pcode[slot] = len(pcode)            # close JZ for IF

def cThen (pcode) :
    if not cStack : fatal("No IF or ELSE for THEN to match")
    code,slot = cStack.pop()
    if code not in ("IF","ELSE") : fatal("THEN preceded by %s (not IF or ELSE)" % code)
    pcode[slot] = len(pcode)             # close JZ for IF or JMP for ELSE

cDict = {
  ':'    : cColon, ';'    : cSemi, 'if': cIf, 'else': cElse, 'then': cThen,
  'begin': cBegin, 'until': cUntil,
'do': cDo, 'loop': cLoop, '+loop' : cLoopPlus, 'i' : cI , 'j' : cJ , 'while' : cWhile, 'repeat' : cRepeat,
}

if __name__ == "__main__" : main()
#END
EXPORT FORTH()
BEGIN
PYTHON(name);
END;