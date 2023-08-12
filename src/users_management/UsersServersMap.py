from src.users_management.Connection import Connection
from datetime import datetime
from typing import Tuple


class UsersServersMap(Connection):

	class Map(object):

		def __init__(self, id_: int, user_id: int, server_id: int, created_at: datetime, updated_at):
			self.id = id_
			self.user_id = user_id
			self.server_id = server_id
			self.created_at = created_at
			self.updated_at = updated_at

		def __dict__(self) -> dict:
			return {
				"id": self.id,
				"user_id": self.user_id,
				'server_id': self.server_id,
				'created_at': self.created_at,
				'updated_at': self.updated_at
			}

		@classmethod
		def __lambda__(cls, x):
			return cls(*x)

		def __str__(self) -> str:
			return str(self.__dict__())

	def __internal_return(func, *args):
		def parse(self, *args):
			return tuple(map(UsersServersMap.Map.__lambda__, func(self, *args)))
		return parse

	@__internal_return
	def get_users_servers_map(self) -> Tuple[Map]:
		with self.cursor as cur:
			cur.execute("SELECT * FROM carlinhos.user_server_map;")
			content = cur.fetchall()
		return content

	def add(self, mapping: Map):
		with self.cursor as cur:
			cur.execute(
				'INSERT INTO carlinhos.user_server_map (user_id, server_id) VALUES (%s, %s)',
				(mapping.user_id, mapping.server_id)
			)
			self.connection.commit()

	def delete(self, mapping: Map):
		with self.cursor as cur:
			cur.execute(
				'DELETE FROM carlinhos.user_server_map WHERE user_id = %s',
				(mapping.user_id,)
			)
			self.connection.commit()

	@__internal_return
	def get_using_user_id(self, mapping: Map) -> Tuple[Map]:
		with self.cursor as cur:
			cur.execute(
				"SELECT * FROM carlinhos.user_server_map WHERE user_id = %s;",
				(mapping.user_id, )
			)
			content = cur.fetchall()
			print(content)
		return content

	@__internal_return
	def get_using_server_id(self, mapping: Map) -> Tuple[Map]:
		with self.cursor as cur:
			cur.execute(
				"SELECT * FROM carlinhos.user_server_map WHERE user_id = %s;",
				(mapping.server_id, )
			)
			content = cur.fetchall()
		return content

	@__internal_return
	def get_using_id(self, mapping: Map) -> Tuple[Map]:
		with self.cursor as cur:
			cur.execute(
				"SELECT * FROM carlinhos.user_server_map WHERE id = %s;",
				(mapping.id, )
			)
			content = cur.fetchall()
		return content

	def update(self, mapping: Map):
		with self.cursor as cur:
			cur.execute(
				"""
UPDATE carlinhos.user_server_map
SET
user_id = %s,
server_id = %s,
created_at = %s,
updated_at = CURRENT_TIMESTAMP
WHERE id = %s;
				""",
				(
					mapping.user_id,
					mapping.server_id,
					mapping.created_at,
					mapping.id
				)
			)
			self.connection.commit()





