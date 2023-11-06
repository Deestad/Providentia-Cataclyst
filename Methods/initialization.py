# Standard Library Imports
import ast
import datetime
import re
import inspect
import logging
import atexit
import json
import random
import time
import sqlite3
import os
import io
import winsound
# Third-Party Library Imports
import peewee
from peewee import Model, CharField, SqliteDatabase
import openai
import elevenlabs
import discord
import PySimpleGUI as sg
# PROJECT IMPORTS
# Project-Specific Imports
from Methods.system_methods import console_log
from Methods.database_models import *




sg.theme('DarkPurple2')

# CONSTANTS
CLIENT_FILE = 'google.json'
TOKEN_FILE = "token.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

USER_INFO_FILE = "MilitaryData/userinfo.json"
VERSION_INFO_FILE = "versioninfo.json"


def termination():
    console_log(f"Initiation of termination procedures. \n")
    db.close()
    console_log("Termination succeeded.")


class Initialization:
    def __init__(self):
        self.model = None
        self.bot_token = None
        self.ai_token = None
        self.voice_token = None
        # Initialization procedures
        self.intents = None
        self.version_title = None
        self.version = None
        self.version_info = None
        self.activity = None

        winsound.PlaySound("Dialogues/keywordsofeconomics.wav", winsound.SND_FILENAME)
        winsound.PlaySound("Dialogues/initializing.wav", winsound.SND_FILENAME)

        try:
            db.connect()
        except peewee.OperationalError as e:
            # If the connection is already open, ignore the exception
            if 'Connection already opened' not in str(e):
                logging.error(e)

        db.create_tables([Whitelist, RPS, FichaRP, Censura], safe=True)

    def load_configuration(self):
        with open(VERSION_INFO_FILE, encoding='utf-8') as version_info_file:
            self.version_info = json.load(version_info_file)
        winsound.PlaySound("Dialogues/choosemodel.wav", winsound.SND_FILENAME)

        get_model = [ [sg.Button('Modelo I: Lygon'),
                       [sg.Button('Modelo II: Espionagem')]]

        ]
        window = sg.Window('Choose the used model', get_model)
        while True:
            event,values = window.read()

            if event == "Modelo I: Lygon":
                self.model = 1
                break
            elif event == "Modelo II: Espionagem":
                self.model = 2
                break
            if event == sg.WIN_CLOSED:
                break
        window.close()


        if os.path.isfile("token.json") and os.access("token.json", os.R_OK):
            console_log("Token detected.")
            with open(TOKEN_FILE, "r") as file:
                token_data = json.load(file)
                if self.model == 1:
                    self.bot_token = token_data.get("token")
                elif self.model == 2:
                    self.bot_token = token_data.get("backup")
                self.ai_token = token_data.get("openaitoken")
                openai.api_key = self.ai_token
                self.voice_token = token_data.get("openaitoken")
                self.voice_token = token_data.get("elevenlabsapikey")
                elevenlabs.set_api_key(self.ai_token)
        else:
            token = input("Info rm the token to activate Providentia. \n")
            openai.api_key = input("Inform the OpenAI token. This one is necessary for talking operations.\n")
            elevenlabs_token = input("Insert token for voice application. ElevenLabs. \n")
            try:
                elevenlabs.set_api_key(elevenlabs_token)
            except Exception as e:
                console_log("Erro obtendo API do Eleven Labs:",e)
                logging.error(e)
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

    def check_whitelist(self, userid):
        userid = str(userid)
        current_frame = inspect.currentframe()
        top_function = inspect.getframeinfo(current_frame.f_back).function
        try:
            whitelisted = Whitelist.get(Whitelist.userid == userid)
            if whitelisted:
                if "on_message" not in top_function:
                    console_log(f"Whitelisted user command. ID: {userid}")
                return True
        except ValueError:
            return False
        except Exception as err:
            error = str(err)
            if "instance matching query does not exist" in error:
                pass
            else:
                console_log("Erro na verificação da Whitelist:", err)
                logging.error(err)

    def call_intents(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        intents = self.intents
        return intents

    def defaultembed(self, title, message):

        self.embed = discord.Embed(title=f"{title}", description=f"{message}", color=0x2ecc71)
        self.embed.set_author(name="PLYG-7X42",
                              icon_url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9f1ed69b-9e98-4f78-acda-c95c6f4be159/db73tp3-8c5589a6-051c-4408-b244-f451c599b04d.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlmMWVkNjliLTllOTgtNGY3OC1hY2RhLWM5NWM2ZjRiZTE1OVwvZGI3M3RwMy04YzU1ODlhNi0wNTFjLTQ0MDgtYjI0NC1mNDUxYzU5OWIwNGQuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.7X4JjtqAwnetH9HC9f4sl3kcik8VCFCE5nr1MGB607M")
        return self.embed
