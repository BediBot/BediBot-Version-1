import discord
from discord.ext import commands

from utils import guild


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: discord.Message):
        response = "Pong! **{0}ms**\n Guilds: **{1}**\n Users: **{2}**".format(int(self.bot.latency * 1000), guild.get_guild_count(self.bot),
                                                                               guild.get_member_count(self.bot))
        await ctx.send(response)


def setup(bot):
    bot.add_cog(GeneralCog(bot))
