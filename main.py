import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
import json
vf = open('versioninfo.json')
versioninfo = json.load(vf)
version = versioninfo["version"]
versiontitle = versioninfo["versiontitle"]
prefix = versioninfo["prefix"]
lasthighlight = versioninfo["lasthighlight"]

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Streaming(name=f"Prefixo: {prefix} - Providentia v.{version}, {versiontitle}.",
                             url="https://www.youtube.com/watch?v=0W2kXsQ5ZYc")
def DefaultEmbed(title,message):
    embedVar = discord.Embed(title=f"{title}", description=f"{message}", color=0xb603fc)
    return embedVar

class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id =696830110493573190))

client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name ="versao", description="Gostaria de saber mais sobre o estado atual de desenvolvimento da Providentia?", guild = discord.Object(id =696830110493573190))
async def self(interaction: discord.Interaction):
    message = (f"Estamos, atualmente, na versão {version}, entitulada {versiontitle}. Nessa versão, foram feitas as seguintes mudanças: '{lasthighlight}'. O ping é de {client.latency * 1000} ms")
    embedVar = DefaultEmbed(f"Providentia Type D {version}", message)
    await interaction.response.send_message(embed=embedVar)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"A versão é {version}")
    client.run('OTE1MjQ4NjkyOTYzOTg3NDc5.Ghcwlm.lRrZihmIKBzeocxGeWxPzxz3GKtbRV75B-nQOU')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
