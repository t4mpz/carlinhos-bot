from src.users_management.Connection import Connection
from typing import Tuple
from datetime import datetime


class MapsLogs(Connection):

	class Log:

		SUCCESS_CODE = 200
		ERROR_CODE   = 500

		def __init__(self, id: int, map_id: int, message: str, sending_data: datetime, status_code: int):
			self.id = id,
			self.map_id = map_id
			self.message = message
			self.sending_data = sending_data
			self.status_code = status_code

		def __dict__(self) -> dict:
			return {
				"id": self.id,
				"map_id": self.map_id,
				'message': self.message,
				'sending_data': self.sending_data,
				'status_code': self.status_code
			}

		@classmethod
		def __lambda__(cls, x):
			return cls(*x)

		def __str__(self) -> str:
			return str(self.__dict__())

	def __internal_return(func, *args):
		def parse(self, *args):
			return tuple(map(MapsLogs.Log.__lambda__, func(self, *args)))
		return parse

	@__internal_return
	def get_logs(self) -> Tuple[Log]:
		with self.cursor as cur:
			cur.execute("SELECT * FROM carlinhos.user_server_log;")
			content = cur.fetchall()
		return content

	@__internal_return
	def get_using_map(self, log: Log) -> Tuple[Log]:
		with self.cursor as cur:
			cur.execute(
				"SELECT * FROM carlinhos.user_server_log WHERE map_id = %s;",
				(log.map_id, )
			)
			content = cur.fetchall()
		return content

	@__internal_return
	def get_using_id(self, log: Log) -> Tuple[Log]:
		with self.cursor as cur:
			cur.execute(
				"SELECT * FROM carlinhos.user_server_log WHERE id = %s;",
				(log.id, )
			)
			content = cur.fetchall()
		return content

	def add(self, log: Log):
		with self.cursor as cur:
			cur.execute(
				"INSERT INTO carlinhos.user_server_log (map_id, message, status_code) VALUES (%s,%s,%s);",
				(log.map_id, log.message, log.status_code)
			)
			self.commit()