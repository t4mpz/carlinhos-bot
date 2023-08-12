from src.users_management.Connection import Connection
from datetime import datetime
from typing import Tuple
from json import loads, dumps


class AccountWatchlist(Connection):

	class Account(object):

		def __init__(self, id: int, account_name: str, account_url: str, created_at: datetime, updated_at: datetime, options: str):
			self.id = id,
			self.account_name = account_name
			self.account_url = account_url
			self.created_at = created_at
			self.updated_at = updated_at
			self.options = options

		def __dict__(self) -> dict:
			return {
				"id": self.id,
				"account_name": self.account_name,
				"account_url": self.account_url,
				"created_at": self.created_at,
				"updated_at": self.updated_at,
				"options": self.options
			}

		@property
		def json_options(self) -> dict:
			return loads(self.options)

		@json_options.setter
		def json_options(self, options: dict):
			self.options = dumps(options)

		@classmethod
		def __lambda__(cls, x):
			return cls(*x)

		def __str__(self) -> str:
			return str(self.__dict__())

	def __internal_return(func, *args):
		def parse(self, *args):
			return tuple(map(AccountWatchlist.Account.__lambda__, func(self, *args)))
		return parse

	@__internal_return
	def get_watchlist(self) -> Tuple[Account]:
		with self.cursor as cur:
			cur.execute("SELECT * FROM carlinhos.account_watchlist;")
			content = cur.fetchall()
		return content

	def add(self, account: Account):
		with self.cursor as cur:
			cur.execute(
				"INSERT INTO carlinhos.account_watchlist (account_name, account_url, options) VALUES (%s, %s, %s);",
				(account.account_name, account.account_url, account.options)
			)
			self.commit()

	def delete(self, account: Account):
		with self.cursor as cur:
			cur.execute(
				"DELETE FROM carlinhos.account_watchlist where id = %s;",
				(account.id,)
			)
			self.commit()
	@__internal_return
	def get_by_id(self, account: Account) -> Tuple[Account]:
		with self.cursor as cur:
			cur.execute("SELECT * FROM carlinhos.account_watchlist WHERE id = %s;", (account.id, ))
			content = cur.fetchall()
		return content

	@__internal_return
	def get_by_name(self, account: Account) -> Tuple[Account]:
		with self.cursor as cur:
			cur.execute("SELECT * FROM carlinhos.account_watchlist WHERE account_name = %s;", (account.account_name, ))
			content = cur.fetchall()
		return content

	def update(self, account: Account):
		with self.cursor as cur:
			cur.execute(
				"""
UPDATE carlinhos.account_watchlist
SET
account_name = %s,
account_url = %s,
created_at = %s,
options = %s,
updated_at = CURRENT_TIMESTAMP
WHERE id = %s;
				""",
				(
					account.account_name,
					account.account_name,
					account.created_at,
					account.options,
					account.id
				)
			)
			self.connection.commit()