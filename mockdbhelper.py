MOCK_LINKS = [{"_id": "1", "number":"1", "owner":"test@example.com", "url": "mockurl"}]

MOCK_USERS = [{"email": "test@example.com", 
               "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=", 
               "hashed":  "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e"}]

class MockDBHelper:

	def add_link(self, link, owner):
		number = len(MOCK_LINKS) + 1
		MOCK_LINKS.append({"_id": str(number), "number": number, "url": link, "owner": owner})

	def get_links(self, owner_id):
		return MOCK_LINKS

	def delete_link(self, link_id):
		for i, link in enumerate(MOCK_LINKS):
			if link.get("_id") == link_id:
				del MOCK_LINKS[i]
				break

	def get_user(self, email):
		user = [x for x in MOCK_USERS if x.get("email") == email]
		if user:
			return user[0]
		return None

	def add_user(self, email, salt, hashed):
		MOCK_USERS.append({"email": email, "salt":salt, "hashed": hashed})
