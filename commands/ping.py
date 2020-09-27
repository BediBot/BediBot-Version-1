
async def ping(msg):
    print("pong")
    await msg.channel.send("pong!")
