import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

#Customize settings
bot_prefix = '!'
client_bot = commands.Bot(command_prefix = bot_prefix)
client_bot.remove_command('help')


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


# ID CHANNEL AND TOKEN DISCORD
TOKEN, ID_CHANNEL, CHANNEL_NAME = env_check()


#checkers server room
#TODO: Возможно переписать под множества каналов. Удалить else
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
    await client_bot.get_channel(ID_CHANNEL).send("Bot is connected to channel")



# Help settings
#FIXME: Возможно лучше переписать кастомный хелп
@client_bot.command()
async def help(ctx):

    embed = discord.Embed(
        colour = discord.Color.blue(),
        description = "Description of the commands"
    )

    embed.add_field(name = "add_player", value = "This will add user", inline = False)
    embed.add_field(name = "add_guild name", value = "Add guild to track", inline = False)
    embed.add_field(name = "status_bot", value = "Check bot status", inline = False)
    embed.add_field(name = "status_API", value = "Check is albion site is not down", inline = False)


    await client_bot.get_channel(ID_CHANNEL).send(embed = embed)


#Commands
#TODO: Больше команд. Исправить название. Написать функции
@client_bot.command()
async def add_player():
    pass

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


client_bot.run(TOKEN)


#API ALBION
KB_ALBION_URL = "https://albiononline.com/en/killboard/battles/"



#TODO: написать чекер канала
# API ALBION
# embed доделать
# можно сделать bot_prefix customize


