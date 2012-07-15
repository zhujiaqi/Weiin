# -*- coding: utf-8 -*-
from public import *

def engage_session(uid):
	sid = str(db.sessions.insert({'u': uid}, safe=True))
	return sid

def get_session(sid):
	s = db.sessions.find_one(ObjectId(sid))
	if s:
		return s['u']

def destroy_session(sid):
	db.sessions.remove({'_id': ObjectId(sid)})