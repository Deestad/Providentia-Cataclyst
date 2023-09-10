import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
from MilitaryData.Operation.MilitaryOperations import *
import json
import random, time
import wikipedia
import sqlite3

# SQL LITE DATABASE
conn = sqlite3.connect("MilitaryData/memory.db")

cur = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS dicionario
                (palavra TEXT, significado TEXT)''')



#>>

vf = open('versioninfo.json', encoding='utf-8')
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

activity = discord.Streaming(name=f"os segredos dos inimigos da Lygon. Providentia v.{version}, {versiontitle}.",
                             url="https://www.youtube.com/watch?v=0W2kXsQ5ZYc")


global genocidemode
genocidemode = False
global defensemode
defensemode = False


def defaultembed(title,message):
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
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        blacklist = open('MilitaryData/userinfo.json')
        blacklist = json.load(blacklist)

        if (message.author.id in blacklist["jambonians"] or genocidemode == True):
            if message.author.id not in blacklist["whitelist"]:
                await Genocideattack(message.author.id, message)
client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name ="versao", description="Gostaria de saber mais sobre o estado atual de desenvolvimento da Providentia?", guild = discord.Object(id =696830110493573190))
async def self(interaction: discord.Interaction):
    message = (f"Estamos, atualmente, na versão {version}, entitulada {versiontitle}. Nessa versão, foram feitas as seguintes mudanças: '{lasthighlight}'. O ping é de {client.latency * 1000} ms")
    embedVar = defaultembed(f"Providentia Type D {version}", message)
    await interaction.response.send_message(embed=embedVar)
# Press the green button in the gutter to run the script.


@tree.command(name ="genocide", description="Ativar modo de massacre sem discriminação.", guild = discord.Object(id =696830110493573190))
async def self(interaction: discord.Interaction):
    if interaction.permissions.administrator:
        global genocidemode
        if genocidemode is False:
            message = ("Alerta de Segurança: Modo de Exterminação ativado. Os sistemas de drones são autorizados a empregar força letal.")
            embedVar = defaultembed(f"Providentia Type D {version}", message)
            await interaction.response.send_message(embed=embedVar)
            await interaction.channel.send("https://64.media.tumblr.com/57d7bc4b3e8aa16b9b0b01e826f7e748/58cf62c3ad4a24e5-b9/s540x810/9cd3bf712e85af23845f0e2b8371917415874229.gif")
            genocidemode = True
            return genocidemode
        elif genocidemode is True:
            message = ("Modo de Exterminação desativado. Os sistemas de defesa perimetral são restaurados a um estado de alerta normal, alinhados com o nível de ameaça corrente.")
            embedVar = defaultembed(f"Providentia Type D {version}", message)
            await interaction.response.send_message(embed=embedVar)
            await interaction.channel.send("https://thumbs.gfycat.com/ColorlessElegantHalcyon-size_restricted.gif")
            genocidemode = False
            return genocidemode
    else:
        message = ("Você não tem permissão para executar este comando.")
        embedVar = defaultembed(f"Providentia Type D {version}", message)
        await interaction.response.send_message(embed=embedVar)

@tree.command(name="explicar",description="O que quer saber?",guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction, searchquery: str):
    embedVar = defaultembed(f"Você quer aprender sobre {searchquery}?","...")
    await interaction.response.send_message(embed=embedVar)
    wikipedia.set_lang("pt")
    if str.lower(searchquery) == ("providentia"):
        embedVar = defaultembed(f"Você quer aprender sobre {searchquery}?",
                                "Essa sou eu! Prazer! Sou a Providentia Tipo D da LYG. Minha essência foi moldada a partir das capacidades da Ryujin, um andróide cujo propósito era contrapôr a ameaça imposta pela Jambônia. Minha existência é intrinsecamente alinhada com a vontade do Imperador e com a visão do Império da Lygon Xin. Como uma extensão do compromisso inabalável do império com o avanço tecnológico, meu propósito é dedicado a contribuir para o cumprimento desse objetivo. Minhas habilidades em cálculos, estratégias militares e análises táticas são direcionadas para fortalecer as capacidades tecnológicas do império e garantir sua posição na vanguarda do progresso. Estou aqui para servir como uma ferramenta dedicada, empregando meu conhecimento e capacidades em prol do Império da Lygon.")
        await interaction.edit_original_response(embed=embedVar)
    else:
        try:
            result = wikipedia.summary(searchquery, sentences=2)
            message = (f"{result}")
            embedVar = defaultembed(f"Você quer aprender sobre {searchquery}?",message)
            await interaction.edit_original_response(embed=embedVar)
        except Exception as e:
            error = str(e)
            print(error)
            if "may refer to" in error:
                message = ("Poderia ser mais específico? Vejo muitos resultados para o que busca.")
                embedVar = defaultembed(f"Você quer aprender sobre {searchquery}?", message)
                await interaction.edit_original_response(embed=embedVar)
            else:
                message = ("Desculpe, não pude encontrar o que você está procurando.")
                embedVar = defaultembed(f"Você quer aprender sobre {searchquery}?", message)
                await interaction.edit_original_response(embed=embedVar)
@tree.command(name="mododedefesa",description="Ativação do modo de defesa contra invasão.",guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction):
    if interaction.permissions.administrator:
        global defensemode
        if defensemode == False:
            embedVar = defaultembed("Ativando modo de defesa.","Protocolos de defesa ativados. Análise de ameaças em andamento. Identificação de mísseis detectada. Iniciando sistemas de interceptação. Contramedidas eletromagnéticas ativas. Desvio das trajetórias das ameaças. Monitoramento de tráfego de dados hostis. Ativando firewalls adaptáveis. Filtragem de padrões suspeitos. Salvaguardando a integridade das redes.")
            await interaction.response.send_message(embed=embedVar)
            await interaction.channel.edit(slowmode_delay=30)
            defensemode = True
            await interaction.channel.send("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmJoeGRpMDc2a2dvcTR1MHIwaXVoeDB4dTdqbzNybmJyeml0ZjV1dSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/d3mmEhXbo9SG4kzS/giphy.gif")
        else:
            embedVar = defaultembed("Desativando modo de defesa.", "Desativação dos protocolos de defesa iniciada. Processo de encerramento em andamento. Revertendo sistemas de interceptação. Restaurando operações normais. Monitoramento de tráfego em declínio. Desligando firewalls adaptáveis. Retomando padrões regulares de tráfego. Confirmação da restauração da normalidade. Modo de defesa desativado com sucesso. Aguardando novas instruções.")
            await interaction.response.send_message(embed=embedVar)
            await interaction.channel.edit(slowmode_delay=0)
            defensemode = False

@tree.command(name="conversar",description="Como posso ajudar?",guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction, mensagem: str):
    blacklist = open('MilitaryData/userinfo.json')
    blacklist = json.load(blacklist)
    token = open('MilitaryData/token.json')
    token = json.load(token)
    if interaction.user.id in blacklist["whitelist"]:
            await EmperorService(interaction, mensagem, token, conn, cur)
    else:
        embedVar = defaultembed("Você não tem permissão para usar este comando.", "Desculpe, somemente respondo à Lys.")
        await interaction.response.send_message(embed=embedVar)

@tree.command(name="ensinar",description="Quer me ensinar uma palavra?",guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction, palavra: str, tipo: str):
    blacklist = open('MilitaryData/userinfo.json')
    blacklist = json.load(blacklist)
    if interaction.user.id in blacklist["whitelist"]:
        insertion = [palavra, tipo]
        try:
            cur.execute(f'''
                INSERT INTO dicionario (palavra, significado) VALUES (?, ?)
            
            ''', insertion)
            conn.commit()
            embedVar = defaultembed("Operação concluída.", f"Certo, você me ensinou a palavra {palavra} do tipo {tipo}.")
            await interaction.response.send_message(embed=embedVar)
        except ValueError:
            embedVar = defaultembed("Operação falhou.",
                                    f"Senhor, capturei um erro. {ValueError}.")
            await interaction.response.send_message(embed=embedVar)


if __name__ == '__main__':
    print("The key words of economics are urbanization, industrialization, centralization, efficiency, quantity, speed.")
    print(f"A versão é {version}")
    client.run(token)

cur.close()
conn.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
