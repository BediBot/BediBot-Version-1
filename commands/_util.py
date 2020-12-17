def parse_message(msg):
    ignoreSpace = False
    args = []
    start = 0
    for x in range(len(msg)):
        if msg[x] == ' ' and not ignoreSpace and not x == start:
            args.append(msg[start:x].strip())
            start = x + 1
        elif msg[x] == '"' and not ignoreSpace:
            start = x + 1
            ignoreSpace = True
        elif msg[x] == '"' and ignoreSpace:
            args.append(msg[start:x].strip())
            ignoreSpace = False
            start = x + 1
        elif x == len(msg) - 1:
            args.append(msg[start:len(msg)].strip())
    return args

# args = parseMessage('$com "2 3" arg2')
# print(args)
