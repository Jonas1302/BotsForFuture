import json
import logging
import os
from os.path import expanduser


logger = logging.getLogger(__name__)
save_dir = os.path.join(expanduser("~"), ".botsforfuture")
storage_dir = os.path.join(save_dir, "data")


def get_storage(name):
	return Storage(os.path.join(storage_dir, name) + ".json")


class Storage:
	def __init__(self, path):
		self.__path = path
		self.__data = {}
		self.load()
	
	
	def __getattr__(self, name):
		return self.__data.get(name)
	
	def __setattr__(self, name, value):
		# do not store private variables
		# 1. it's useless to store them in the json file
		# 2. it would create an infinite loop with __getattr__
		if name.startswith("_"):
			super().__setattr__(name, value)
		else:
			self.__data[name] = value
	
	
	def load(self):
		"""
		Load all data from the disk, overwriting all data that wasn't saved.
		Clear data if there's no storage file.
		"""
		if not os.path.exists(self.__path):
			self.__data = {}
			return
		
		with open(self.__path, "r") as f:
			self.__data = json.load(f)
	
	def save(self):
		"""Save all data on the disk"""
		with open(self.__path, "w") as f:
			json.dump(self.__data, f)

def load(path):
	"""Load a json file and return it as dict"""
	with open(os.path.join(save_dir, path), "r") as f:
		return json.load(f)

def save(path, data):
	"""Save all data on the disk as json file"""
	with open(os.path.join(save_dir, path), "w") as f:
		json.dump(data, f)
