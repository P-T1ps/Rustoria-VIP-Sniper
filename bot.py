import time

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
roles_prefix = "Rustoria "


@client.event
async def on_ready():
    print("Ready")
    checker.start()


@client.event
async def on_message(message):
    contents = message.content
    author = message.author
    guild = client.get_guild(874007431527686154)
    roles = {
        "usmain": discord.utils.get(guild.roles, id=874013034195066932),
        "usmedium": discord.utils.get(guild.roles, id=874007919451066458),
        "uslong": discord.utils.get(guild.roles, id=874013139816054806),
        "ussmall": discord.utils.get(guild.roles, id=874013079476768819),

        "eumain": discord.utils.get(guild.roles, id=874018564523307018),
        "eumedium": discord.utils.get(guild.roles, id=874018668344901672),
        "eulong": discord.utils.get(guild.roles, id=874018735122423830),
        "eusmall": discord.utils.get(guild.roles, id=874022194257219595)
    }
    if contents.startswith("."):
        contents = contents.split(".", 1)[1]
        if contents in roles:
            role = roles[contents]
            if role in author.roles:
                await author.remove_roles(role)
            else:
                await author.add_roles(role)


@tasks.loop(seconds=15)
async def checker():
    try:
        guild = client.get_guild(874007431527686154)
        roles = {
            "usmain": discord.utils.get(guild.roles, id=874013034195066932),
            "usmedium": discord.utils.get(guild.roles, id=874007919451066458),
            "uslong": discord.utils.get(guild.roles, id=874013139816054806),
            "ussmall": discord.utils.get(guild.roles, id=874013079476768819),

            "eumain": discord.utils.get(guild.roles, id=874018564523307018),
            "eumedium": discord.utils.get(guild.roles, id=874018668344901672),
            "eulong": discord.utils.get(guild.roles, id=874018735122423830),
            "eusmall": discord.utils.get(guild.roles, id=874022194257219595)
        }
        data_functions = {
            roles["usmain"]: [
                                [
                                    rustoria_us_main,
                                    rustoria_us_main_wipe
                                ],
                                discord.utils.get(guild.roles, id=874013034195066932)],
            roles["usmedium"]: [
                                [
                                    rustoria_us_medium
                                ],
                                discord.utils.get(guild.roles, id=874007919451066458)],
            roles["uslong"]: [
                                [
                                    rustoria_us_long
                                ],
                                discord.utils.get(guild.roles, id=874013139816054806)],
            roles["ussmall"]: [
                                [
                                    rustoria_us_small
                                ],
                                discord.utils.get(guild.roles, id=874013079476768819)],

            roles["eumain"]: [
                                [
                                    rustoria_eu_main
                                ],
                                discord.utils.get(guild.roles, id=874018564523307018)],
            roles["eumedium"]: [
                                [
                                    rustoria_eu_medium
                                ],
                                discord.utils.get(guild.roles, id=874018668344901672)],
            roles["eulong"]: [
                                [
                                    rustoria_eu_long
                                ],
                                discord.utils.get(guild.roles, id=874018735122423830)],
            roles["eusmall"]: [
                                [
                                    rustoria_eu_small
                                ],
                                discord.utils.get(guild.roles, id=874022194257219595)],
        }

        occupied_roles = [role for role in roles.values() if role.members]
        for role in occupied_roles:
            do_break = False
            for i in data_functions[role][0]:
                if do_break:
                    break
                function_data = i([tools])
                if function_data["in_stock"]:
                    do_break = True
                    for member in role.members:
                        embed = discord.Embed()
                        embed.title = function_data['title']
                        embed.set_image(url=dict(function_data)['img'])
                        embed.url = "https://donate.rustoria.co/packages.php?game=<GM>&server=<SVR>".replace(
                            "<GM>", dict(function_data)['game']).replace("<SVR>", dict(function_data)['server'])
                        embed.description = discord_styler(dict(function_data)['description'])
                        a = dict(function_data)['price']
                        price_str = str(a) + "0" if len(str(a).split(".")[1]) == 1 else str(a)
                        embed.add_field(name="Price", value="$" + price_str, inline=True)
                        embed.add_field(name="Duration", value=str(int(float(function_data['expires']))) + " Days")

                        await member.send(embed=embed)
                        await member.remove_roles(role)
    except Exception as e:
        print(e, time.time())

client.run(token)
