from peewee import Model, CharField, SqliteDatabase

db = SqliteDatabase("MilitaryData/memory.db")


class Whitelist(Model):
    userid = CharField(unique=True)

    class Meta:
        database = db


class RPS(Model):
    titulo = CharField()
    descricao = CharField()
    autor = CharField()
    imagem = CharField()

    class Meta:
        database = db


class FichaRP(Model):
    titulorp = CharField()
    jogador = CharField()
    nomepersonagem = CharField()
    personalidade = CharField()
    idade = CharField()
    habilidades = CharField()
    aparencia = CharField()
    historia = CharField()
    imagem = CharField()
    genero = CharField()

    class Meta:
        database = db


class Censura(Model):
    palavra = CharField()

    class Meta:
        database = db
