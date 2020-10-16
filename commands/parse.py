from ._util import parseMessage

async def parseCommand(ctx, client):
    args = parseMessage(ctx.content)
    msg = ""
    num = 0
    for arg in args:
        msg += "arg " + str(num) + " : " + arg + "\n"
        num += 1
    await ctx.channel.send(msg)



