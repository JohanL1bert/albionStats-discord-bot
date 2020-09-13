import os
import asyncio
import requests
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv

#Customize settings
bot_prefix = '!'
client_bot = commands.Bot(command_prefix = bot_prefix)
client_bot.remove_command('help')
db_name = "guild_data.db"


#LIST to save track player and guild
player_track_list = list(None)
guild_track_list = list(None)

def create_file_list():
    pass


#API ALBION
ALBION_URL = "https://albiononline.com/en/killboard/battles/"


#check exist db if not create
#TODO: Bad code. Later maybe full rewrite. 
def db_exists():
    if os.path.isfile(db_name):
        connect_db(db_name)
    else:
        file_name = open(db_name, "w+")
        file_name.close()
        conn = connect_db(db_name)
        create_default_fields(conn)



#TODO: Delete field id or create one table
# Create default field for database
def create_default_fields(conn):
    cur = conn.cursor()

    # Создание таблиц Player и Guilds
    cur.execute("""CREATE TABLE Players(
        userid INT PRIMARY KEY,
        name TEXT);
    """)

    cur.execute("""CREATE TABLE Guilds(
        guildid INT PRIMARY KEY,
        name TEXT);
    """)

    conn.commit()
    cur.close()
    
   
# Connect to db
def connect_db(db_name):
    connection = sqlite3.connect(db_name)
    return connection



# Add data to db. Not working
def add_values_toBD(player_name, guild_name):
    conn = connect_db(db_name)
    cur = conn.cursor()
    if player_name:
        cur.execute("INSERT INTO Players(name) values (?)", (player_name))
    elif guild_name:
        cur.execute("INSERT INTO Guilds(name) values(?)", (guild_name))
    cur.close()

   

def ch_exists_value(iter_variable, function_name):
    conn = connect_db(db_name)
    cur = conn.cursor()
    if function_name == "add_player":
        cur.execute("SELECT name FROM Players WHERE name = ?", (iter_variable,))
        if cur.fetchone():
            return None
        else:
            return iter_variable
    elif function_name == "add_guild":
        cur.execute("SELECT name FROM Guilds WHERE name = ?", (iter_variable,))
        if cur.fetchone():
            return None
        else:
            return iter_variable
    cur.close()



# Check is env file is exists and not empty
#TODO: Переписать функцию проверки файла на пустоту. =/
def env_check():
    if os.path.isfile(".env"):
        load_dotenv()
        if os.path.getsize(".env") != 0:
            TOKEN = os.getenv("DISCORD_TOKEN")
            ID_CHANNEL = int(os.getenv("DISCORD_CHANNEL_ID"))
            CHANNEL_NAME = os.getenv("CHANNEL_NAME")
            return TOKEN, ID_CHANNEL, CHANNEL_NAME
        else:
            print("custom error = File .env is empty")
    else:
        print("custom error = Env file not found")



# FUNC to Check DB exists 
db_exists()

# ID CHANNEL AND TOKEN DISCORD
TOKEN, ID_CHANNEL, CHANNEL_NAME = env_check()


#checkers server room
#FIXME: Возможно переписать под множества каналов. Удалить else. Дергать только существующие каналы 
@client_bot.event
async def on_message(ctx):
    if ctx.channel.id == ID_CHANNEL:
        await client_bot.process_commands(ctx)
    else: # test Be deleted
        await client_bot.get_channel(ID_CHANNEL).send("Wrong channel")



# Send ready when bot is connect to server
#FIXME: Переписать проверку. Возможно лучше по каналам сделать
@client_bot.event
async def on_connect():
    start_message = ("```Bot is connected to channel```")
    await asyncio.sleep(0.2)
    await client_bot.get_channel(ID_CHANNEL).send(start_message)



# Help settings
#FIXME: Возможно лучше переписать кастомный хелп
@client_bot.command()
async def help(ctx):

    embed = discord.Embed(
        colour = discord.Color.blue(),
        description = "Description of the commands"
    )

    embed.add_field(name = "add player", value = "This will add user", inline = False)
    embed.add_field(name = "add guild name", value = "Add guild to track", inline = False)
    embed.add_field(name = "remove watch player", value = "Remove track from player", inline= False)
    embed.add_field(name = "remove watch guild", value = "Remove track from guild", inline= False)
    embed.add_field(name = "Check player is add", value = "Check is player already in database", inline = False)
    embed.add_field(name = "Check guild is add", value = "Check is guild already in database", inline = False)
    embed.add_field(name = "site status", value = "Check bot status", inline = False)
    embed.add_field(name = "status API", value = "Check is albion site is not down", inline = False)


    await ctx.send(embed = embed) # ctx.send(embed = embed) #client_bot.get_channel(ID_CHANNEL)


#Commands
#TODO: Больше команд. Исправить название. Написать функции
@client_bot.command()
async def add_player(ctx, player_name):
    func_name = ("add_player")
    player_status = ch_exists_value(player_name, func_name)
    if player_status == None:
        await ctx.send("Player name - {} is already in database".format(player_name))
    else:
        await ctx.send("Player name - {} is add to database and start tracking".format(player_status))




@client_bot.command()
async def add_guild(ctx, name_guild):
    func_name = ("add_guild")
    guild_status = ch_exists_value(name_guild, func_name)
    if guild_status == None:
        await ctx.send("Guild - {} is already in database".format(name_guild))
    else:
        await ctx.send("Guild name - {} is add to database and start tracking".format(guild_status))



@client_bot.command()
async def track_player():
    pass



@client_bot.command()
async def track_guild():
    pass



#TODO: try to rewrite for one func
@client_bot.command()
async def site_status(ctx):
    checkup = requests.get(ALBION_URL)
    if checkup.ok:
        await ctx.send("https://albiononline.com/en/home is okay")
    else:
        await ctx.send("Something wrong with albion site")



@client_bot.command()
async def ch_player(ctx, PL_name):
    conn = connect_db(db_name)
    cur = conn.cursor()
    cur.execute("SELECT name FROM Players WHERE name = ?", (PL_name,))
    if cur.fetchone():
        await ctx.send("Player name {} is exists in database".format(PL_name))
    else:
        await ctx.send("Not found in database")
    cur.close()

    
    

@client_bot.command()
async def ch_guild(ctx, G_name):
    conn = connect_db(db_name)
    cur = conn.cursor()
    cur.execute("SELECT name FROM Players WHERE name = ?", (G_name,))
    if cur.fetchone():
        await ctx.send("Guilds {} is exists in database".format(G_name))
    else:
        await ctx.send("Not found in database")
    cur.close()



#Save 
#TODO: Возможно лучше сделать один файл для всех сейвов
""" def save_player_name():
    pass
 """

#requestest 
#settings async
#VERY BAD
""" player_name = add_player()
print(player_name) """

client_bot.run(TOKEN)




#TODO: написать чекер канала
# API ALBION
# embed доделать
# можно сделать bot_prefix customize

#Добавляешь value
# Оно проверяет сущесвует ли в БД
# Если существует, то вовращает результат, что существует
# Если нет, то добавляет




