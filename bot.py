import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv

#Customize settings
bot_prefix = '!'
client_bot = commands.Bot(command_prefix = bot_prefix)
client_bot.remove_command('help')
db_name = "guild_data.db"


#check exist db
#TODO: Bad code. Later maybe full rewrite. 
def db_exists():
    if os.path.isfile(db_name):
        connect_db(db_name)
    else:
        file_name = open(db_name, "w+")
        file_name.close()
        conn = connect_db(db_name)
        create_default_fields(conn)
        


# Create default field for bd
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
    
   

def connect_db(db_name):
    connection = sqlite3.connect(db_name)
    return connection 

  


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
    embed.add_field(name = "status bot", value = "Check bot status", inline = False)
    embed.add_field(name = "status API", value = "Check is albion site is not down", inline = False)

    await client_bot.get_channel(ID_CHANNEL).send(embed = embed) # ctx.send(embed = embed)


#Commands
#TODO: Больше команд. Исправить название. Написать функции
@client_bot.command()
async def add_player(ctx, name):
    await ctx.send("Player name - {} is add".format(name))


@client_bot.command()
async def add_guild():
    pass

@client_bot.command()
async def status():
    pass

@client_bot.command()
async def albion_status():
    pass


#Save 
#TODO: Возможно лучше сделать один файл для всех сейвов
""" def save_player_name():
    pass

 """

#requestest 

client_bot.run(TOKEN)


#API ALBION
KB_ALBION_URL = "https://albiononline.com/en/killboard/battles/"



#TODO: написать чекер канала
# API ALBION
# embed доделать
# можно сделать bot_prefix customize






