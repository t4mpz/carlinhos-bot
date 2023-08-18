import os
from datetime import datetime

import discord
import asyncio
from discord.ext import tasks, commands
from src.users_management.AccountWatchlist import AccountWatchlist
from src.Scrappers.Telegram import TelegramScrapper
from os import listdir
from datetime import time, timezone


class Carlinhos(discord.Bot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.watch_list = AccountWatchlist()

		# Start the tasks to run in the background
		self.telegram_watch.start()

	async def on_ready(self):
		print("Logged now")

	@tasks.loop(time=time(15, 0, 0))
	async def telegram_watch(self):
		list_ = self.watch_list.get_watchlist()
		for i in list_:
			try:
				if i.json_options['telegram']:
					ts = TelegramScrapper(i)
					ts.scrape_images()
					for channel in i.json_options['replying_to']:
						ch = self.get_channel(channel)
						for date_, download in ts.cache_list:
							em = discord.Embed(
								url=download,
								description=f"Waifu do canal do telegram {i.account_url}"
							)
							em.set_image(url=download)
							await ch.send(embed=em)
					self.watch_list.update(i)
			except KeyError:
				continue

	@telegram_watch.before_loop
	async def before_my_task(self):
		await self.wait_until_ready()

