import discord
from discord.ext import commands
import json
vf = open('versioninfo.json')
versioninfo = json.load(vf)
version = versioninfo["version"]
versiontitle = versioninfo["versiontitle"]
prefix = versioninfo["prefix"]

intents = discord.Intents.default()
intents.message_content = True



activity = discord.Streaming(name=f"Prefixo: {prefix} - Providentia v.{version}, {versiontitle}.",
                             url="https://www.youtube.com/watch?v=0W2kXsQ5ZYc")
client = discord.Client(intents=intents, command_prefix=prefix, activity=activity, status=discord.Status.idle)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"A versão é {version}")
    client.run('OTE1MjQ4NjkyOTYzOTg3NDc5.Ghcwlm.lRrZihmIKBzeocxGeWxPzxz3GKtbRV75B-nQOU')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
