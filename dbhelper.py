import pymongo
from bson.objectid import ObjectId

DATABASE = 'linkshare'

class DBHelper:

	def __init__(self):
		client = pymongo.MongoClient()
		self.db = client[DATABASE]

	def get_user(self, email):
		return self.db.users.find_one({"email": email})

	def add_user(self, email, salt, hashed):
		self.db.users.insert({"email": email, "salt": salt, "hashed": hashed})

	def add_link(self, link, owner):
		self.db.links.insert({"url": link, "owner": owner})

	def get_links(self, owner_id):
		return list[self.db.links.find({"owner": owner_id})]

	def delete_link(self, link_id):
		self.db.links.remove({"_id": ObjectId(link_id)})