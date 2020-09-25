async def ping(msg, bot):
    print("pong")
    await msg.channel.send("pong!")
    