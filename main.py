import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
from MilitaryData.Operation.MilitaryOperations import *
import json
import random, time
vf = open('versioninfo.json')
opentoken = open("MilitaryData/token.json")

#VERSION INFO ORG
versioninfo = json.load(vf)
tokenfile = json.load(opentoken)
token = tokenfile["token"]
version = versioninfo["version"]
versiontitle = versioninfo["versiontitle"]
prefix = versioninfo["prefix"]
lasthighlight = versioninfo["lasthighlight"]
intents = discord.Intents.default()
intents.message_content = True

activity = discord.Streaming(name=f"Prefixo: {prefix} - Providentia v.{version}, {versiontitle}.",
                             url="https://www.youtube.com/watch?v=0W2kXsQ5ZYc")
global genocidemode
genocidemode = False

def DefaultEmbed(title,message):
    embedVar = discord.Embed(title=f"{title}", description=f"{message}", color=0xb603fc)
    embedVar.set_author(name="PLYG-7X42", icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9f1ed69b-9e98-4f78-acda-c95c6f4be159/db73tp3-8c5589a6-051c-4408-b244-f451c599b04d.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlmMWVkNjliLTllOTgtNGY3OC1hY2RhLWM5NWM2ZjRiZTE1OVwvZGI3M3RwMy04YzU1ODlhNi0wNTFjLTQ0MDgtYjI0NC1mNDUxYzU5OWIwNGQuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.7X4JjtqAwnetH9HC9f4sl3kcik8VCFCE5nr1MGB607M")
    return embedVar

class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id =696830110493573190))
    async def on_message(self, message):
        blacklist = open('MilitaryData/enemyinfo.json')
        blacklist = json.load(blacklist)

        if (message.author.id in blacklist["jambonians"] or genocidemode == True):
            if message.author.id not in blacklist["whitelist"]:
                await Genocideattack(message.author.id, message)
client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name ="versao", description="Gostaria de saber mais sobre o estado atual de desenvolvimento da Providentia?", guild = discord.Object(id =696830110493573190))
async def self(interaction: discord.Interaction):
    message = (f"Estamos, atualmente, na versão {version}, entitulada {versiontitle}. Nessa versão, foram feitas as seguintes mudanças: '{lasthighlight}'. O ping é de {client.latency * 1000} ms")
    embedVar = DefaultEmbed(f"Providentia Type D {version}", message)
    await interaction.response.send_message(embed=embedVar)
# Press the green button in the gutter to run the script.


@tree.command(name ="genocide", description="Ativar modo de massacre sem discriminação.", guild = discord.Object(id =696830110493573190))
async def self(interaction: discord.Interaction):
    global genocidemode
    if genocidemode is False:
        message = ("Alerta de Segurança: Modo de Exterminação ativado. Os sistemas de drones são autorizados a empregar força letal, conforme diretrizes estabelecidas.")
        embedVar = DefaultEmbed(f"Providentia Type D {version}", message)
        await interaction.response.send_message(embed=embedVar)
        await interaction.channel.send("https://64.media.tumblr.com/57d7bc4b3e8aa16b9b0b01e826f7e748/58cf62c3ad4a24e5-b9/s540x810/9cd3bf712e85af23845f0e2b8371917415874229.gif")
        genocidemode = True
        return genocidemode
    elif genocidemode is True:
        message = ("Modo de Exterminação desativado. Os sistemas de defesa perimetral são restaurados a um estado de alerta normal, alinhados com o nível de ameaça corrente.")
        embedVar = DefaultEmbed(f"Providentia Type D {version}", message)
        await interaction.response.send_message(embed=embedVar)
        await interaction.channel.send("https://thumbs.gfycat.com/ColorlessElegantHalcyon-size_restricted.gif")
        genocidemode = False
        return genocidemode

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    print(f"A versão é {version}")
    client.run(token)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
