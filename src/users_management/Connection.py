from psycopg2 import connect
from json import loads, dumps


class Connection(object):

	def __init__(self, config_path="config/config.json"):
		with open(config_path, "r") as config:
			self.config = loads(config.read())
		self.connection = connect(
			host=self.config['DATABASE']['HOST'],
			user=self.config['DATABASE']['USER'],
			password=self.config['DATABASE']['PASSWORD'],
			dbname=self.config['DATABASE']['USER']
		)
		self.using_file = config_path

	# def __del__(self):
	# 	with open(self.using_file, 'w') as config:
	# 		config.write(dumps(self.config, indent="\t"))

	@property
	def cursor(self):
		return self.connection.cursor()

	def commit(self):
		self.connection.commit()