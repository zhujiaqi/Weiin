# -*- coding: utf-8 -*-
from public import *

def store_token(uid,at,expire):
	db.access_tokens.save({'_id': uid, 'at': at, 'exp': expire, 'c': datetime.datetime.now()})

def get_token(uid):
	item = db.access_tokens.find_one(uid)
	if item:
		return item['at'],item['exp']