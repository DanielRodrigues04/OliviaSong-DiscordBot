from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def custom_help(self, ctx):
        await ctx.send("Lista de comandos disponíveis: !join, !leave, !ping")

async def setup(bot):
    await bot.add_cog(Utility(bot))
