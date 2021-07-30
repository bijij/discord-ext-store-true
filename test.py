import os

from discord.ext import commands, store_true

class MyBot(store_true.StoreTrueMixin, commands.Bot):
    ...


class TestFlags(commands.FlagConverter, prefix='--', delimiter=' '):
    a: bool = False
    c: str


bot = MyBot(command_prefix="(d!)")

@bot.command()
async def foo(ctx, *, flag: TestFlags):
    await ctx.send(flag.a)


bot.run(os.getenv("BOT_TOKEN"))
