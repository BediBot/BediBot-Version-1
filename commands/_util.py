

def parseMessage(msg):
    ignoreSpace = False
    args = []
    start = 0
    for x in range(len(msg)):
        if msg[x] == ' ' and not ignoreSpace and not x == start:
            args.append(msg[start:x])
            start = x+1
        elif msg[x] == '"' and not ignoreSpace:
            start = x+1
            ignoreSpace = True
        elif msg[x] == '"' and ignoreSpace and x != start +1:
            args.append(msg[start:x])
            start = x+1
            ignoreSpace = False
        elif x == len(msg)-1:
            args.append(msg[start:len(msg)])
    return args


#args = parseMessage('$com "arg1 space" arg2')
#print(args)