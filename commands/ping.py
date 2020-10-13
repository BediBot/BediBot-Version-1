
async def ping(ctx, client):
    print("pong")
    await ctx.channel.send("pong!")
    