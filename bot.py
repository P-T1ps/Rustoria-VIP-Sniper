import discord
from discord.ext import commands
from discord.ext import tasks
from servers.rustoria import *
from tools.functions import convert_gbp_usd as tools
from tools.functions import discord_styler


token = open('token', 'r').read()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    print("Ready")
    checker.start()


@client.command()
async def usmedium(ctx):
    role_name = "VIP US Medium"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def uslong(ctx):
    role_name = "VIP US Long"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def ussmall(ctx):
    role_name = "VIP US Small"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def usmain(ctx):
    role_name = "VIP US Main"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def eumedium(ctx):
    role_name = "VIP EU Medium"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def eulong(ctx):
    role_name = "VIP EU Long"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def eusmall(ctx):
    role_name = "VIP EU Small"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@client.command()
async def eumain(ctx):
    role_name = "VIP EU Main"
    user = ctx.author
    user_roles = ctx.author.roles
    target_role = discord.utils.get(ctx.message.guild.roles, name=role_name)
    for role in user_roles:
        if role.name == role_name:
            await user.remove_roles(target_role)
            return
    await user.add_roles(target_role)


@tasks.loop(minutes=1)
async def checker():
    picker_channel = client.get_channel(874007831546830898)
    data = {
        "us_main": [rustoria_us_main([tools]), "VIP US Main"],
        "us_medium": [rustoria_us_medium([tools]), "VIP US Medium"],
        "us_long": [rustoria_us_long([tools]), "VIP US Long"],
        "us_small": [rustoria_us_small([tools]), "VIP US Small"],

        "eu_main": [rustoria_eu_main([tools]), "VIP EU Main"],
        "eu_medium": [rustoria_eu_medium([tools]), "VIP EU Medium"],
        "eu_long": [rustoria_eu_long([tools]), "VIP EU Long"],
        "eu_small": [rustoria_eu_small([tools]), "VIP EU Small"]
    }
    guild = client.get_guild(874007431527686154)
    for x in data:
        in_stock = dict(data[x][0])["in_stock"]
        if in_stock:
            embed = discord.Embed()
            embed.title = data[x][1]
            embed.url = "https://donate.rustoria.co/packages.php?game=<GM>&server=<SVR>".replace(
                "<GM>", dict(data[x][0])['game']).replace("<SVR>", dict(data[x][0])['server'])
            embed.description = discord_styler(dict(data[x][0])['description'])
            embed.add_field(name="Price", value="$" + str(dict(data[x][0])['price']), inline=True)
            role = discord.utils.get(guild.roles, name=data[x][1])
            for member in guild.members:
                if role in member.roles:
                    await member.send(embed=embed,
                                      content=f"{member.mention}, if you don't buy this in time reassign your role "
                                              f"in {picker_channel.mention}!")
                    await member.remove_roles(role)

client.run(token)
