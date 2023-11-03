import ast
import datetime
import typing
import openai
import elevenlabs
import requests
import re
from requests import get

from comandos import *
import discord
import sympy
from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
import json
import random, time
import wikipedia
import sqlite3
import os, io
import numpy as np
from sympy import *
import statistics
import typing
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from urllib import parse, request

conn = sqlite3.connect("MilitaryData/memory.db")
cur = conn.cursor()
global teaching_mode
global teaching_dialogue

# CONSTANTS
TEMP = "temp"

if os.path.exists(TEMP) and os.path.isdir(TEMP):
    for filename in os.listdir(TEMP):
        file_path = os.path.join(TEMP, filename)
        os.remove(file_path)
else:
    os.mkdir(TEMP)


class MainExecution:

    def __init__(self):

        self.intents = None
        self.version_title = None
        self.version = None
        self.version_info = None
        self.activity = None
        self.setversioninfo()
        self.setuserinfo()
        self.initializedatabase()

    def checkwhitelist(self, userid):
        userid = str(userid)
        try:
            whitelisted = cur.execute(f'''SELECT userid FROM whitelist
                                                        WHERE userid = (?)
    
                                                            ''', (userid,)).fetchone()
            if whitelisted:
                print("Whitelisted user used a command.")
                return True
        except ValueError:
            return False
        except Exception as err:
            print(err)

    def initializedatabase(self):
        cur.execute('''
                            CREATE TABLE IF NOT EXISTS frases(entrada TXT, saida1 TXT, saida2 TXT, saida3 TXT);
                ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS whitelist(userid INT);
        ''')
        cur.execute('''
                            CREATE TABLE IF NOT EXISTS rps(titulo TEXT, descricao TEXT, autor TEXT, imagem TEXT);
                ''')

        cur.execute('''
                                    CREATE TABLE IF NOT EXISTS fichaRP(titulorp TEXT, jogador TEXT, nomepersonagem TEXT, personalidade TEXT, idade TEXT, habilidades TEXT, aparencia TEXT, historia TEXT, imagem TEXT, genero TEXT);
                        ''')
        cur.execute('''
                                            CREATE TABLE IF NOT EXISTS censura(palavra TEXT);
                                ''')

    def tokenload(self):
        if os.path.isfile("token.json") and os.access("token.json", os.R_OK):
            print("Token detected.")
            token = open("token.json")
            token = json.load(token)
            token = token["token"]
            openai_token = open("token.json")
            openai_token = json.load(openai_token)
            openai.api_key = openai_token['openaitoken']
            elevenlabs_token = open("token.json")
            elevenlabs_token = json.load(elevenlabs_token)
            elevenlabs_token = elevenlabs_token['elevenlabsapikey']
            elevenlabs.set_api_key(elevenlabs_token)
            return token
        else:
            token = input("Inform the token to activate Providentia. \n")
            openai.api_key = input("Inform the OpenAI token. This one is necessary for talking operations.\n")
            elevenlabs_token = input("Insert token for voice application. ElevenLabs. \n")
            try:
                elevenlabs.set_api_key(elevenlabs_token)
            except Exception as e:
                print(e)
            data = {
                'token': token,
                'openaitoken': openai.api_key,
                "elevenlabsapikey": elevenlabs_token
            }
            with open("token.json", "w") as file:
                json.dump(data, file, indent=4)
            token = open("token.json")
            token = json.load(token)
            token = token["token"]
            return token

    def setuserinfo(self):
        user_info = open("MilitaryData/userinfo.json")
        user_info = json.load(user_info)
        return user_info

    def callIntents(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        intents = self.intents
        return intents

    def setversioninfo(self):
        version_info = open('versioninfo.json', encoding='utf-8')
        self.version_info = json.load(version_info)
        self.version = self.version_info["version"]
        self.version_title = self.version_info["versiontitle"]

        return self.version_info

    def defaultembed(self, title, message):

        self.embed_configuration = discord.Embed(title=f"{title}", description=f"{message}", color=0x2ecc71)
        self.embed_configuration.set_author(name="PLYG-7X42",
                                            icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9f1ed69b-9e98-4f78-acda-c95c6f4be159/db73tp3-8c5589a6-051c-4408-b244-f451c599b04d.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlmMWVkNjliLTllOTgtNGY3OC1hY2RhLWM5NWM2ZjRiZTE1OVwvZGI3M3RwMy04YzU1ODlhNi0wNTFjLTQ0MDgtYjI0NC1mNDUxYzU5OWIwNGQuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.7X4JjtqAwnetH9HC9f4sl3kcik8VCFCE5nr1MGB607M")
        return self.embed_configuration


listaderps = cur.execute(f'''
            SELECT titulo, autor FROM rps
        ''').fetchone()
censura = cur.execute('''SELECT palavra FROM censura;

        ''').fetchall()
flat_list = list()
censura = flatten([list(item) for item in censura])
for sub_list in censura:
    flat_list += sub_list


class aclient(discord.Client):

    def __init__(self):
        intents = MainExecution().callIntents()
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
        await self.change_presence(status=discord.Status.dnd, activity=(
            discord.Activity(type=discord.ActivityType.listening, name="aos meios de comunicações inimigos.")))

    async def on_message(self, message):
        whitelisted = MainExecution().checkwhitelist(message.author.id)
        channel = message.channel.name

        # SPYBOT FUNCTIONALITY
        if message.author.id == client.user.id:
            pass
        if str.lower(message.content).__contains__("atir") and str.lower(message.content).__contains__("providentia"):
            await message.channel.send("https://media.tenor.com/Jw8I___MCdQAAAAC/matrix-dodge.gif")
        elif str.lower(message.content).__contains__("atac") or str.lower(message.content).__contains__("bat") and str.lower(message.content).__contains__("providentia"):
            await message.channel.send("https://64.media.tumblr.com/35077a06fa6fd1401500b802d6deee9f/tumblr_om8b32BOzF1rrwrx4o1_500.gif")
        # WHITELIST FUNCTIONS
        if whitelisted:
            if str.lower(message.content).startswith("providentia,"):
                guild = client.get_guild(message.guild.id)
                targets = []
                if str.lower(message.content).__contains__("quantos canais"):
                    guild_length = len(message.guild.channels)
                    await message.channel.send(f"Este servidor tem {guild_length}, senhor.")
                elif str.lower(message.content).__contains__("expuls"):
                    order = str.lower(message.content).split(" ")
                    for word in order:
                        if word.startswith("<@"):
                            targets.append(word)
                    for victim in targets:
                        victim = victim.replace("&", "")
                        victim = victim.replace("<@", "")
                        victim = victim.replace(">", "")
                        victim = guild.get_member(int(victim))
                        try:
                            await discord.Member.kick(victim, reason="Execução.")
                            await message.channel.send(f"Operação concluída. {victim} eliminado.")
                        except Exception as e:
                            print(e)
                            if isinstance(e, commands.MissingPermissions):
                                await message.channel.send(f"Não tenho permissões para executar este comando aqui.")
                            elif isinstance(e, commands.MissingRequiredArgument):
                                await message.channel.send(f"Especifique o alvo, senhor.")
                else:
                    url = "http://api.giphy.com/v1/gifs/search"
                    reaction = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        max_tokens=10,
                        messages=[

                            {"role": "system",
                             "content": "Você é uma automata de destruição. Responda apenas com uma a três palavras a seguinte ordem dada pelo imperador."},
                            {"role": "user",
                             "content": f"Faça uma reação como resposta à ordem dada pelo imperador em duas, no máximo três palavras: {message.content}"}
                        ]

                    )
                    context = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        max_tokens=10,
                        messages=[

                            {"role": "system",
                             "content": "Narrate this scene happens, but just use three "
                                        "words. This will be used to search for a gif in Giphy."},
                            {"role": "user",
                             "content": f"Narrate in three words what happens visually in the scene. Don't say emotions, just literally what happens: {message.content}"}
                        ]

                    )
                    context = context.choices[0].message["content"]
                    context.replace(" ", "-")
                    print(context)
                    params = parse.urlencode({
                        "q": context,
                        "api_key": "8AkWlssazxQ5ohXq3MlOBo2FLPkFDexa",
                        "limit": "5"
                    })
                    with request.urlopen("".join((url, "?", params))) as response:
                        data = json.loads(response.read())
                        gif_url = data['data'][0]['images']['fixed_height']['url']
                    await message.channel.send(f"{reaction.choices[0].message['content']}")
                    await message.channel.send(f"{gif_url}")

        elif channel == "ações" or channel == "aleatorio" or channel == "diplomacia":
            author = message.author.name
            authorimage = message.author.avatar
            security_base = client.get_channel(1165782255168409720)
            embed_configuration = discord.Embed(title=f"Comunicação inimiga detectada: Usuário {author}",
                                                color=discord.Color.random(),
                                                description=f"{message.content}")
            embed_configuration.set_thumbnail(url=authorimage)

            await security_base.send(embed=embed_configuration)
        elif channel == "ficha":
            author = message.author.name
            authorimage = message.author.avatar
            security_base = client.get_channel(1165782255168409720)
            embed_configuration = discord.Embed(title=f"Ficha inimiga detectada:",
                                                color=discord.Color.random(),
                                                description=f"")
            embed_configuration.set_image(url=message.attachments[0].url)

            await security_base.send(embed=embed_configuration)
        else:
            if str.lower(message.content).__contains__("providen") or str.lower(message.content).__contains__("providên"):
                await message.channel.send("https://i.pinimg.com/originals/3f/26/ac/3f26acb731d8e3e7095967ab6a66f570.gif")




# EVENTS

client = aclient()
tree = app_commands.CommandTree(client)
version_info = MainExecution().setversioninfo()
user_info = MainExecution().setuserinfo()

async def lackPermissions(interaction: discord.Interaction):
    await interaction.response.send_message("Desculpe, você não tem permissão para usar este comando.")

@tree.command(name="ajuda",
              description="Listagem dos comandos atualmente disponíveis.",
              )
async def self(interaction: discord.Interaction):
    embed_configuration = discord.Embed(title="Comandos da Providentia:", color=0x2ecc71,
                                        description="Abaixo, você encontrará uma lista das funcionalidades disponíveis.")

    embed_configuration.set_image(
        url="https://camo.githubusercontent.com/019f7739ee9d317a8ce42ce19b4b7070569aea7614313f964bb0bd082cf28062/68747470733a2f2f7062732e7477696d672e636f6d2f6d656469612f455a786a4f6751587341514254354c3f666f726d61743d6a7067266e616d653d6d656469756d")
    embed_configuration.add_field(name="MATEMÁTICA:", value="", inline=False)
    for comando in matematica:
        embed_configuration.add_field(name="", value=f"• /{comando}", inline=False)
    embed_configuration.add_field(name="ROLEPLAY:", value="", inline=False)

    for comando in rp:
        embed_configuration.add_field(name="", value=f"• /{comando}", inline=False)
    embed_configuration.add_field(name="ENTRETENIMENTO:", value="", inline=False)

    for comando in fun:
        embed_configuration.add_field(name="", value=f"• /{comando}", inline=False)

    await interaction.response.send_message(embed=embed_configuration)


@tree.command(name="version",
              description="Gostaria de saber mais sobre o estado atual de desenvolvimento da Providentia?",
              )
async def self(interaction: discord.Interaction):
    message = (
        f'''Estamos, atualmente, na versão {version_info['version']}, entitulada {version_info['versiontitle']}. 
           Nessa versão, foram feitas as seguintes mudanças: '{version_info['lasthighlight']}''')

    embed_configuration = discord.Embed(
        title=f"Providentia Type D {version_info['version']}",
        color=discord.Color.random(),
        description=f"{message}")
    embed_configuration.set_image(
        url="https://steamuserimages-a.akamaihd.net/ugc/2028349797208462796/E03311E21C8EF797E056AA056FF4F7B743AE3B9C/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false")
    embed_configuration.set_footer(text=f"O ping é de {client.latency * 1000} ms")
    presentation = "Dialogues/presentation.mp3"

    await interaction.response.send_message(embed=embed_configuration)
    await interaction.channel.send(file=discord.File(presentation))


@tree.command(name="explain", description="O que quer saber?")
async def self(interaction: discord.Interaction, searchquery: str):
    default_embed = MainExecution().defaultembed
    embedVar = default_embed(f"Você quer aprender sobre {searchquery}?", "...")
    await interaction.response.send_message(embed=embedVar)
    wikipedia.set_lang("pt")
    if str.lower(searchquery) == ("providentia"):
        embedVar = default_embed(f"Você quer aprender sobre {searchquery}?",
                                 "Essa sou eu! Prazer! Sou a Providentia Tipo D da LYG. Minha essência foi moldada a partir das capacidades da Ryujin, um andróide cujo propósito era contrapôr a ameaça imposta pela Jambônia. Minha existência é intrinsecamente alinhada com a vontade do Imperador e com a visão do Império da Lygon Xin. Como uma extensão do compromisso inabalável do império com o avanço tecnológico, meu propósito é dedicado a contribuir para o cumprimento desse objetivo. Minhas habilidades em cálculos, estratégias militares e análises táticas são direcionadas para fortalecer as capacidades tecnológicas do império e garantir sua posição na vanguarda do progresso. Estou aqui para servir como uma ferramenta dedicada, empregando meu conhecimento e capacidades em prol do Império da Lygon.")
        await interaction.edit_original_response(embed=embedVar)
    elif str.lower(searchquery) in censura:
        embedVar = default_embed(f"Opa, que isso?", "Perdões, mas não vou fazer isso, seu engraçadinho.")
        await interaction.edit_original_response(embed=embedVar)
    else:
        try:
            result = wikipedia.summary(searchquery, sentences=2)
            message = f"{result}"
            embedVar = default_embed(f"Você quer aprender sobre {searchquery}?", message)
            await interaction.edit_original_response(embed=embedVar)
            images = wikipedia.page(searchquery).images
            result_image = [image for image in images if f"{searchquery.replace(' ', '')}" and '.svg' not in image][0]
            await interaction.channel.send(result_image)
        except Exception as e:
            error = str(e)
            print(error)
            if "may refer to" in error:
                message = (
                    f"Poderia ser mais específico? Vejo muitos resultados para o que busca. \n \n {str(e).replace('may refer to:', 'pode se referir à:')}")
                embedVar = default_embed(f"Você quer aprender sobre {searchquery}?", message)
                await interaction.edit_original_response(embed=embedVar)
            else:
                message = ("Desculpe, não pude encontrar o que você está procurando.")
                embedVar = default_embed(f"Você quer aprender sobre {searchquery}?", message)
                await interaction.edit_original_response(embed=embedVar)


@tree.command(name="arithmetic",
              description="Resolução de problemas simples de matemática básica.",
              )
async def self(interaction: discord.Interaction, expression: str):
    whitelisted = MainExecution().checkwhitelist(interaction.user.id)
    default_embed = MainExecution().defaultembed
    if whitelisted:
        try:
            resultado = eval(expression)
            embedVar = default_embed(f"Dada a expressão, {expression}:", f"O resultado é: {resultado}")
            await interaction.response.send_message(embed=embedVar)
        except NameError:
            embedVar = default_embed(f"Erro.", f"Insira uma expressão válida.")
            await interaction.response.send_message(embed=embedVar)

    else:
        await lackPermissions(interaction)


@tree.command(name="equation",
              description="Resolução de equações de primeiro grau de uma variável 'x'.",
              )
async def self(interaction: discord.Interaction, leftside: str, equals: int):
    try:
        x = Symbol('x')
        default_embed = MainExecution().defaultembed
        expression = sympy.sympify(leftside)
        equation = solve((expression, equals), x)

        print(expression)
        print(equation)
        equation = equation[x]
        expression_format = str(expression)
        expression_format = expression_format.replace('*x', 'x')

        embedVar = default_embed(f"Dada a equação, {expression_format} = {equals}:",
                                 f"Resultado: {equation}, ou: {N(equation)}")
        await interaction.response.send_message(embed=embedVar)

        default_embed = MainExecution().defaultembed
    except ValueError:
        embedVar = default_embed(f"Erro. {leftside} = {equals} não é uma expressão válida.",
                                 f"Verifique a sintaxe e tente novamente.")
        await interaction.response.send_message(embed=embedVar)


@tree.command(name="average",
              description="Calculo de médias. Separe por vírgulas.")
async def self(interaction: discord.Interaction, items: str):
    try:
        lista_formatada = items
        lista_formatada = lista_formatada.replace(',', ', ')
        items = items.replace(' ', '')
        items = items.split(',')
        numeros = []

        for item in items:
            item = int(item)
            numeros.append(item)
        resultado = statistics.fmean(numeros)
        default_embed = MainExecution().defaultembed

        embedVar = default_embed(f"Para os números, {lista_formatada}:", f"É dada a média {resultado}.")
        await interaction.response.send_message(embed=embedVar)
    except ValueError:
        default_embed = MainExecution().defaultembed
        embedVar = default_embed(f"Valor inválido.", f"Insira uma lista de números separados por vírgulas.")
        await interaction.response.send_message(embed=embedVar)


@tree.command(name="analyze", description="Realizar análise.")
async def self(interaction: discord.Interaction, searchquery: str, searchsize: int,
               searchtarget_id: typing.Optional[str], must_contain: typing.Optional[str],
               create_word_cloud: typing.Optional[bool] = False, providentia: typing.Optional[bool] = False):
    whitelisted = MainExecution().checkwhitelist(interaction.user.id)

    async def sendMessage():
        embed_configuration = discord.Embed(
            title=f"Análise de comunicação inimiga. Autor da ação: {message.author.name}",
            color=discord.Color.random(),
            description=f"{message.content} \n\n Timestamp: {message.created_at}")
        embed_configuration.set_thumbnail(url=message.author.avatar)
        await security_base.send(embed=embed_configuration)

    async def generate_word_cloud(text):
        ustring = (" ").join(text)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(ustring)
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        wordc_file = "temp/word_cloud.jpg"
        plt.savefig(wordc_file)
        await security_base.send(file=discord.File(wordc_file))

    async def thejudgmentofprovidentia(messages):
        dialogue = (" ").join(messages)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Você é Providentia, uma máquina de destruição em massa. Uma agente de Inteligência "
                            "Artificial feito para atacar e destruir os inimigos do Império da Lygon. Você nutre um "
                            "ódio intenso pela Jambônia e acabará com todos que entrarem no seu caminho."},
                {"role": "user", "content": f"Faça uma análise das ações inimigas e me diga estratégias e ações que "
                                            f"eu poderia fazer para se defender contra algumas delas. Somos uma nação distante e sem envolvimento, mas desejamos impedi-los. : \n\n'{dialogue}'"}
            ]
        )
        await security_base.send(completion.choices[0].message["content"])

    if whitelisted:
        enemyinfo = []
        current_wargame = client.get_guild(1150898662982041641)
        security_base = client.get_channel(1165782255168409720)
        for channel in current_wargame.channels:
            if channel.name == searchquery:
                last_messages = [message async for message in channel.history(limit=searchsize)]
                for message in last_messages:
                    if searchtarget_id:
                        if searchtarget_id in str(message.author.id):
                            if must_contain:
                                if message.content.__contains__(must_contain):
                                    await sendMessage()
                                    enemyinfo.append(f"{message.content}")
                                else:
                                    pass
                            else:
                                await sendMessage()
                                enemyinfo.append(f"{message.content}")
                        else:
                            pass
                    else:
                        if must_contain:
                            if message.content.__contains__(must_contain):
                                await sendMessage()
                                enemyinfo.append(f"{message.content}")
                            else:
                                pass
                        else:
                            await sendMessage()
                            enemyinfo.append(f"{message.content}")
        if create_word_cloud:
            await generate_word_cloud(enemyinfo)
        if providentia:
            if providentia and searchquery == "ações" and searchsize < 2:
                await thejudgmentofprovidentia(enemyinfo)
            else:
                await interaction.response.send_message(
                    "Perdões, este comando ainda é bastante limitado. Especifique o canal necessário e use um tamanho de pesquisa menor.")

@tree.command(name="statisticalanalysis", description="Faça uma análise estatística de uma área.")
async def self(interaction: discord.Interaction, searchsize: int, query: str):
    query = str.lower(query)
    whitelisted = MainExecution().checkwhitelist(interaction.user.id)

    async def BuildGraph(messages,time, query):
        plt.bar(month_counts.keys(), month_counts.values())
        plt.xlabel('Mês')
        plt.ylabel(f'Vezes em que {query} foi mencionado')
        plt.xticks(rotation=45)
        plt.title = f"Vezes em que foi dito neste servidor: {query}"
        graph_file = "temp/analysis_graph.jpg"
        plt.savefig(graph_file)
        await interaction.channel.send(file=discord.File(graph_file))

    if whitelisted:
        await interaction.response.send_message("Iniciando análise.")
        analysis_messages = []
        analysis_timestamp = []
        for channel in interaction.guild.channels:
            if isinstance(channel, discord.TextChannel):
                message_history = [message async for message in channel.history(limit=searchsize)]
                for message in message_history:
                    if str.lower(message.content).__contains__(query):
                        analysis_messages.append(message.content)
                        analysis_timestamp.append(message.created_at)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

        # Create a dictionary to store the counts of each month
        month_counts = {month: 0 for month in months}

        # Loop through analysis_messages and count the months
        for message, timestamp in zip(analysis_messages, analysis_timestamp):
            for month in months:
                if month in timestamp.strftime("%B") and str.lower(message).__contains__(query):
                    month_counts[month] += 1





        await BuildGraph(analysis_messages, analysis_timestamp, query)
    else:
        await lackPermissions(interaction)



@tree.command(name="whitelist",
              description="Adicionar usuário a lista de operações da Providentia.",
              )
async def self(interaction: discord.Interaction, userid: str, add_remove: str):
    id = int(userid)
    whitelisted = MainExecution().checkwhitelist(interaction.user.id)
    default_embed = MainExecution().defaultembed
    if whitelisted:
        try:
            if add_remove == 'add':
                whitelist = cur.execute(f'''SELECT userid FROM whitelist
                                            WHERE userid = {userid}

                                                ''').fetchone()
                print(whitelist)
                if not whitelist:
                    try:
                        cur.execute('''
                                    INSERT INTO whitelist (userid) VALUES (?)
                        
                        
                        ''', (id,))
                        conn.commit()
                        embedVar = default_embed(f"Sucesso.", f"<@{userid}> adicionado na Whitelist.")
                        await interaction.response.send_message(embed=embedVar)
                    except ValueError:
                        embedVar = default_embed(f"Valor inválido.", f"Insira um id inteiro.")
                        await interaction.response.send_message(embed=embedVar)
                    except Exception as e:
                        print(e)
                else:
                    embedVar = default_embed(f"Não pude usar este comando.",
                                             f"Usuário já está na Whitelist.")
                    await interaction.response.send_message(embed=embedVar)


            elif add_remove == 'remove':
                id = int(id)
                try:
                    cur.execute(f'''
                                                DELETE FROM whitelist       
                                                WHERE userid = {id};

                                    ''')
                    conn.commit()
                    embedVar = default_embed(f"Sucesso.", f"Usuário removido da Whitelist.")
                    await interaction.response.send_message(embed=embedVar)
                except ValueError:
                    embedVar = default_embed(f"Valor inválido.", f"Insira um id inteiro.")
                    await interaction.response.send_message(embed=embedVar)
                except Exception as e:
                    print(e)
            else:
                pass
        except ValueError:
            embedVar = default_embed(f"Valor inválido.", f"Insira um id inteiro.")
            await interaction.response.send_message(embed=embedVar)
        except Exception as e:
            print(e)
    else:
        await lackPermissions(interaction)


@tree.command(name="censurar",
              description="Censurar palavras para uso do bot.",
              )
async def self(interaction: discord.Interaction, palavra: str):
    palavra = str.lower(palavra)
    palavra = palavra.replace(' ', '')
    palavra = palavra.split(",")
    palavra = [(words,) for words in palavra]
    print(palavra)

    whitelisted = MainExecution().checkwhitelist(interaction.user.id)
    default_embed = MainExecution().defaultembed
    if whitelisted:
        try:
            await interaction.response.send_message("Censurando...")
            cur.executemany('''
                    INSERT INTO censura(palavra) VALUES (?)            
                ''', palavra)
            conn.commit()
            print(f"{len(palavra)} palavras censuradas.")
            conn.commit()
            await interaction.edit_original_response(
                embed=default_embed("Censurado com sucesso.", f"{len(palavra)} palavras censuradas."))
        except Exception as e:
            print(e)


@tree.command(name="confederate", description="Urra")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(
        "https://cdn.discordapp.com/attachments/1165444969641812059/1165445020892008498/Dixie.mp4?ex=6546e041&is=65346b41&hm=ef5b2039c0708574d3844d215cc09626e5bb03af38c11750986a6cdf65947730&")


@tree.command(name="rplistagem", description="Verificar os RPs em progresso.")
async def self(interaction: discord.Interaction):
    embed_configuration = discord.Embed(title="Lista de RPS:", color=0x2ecc71)
    i = 1
    for rp in listaderps:
        rp = str.title(rp)
        embed_configuration.add_field(name=f"{i}.", value=f" {rp}")
        i += 1
    await interaction.response.send_message(embed=embed_configuration)


@tree.command(name="rpnovaficha", description="Adicionar ficha à um RP.",
              )
async def self(interaction: discord.Interaction, nome_rp: str, nome_personagem: str, genero: str, personalidade: str,
               idade: str, habilidades: str, aparencia: str, historia: str, imagem: str):
    nome_rp = str.lower(nome_rp)
    nome_personagem = str.lower(nome_personagem)
    jogador = interaction.user.id

    rpcheck = cur.execute(f'''
        SELECT titulo FROM rps WHERE titulo = ?
    
    
    ''', (nome_rp,)).fetchone()
    print(rpcheck)
    if rpcheck:

        cur.execute('''INSERT into fichaRP (titulorp, jogador, nomepersonagem, personalidade, idade, habilidades, 
        aparencia, historia, imagem, genero) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)


        ''', (
            nome_rp, jogador, nome_personagem, personalidade, idade, habilidades, aparencia, historia, imagem, genero))
        default_embed = MainExecution().defaultembed
        conn.commit()
        embedVar = default_embed("Sucesso.", f"Ficha adicionada.")
        await interaction.response.send_message(embed=embedVar)
    else:
        default_embed = MainExecution().defaultembed
        embedVar = default_embed("Erro", f"Roleplay não existe.")
        await interaction.response.send_message(embed=embedVar)


@tree.command(name="ficharp", description="Verificar ficha de um usuário.")
async def self(interaction: discord.Interaction, nome_rp: str, personagem: str):
    personagem = str.lower(personagem)
    nome_rp = str.lower(nome_rp)

    ficha = cur.execute('''
            SELECT titulorp, jogador, nomepersonagem, personalidade, idade, habilidades, aparencia, historia, imagem, genero
            FROM fichaRP
            WHERE nomepersonagem = ? AND titulorp = ?
        
        ''', (personagem, nome_rp)).fetchone()
    print(ficha)
    embed_configuration = discord.Embed(title=f"{str.upper(ficha[0])} | {str.capitalize(ficha[2])}",
                                        description=f"Idade: {ficha[4]} \n\n **História:** {ficha[7]} \n\n **Personalidade:** {ficha[3]} \n\n **Habi"
                                                    f"lidades:** {ficha[5]}\n\n **Aparência:** {ficha[6]}",
                                        color=0x2ecc71)
    embed_configuration.add_field(name="Jogador:", value=f"<@{ficha[1]}>")
    await interaction.response.send_message(embed=embed_configuration)
    await interaction.channel.send(f"{ficha[8]}")


@tree.command(name="rpinfo",
              description="Verificar as informações de um RP.")
async def self(interaction: discord.Interaction, nome: str):
    nome = str.lower(nome)
    info = cur.execute(f'''
        SELECT titulo, descricao, autor, imagem FROM rps
        WHERE titulo = ? 
    
    
    ''', (nome,)).fetchone()
    embed_configuration = discord.Embed(title=f"{str.title(info[0])}", description=f"{info[1]}", color=0x2ecc71)
    embed_configuration.add_field(name="Autor:", value=f"<@{info[2]}>")
    await interaction.response.send_message(embed=embed_configuration)
    await interaction.channel.send(f"{info[3]}")


@tree.command(name="rpcriar",
              description="Criar um Roleplay (rp).")
async def self(interaction: discord.Interaction, nome: str, descricao: str, imagem: str):
    default_embed = MainExecution().defaultembed
    autor = str(interaction.user.id)
    nome = str.lower(nome)
    try:
        cur.execute('''
                    INSERT INTO rps (titulo, descricao, autor, imagem) VALUES (?, ?, ?, ?)


        ''', (nome, descricao, autor, imagem))
        conn.commit()
        embedVar = default_embed(f"Sucesso.", f"RP {nome} adicionado.")
        await interaction.response.send_message(embed=embedVar)
    except Exception as e:
        print(e)


@tree.command(name="interpretarnpc",
              description="Interprete um personagem.")
async def self(interaction: discord.Interaction, nomenpc: str, titulo: typing.Optional[str],
               image: typing.Optional[str], dialogo: str, ):
    embed_configuration = discord.Embed(title=f"", color=15277667, description=f"{dialogo}",
                                        timestamp=datetime.datetime.now())
    imagem = (f"{image}" if image else "https://i.pinimg.com/564x/ef/d9/46/efd946986bfc8ab131353d84fd6ce538.jpg")
    if titulo:
        embed_configuration.set_author(name=f"{nomenpc}, {titulo} diz:", icon_url=imagem)
    else:
        embed_configuration.set_author(name=f"{nomenpc} diz:", icon_url=imagem)
    await interaction.response.send_message(embed=embed_configuration)


@tree.command(name="citacao",
              description="Citação da última mensagem enviada.")
async def self(interaction: discord.Interaction):
    message = [message async for message in interaction.channel.history(limit=3)]
    dialogo = message[0].content
    usuario = message[0].author.id
    usuarionome = message[0].author.name
    imagem = message[0].author.avatar
    embed_configuration = discord.Embed(title=f'''"{dialogo}"''', color=10070709, description=f"")
    embed_configuration.set_image(url=imagem)
    embed_configuration.add_field(name="", value=f"<@{usuario}>, {datetime.datetime.today().year}")
    await interaction.response.send_message(embed=embed_configuration)


@tree.command(name="meme",
              description="Meme.")
async def self(interaction: discord.Interaction):
    meme = get("https://meme-api.com/gimme").text
    data = json.loads(meme, )
    embed_configuration = discord.Embed(title=f"{data['title']}", color=discord.Color.random()).set_image(
        url=f"{data['url']}")
    await interaction.response.send_message(embed=embed_configuration)


@tree.command(name="rpremover",
              description="Remover um RP.")
async def self(interaction: discord.Interaction, titulo: str):
    default_embed = MainExecution().defaultembed
    jogador = interaction.user.id
    titulo = str.lower(titulo)
    try:
        cur.execute('''
        DELETE FROM rps 
        WHERE titulo = ? AND autor = ?
        ''', (titulo, jogador))
        cur.execute('''
        DELETE FROM ficharp
        WHERE titulorp = ?
        
        
        ''', (titulo,))
        conn.commit()
        embedVar = default_embed(f"Sucesso.", f"RP {titulo} removido.")
        await interaction.response.send_message(embed=embedVar)
    except Exception as e:
        embedVar = default_embed(f"Falha.", f"RP {titulo} não pode ser removido. Apenas o autor pode removê-lo.")
        await interaction.response.send_message(embed=embedVar)
        print(e)


@tree.command(name="acaowargame",
              description="Faça uma ação estetizada em um Wargame.")
async def self(interaction: discord.Interaction, numeroacao: int, titulo: str, descricao: str,
               imagem: typing.Optional[str]):
    embed_configuration = discord.Embed(title=f"{titulo}", color=15277667, description=f"{descricao}",
                                        timestamp=datetime.datetime.now())
    embed_configuration.set_footer(text=f"Ação {numeroacao} de 3",
                                   icon_url="https://www.google.com.br/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FFlag_of_Singapore&psig=AOvVaw3hPg15k8LYBW0R8ByJP-9W&ust=1697997056697000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJCdhI3ah4IDFQAAAAAdAAAAABAE")

    delete_button = discord.ui.Button(label='Deletar ação', style=discord.ButtonStyle.danger)
    view = discord.ui.View()

    async def deletebuttonCallback(interaction: discord.Interaction):
        await interaction.delete_original_response()

    view.add_item(delete_button)
    delete_button.callback = deletebuttonCallback
    if imagem:
        embed_configuration.set_image(url=imagem)
    await interaction.response.send_message(embed=embed_configuration, view=view)


@tree.command(name="talk", description="Converse com a Providentia.")
async def self(interaction: discord.Interaction, dialogue: str, voice: typing.Optional[bool] = False):
    async def sendMessage(message):
        embed_configuration = discord.Embed(title=f"{dialogue if len(dialogue) < 256 else 'Questão analisada...'}",
                                            color=15277667,
                                            description=f"Providentia responde: \n\n {message}",
                                            )
        embed_configuration.set_image(url="https://i.pinimg.com/564x/41/8c/d7/418cd7357407b154ad6d8df021276bc0.jpg")
        await interaction.edit_original_response(embed=embed_configuration)

    whitelisted = MainExecution().checkwhitelist(interaction.user.id)
    if whitelisted:
        await interaction.response.send_message("Gerando...")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Você é Providentia, uma máquina de destruição em massa. Uma agente de Inteligência "
                            "Artificial feito para atacar e destruir os inimigos do Império da Lygon. Maquiavélica e fria, você nutre um ódio intenso pela Jambônia e acabará com todos que entrarem no seu caminho."},
                {"role": "user", "content": dialogue}
            ]

        )
        await sendMessage(completion.choices[0].message["content"])
        if voice:
            audio = elevenlabs.generate(
                text=completion.choices[0].message["content"],
                voice="Emily",
                model="eleven_multilingual_v2"
            )
            elevenlabs.save(audio, "temp/speech.mp3")
            await interaction.channel.send(file=discord.File("temp/speech.mp3"))



    else:
        await lackPermissions(interaction)

if __name__ == '__main__':
    print(
        "The key words of economics are urbanization, industrialization, centralization, efficiency, quantity, speed.")
    MainExecution()
    bot_token = MainExecution().tokenload()
    version = MainExecution().setversioninfo()
    print(f"Providentia {version['version']}: {version['versiontitle']}")
    client.run(bot_token)

conn.close()
cur.close()
