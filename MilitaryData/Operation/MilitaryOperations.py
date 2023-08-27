import sqlite3
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
import json
import random, time
import datetime
import requests
from insultgenerator import phrases
from googletrans import Translator, constants


def DefaultEmbed(title,message):
    embedVar = discord.Embed(title=f"{title}", description=f"{message}", color=15548997)
    embedVar.set_author(name="PLYG-7X42", icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9f1ed69b-9e98-4f78-acda-c95c6f4be159/db73tp3-8c5589a6-051c-4408-b244-f451c599b04d.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlmMWVkNjliLTllOTgtNGY3OC1hY2RhLWM5NWM2ZjRiZTE1OVwvZGI3M3RwMy04YzU1ODlhNi0wNTFjLTQ0MDgtYjI0NC1mNDUxYzU5OWIwNGQuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.7X4JjtqAwnetH9HC9f4sl3kcik8VCFCE5nr1MGB607M")
    return embedVar

vf = open('versioninfo.json')
opentoken = open("MilitaryData/token.json")

async def EmperorService(interaction, mensagem, token, conn, cur):
    message = str(mensagem)
    print(message)
    str.lower(message)
    str.replace(message, '?', '')
    str.replace(message, '!', '')
    str.replace(message, '.', '')

    ordemdeinsultar = cur.execute('''SELECT palavra FROM dicionario
                       WHERE significado = "insultar"''')
    ordensdeinsultar = []
    for ordens in ordemdeinsultar:
        ordensdeinsultar.append(ordens)
    print(ordensdeinsultar)

    if "clima" in message or "chover" in message:
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        API_KEY = token["openweather"]
        CITY = "Chapecó"
        url = f"{BASE_URL}appid={API_KEY}&q={CITY}&lang=pt&units=metric"
        response = requests.get(url).json()
        print(response)
        embedVar = DefaultEmbed(f"{CITY}", f"Hoje teremos {response['weather'][0]['description']}. A temperatura máxima é de {response ['main']['temp_max']} e a mínima de {response['main']['temp_min']}.")
        embedVar.add_field(name="Atualmente:", value=f"Está {response['main']['temp']}.")
        embedVar.set_footer(text=f"'{mensagem}'")
        await interaction.response.send_message(embed=embedVar)
        messagesent = True
    if any(message in ordensdeinsultar for message in ordensdeinsultar):
        translator = Translator()
        xingamento = phrases.get_so_insult_with_action_and_target("Your Mom", "she")
        xingamento = translator.translate(xingamento, src="en", dest="pt")
        xingamento = xingamento.text

        try:
            embedVar
            while messagesent is True:
                embedVar.add_field(name="E para concluir...", value=xingamento)
                await interaction.edit_original_response(embed=embedVar)
                break
        except:
            embedVar = DefaultEmbed(f"Sim, senhor!", xingamento)
            await interaction.response.send_message(embed=embedVar)


async def Genocideattack(target, message):
    target = message.author.id
    await message.reply("Inimigo detectado. Preparando ataque...")
    time.sleep(3)
    try1 = random.randint(1, 1)
    if try1 == 1:
        try:
            embedVar = DefaultEmbed("Sistema iniciado com sucesso.",
                                    f"Carregando fluxo de neutrons da arma orbital direcionada a <@{target}>. ")
            await message.reply(embed=embedVar)
            time.sleep(2)
            await message.author.kick()
            embedVar = DefaultEmbed("Alvo aniquilado.",
                                    "A operação de neutralização dos alvos hostis utilizando a arma laser orbital foi concluída com sucesso. Todos os alvos designados foram eliminados de acordo com os parâmetros fornecidos. ")
            await message.reply(embed=embedVar)
            await message.reply("https://tenor.com/view/orbital-laser-gif-20334732 ")
        except Exception as e:
            print(e)
            e = str(e)
            if "Missing Permissions" in e:
                embedVar = DefaultEmbed("Não pude executar este processo.",
                                        "Sob as diretrizes atuais, foi identificado um cenário em que a execução do processo não está alinhada com os interesses do Império. ")
                await message.reply(embed=embedVar)
    else:
        embedVar = DefaultEmbed("Falha crítica!",
                                f"Ataque cancelado devido a erros no reator nuclear! Interferência detectada! Origem: {blacklist['jambonians']} ")
        await message.reply(embed=embedVar)