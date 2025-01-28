from discord.ext import commands

# Define um cog vazio ou com comandos se necessário
class InitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def init_command(self, ctx):
        await ctx.send("Comando de inicialização do cog __init__")

# A função setup é necessária para o carregamento do cog
async def setup(bot):
    await bot.add_cog(InitCog(bot))
