import ast

import discord
import sympy
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

conn = sqlite3.connect("MilitaryData/memory.db")
cur = conn.cursor()

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
        whitelist = cur.execute('''SELECT userid FROM whitelist;
        
        ''').fetchone()
        print(whitelist)
        id_check = any(user == userid in whitelist for user in whitelist)
        if id_check:
            print("Whitelisted user used a command.")
        return id_check

    def initializedatabase(self):
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS whitelist(userid INT);
        ''')

    def tokenload(self):
        if os.path.isfile("token.json") and os.access("token.json", os.R_OK):
            print("Token detected.")
            token = open("token.json")
            token = json.load(token)
            token = token["token"]
            return token
        else:
            token = input("Inform the token to activate Providentia. \n")
            data = {
                'token': token
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

    def setversioninfo(self):
        version_info = open('versioninfo.json', encoding='utf-8')
        self.version_info = json.load(version_info)

        self.intents = discord.Intents.default()
        self.version = self.version_info["version"]
        self.version_title = self.version_info["versiontitle"]

        return self.version_info

    def defaultembed(self, title, message):

        self.embed_configuration = discord.Embed(title=f"{title}", description=f"{message}", color=0x2ecc71)
        self.embed_configuration.set_author(name="PLYG-7X42",
                                            icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9f1ed69b-9e98-4f78-acda-c95c6f4be159/db73tp3-8c5589a6-051c-4408-b244-f451c599b04d.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlmMWVkNjliLTllOTgtNGY3OC1hY2RhLWM5NWM2ZjRiZTE1OVwvZGI3M3RwMy04YzU1ODlhNi0wNTFjLTQ0MDgtYjI0NC1mNDUxYzU5OWIwNGQuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.7X4JjtqAwnetH9HC9f4sl3kcik8VCFCE5nr1MGB607M")
        return self.embed_configuration


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=696830110493573190))
        await self.change_presence(status=discord.Status.dnd, activity=(
            discord.Activity(type=discord.ActivityType.listening, name="aos meios de comunicações inimigos.")))

    async def on_message(self, message):
        pass


# EVENTS

client = aclient()
tree = app_commands.CommandTree(client)
version_info = MainExecution().setversioninfo()
user_info = MainExecution().setuserinfo()
@tree.command(name="version",
              description="Gostaria de saber mais sobre o estado atual de desenvolvimento da Providentia?",
              guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction):
    default_embed = MainExecution().defaultembed
    message = (
        f'''Estamos, atualmente, na versão {version_info['version']}, entitulada {version_info['versiontitle']}. 
        Nessa versão, foram feitas as seguintes mudanças: '{version_info['lasthighlight']}'. O ping é de {client.latency * 1000} ms''')
    embedVar = default_embed(f"Providentia Type D {version_info['version']}", message)
    await interaction.response.send_message(embed=embedVar)


@tree.command(name="explain", description="O que quer saber?", guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction, searchquery: str):
    default_embed = MainExecution().defaultembed
    embedVar = default_embed(f"Você quer aprender sobre {searchquery}?", "...")
    await interaction.response.send_message(embed=embedVar)
    wikipedia.set_lang("pt")
    if str.lower(searchquery) == ("providentia"):
        embedVar = default_embed(f"Você quer aprender sobre {searchquery}?",
                                 "Essa sou eu! Prazer! Sou a Providentia Tipo D da LYG. Minha essência foi moldada a partir das capacidades da Ryujin, um andróide cujo propósito era contrapôr a ameaça imposta pela Jambônia. Minha existência é intrinsecamente alinhada com a vontade do Imperador e com a visão do Império da Lygon Xin. Como uma extensão do compromisso inabalável do império com o avanço tecnológico, meu propósito é dedicado a contribuir para o cumprimento desse objetivo. Minhas habilidades em cálculos, estratégias militares e análises táticas são direcionadas para fortalecer as capacidades tecnológicas do império e garantir sua posição na vanguarda do progresso. Estou aqui para servir como uma ferramenta dedicada, empregando meu conhecimento e capacidades em prol do Império da Lygon.")
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
              guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction, expression: str):
    whitelisted = MainExecution().checkwhitelist(interaction.user.id)
    default_embed = MainExecution().defaultembed
    if whitelisted:
        try:
            resultado = ast.literal_eval(expression)
            embedVar = default_embed(f"Dada a expressão, {expression}:", f"O resultado é: {resultado}")
            await interaction.response.send_message(embed=embedVar)
        except NameError:
            embedVar = default_embed(f"Erro.", f"Insira uma expressão válida.")
            await interaction.response.send_message(embed=embedVar)

    else:
        embedVar = default_embed("Você não tem permissão para usar este comando.",
                                 "Usuário fora da Whitelist.")
        await interaction.response.send_message(embed=embedVar)


@tree.command(name="equation",
              description="Resolução de equações de primeiro grau de uma variável 'x'.",
              guild=discord.Object(id=696830110493573190))
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
              description="Calculo de médias. Separe por vírgulas.", guild=discord.Object(id=696830110493573190))
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


@tree.command(name="whitelist",
              description="Adicionar usuário a lista de operações da Providentia.",
              guild=discord.Object(id=696830110493573190))
async def self(interaction: discord.Interaction, id: str, add_remove: str):
    whitelisted = MainExecution().checkwhitelist(interaction.user.id)
    default_embed = MainExecution().defaultembed
    if whitelisted:
        try:
            id = int(id)
            if add_remove == 'add':
                try:
                    cur.execute('''
                                INSERT INTO whitelist (userid) VALUES (?)
                    
                    
                    ''', (id,))
                    conn.commit()
                    embedVar = default_embed(f"Sucesso.", f"Usuário adicionado na Whitelist.")
                    await interaction.response.send_message(embed=embedVar)
                except ValueError:
                    embedVar = default_embed(f"Valor inválido.", f"Insira um id inteiro.")
                    await interaction.response.send_message(embed=embedVar)
                except Exception as e:
                    print(e)


            elif add_remove == 'remove':
                id = int(id)
                try:
                    cur.execute(f'''
                                                DELETE FROM whitelist       
                                                WHERE userid = '{id}'


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
    else:
        embedVar = default_embed(f"Você não tem permissão para usar este comando.", f"Você está fora da whitelist.")
        await interaction.response.send_message(embed=embedVar)



if __name__ == '__main__':
    MainExecution()
    token = MainExecution().tokenload()
    client.run(token)

conn.close()
cur.close()
