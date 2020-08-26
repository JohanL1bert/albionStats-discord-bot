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
            return TOKEN, ID_CHANNEL
        else:
            print("custom error = File .env is empty")
    else:
        print("custom error = Env file not found")


# ID CHANNEL AND TOKEN DISCORD
TOKEN, ID_CHANNEL = env_check()


# checkers server room
def check_id_channel(id_channel):
    pass
    


# Send ready when bot is connect to server
#FIXME: Переписать проверку
@client_bot.event
async def on_ready():
    await client_bot.get_channel(ID_CHANNEL).send("Bot is ready")


# Help settings
#FIXME: Возможно лучше переписать кастомный хелп
@client_bot.command()
async def help(ctx):

    embed = discord.Embed(
        colour = discord.Color.blue(),
        description = "Description of the commands"
    )

    embed.add_field(name = "add user", value = "This will add user", inline = False)
    embed.add_field(name = "status bot", value = "Check bot status", inline = False)
    embed.add_field(name = "status API", value = "Check is albion site is not down", inline = False)


    await client_bot.get_channel(ID_CHANNEL).send(embed = embed)


client_bot.run(TOKEN)



#TODO: написать чекер канала
# API ALBION
# embed доделать

