from discord.ext import commands
import discord
from datetime import datetime
from src.users_management.AccountWatchlist import AccountWatchlist
from src.Scrappers.Telegram import TelegramScrapper
from json import dumps

class Cog(discord.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name='hello')
	async def hello(self, ctx: discord.ApplicationContext):
		await ctx.respond(f"CAVALOOOOS DO {ctx.author.mention}")

	@commands.slash_command(name='send-captilazed-message')
	async def send_big_message(self, ctx: discord.ApplicationContext, message: str):
		await ctx.respond(str(message).upper())

	@commands.slash_command(name='watch-account-telegram-here')
	async def account_telegram_here(self, ctx: discord.ApplicationContext, account_name: str, account_url: str):
		"""
		Creates a new telegram account to be mapped
		:param ctx:
		:param account_name:
		:param account_url:
		:return:
		"""
		con = AccountWatchlist()
		opts = TelegramScrapper.OPTIONS_SCHEME
		opts['replying_to'].append(ctx.channel_id)
		account = AccountWatchlist.Account(
			id=None,
			account_name=account_name,
			account_url=account_url,
			options=dumps(TelegramScrapper.OPTIONS_SCHEME),
			created_at=datetime.now(),
			updated_at=None
		)
		con.add(account)
		await ctx.respond(f"Account added to you and replying this channel {ctx.author.mention}")

	@commands.slash_command(name='reply-to-server')
	async def reply_to_server(self, ctx: discord.ApplicationContext, message: str, server_channel: str):
		await ctx.send("Sua mensagem foi enviada com successo >w<")
		await self.bot.get_channel(int(server_channel)).send(content=f'"{message}" - {ctx.author.name} de bem longe')
