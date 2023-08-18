from src.DiscordBot.Carlinhos import Carlinhos
from src.DiscordBot.Commands import Cog
from json import loads
import asyncio
from discord import commands
import discord

with open('config/config.json', 'r') as config: rr = loads(config.read())

# bot.run(rr['BOT'])
carlinhos = Carlinhos()
carlinhos.add_cog(Cog(carlinhos))
carlinhos.run(rr['BOT'])