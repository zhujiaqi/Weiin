#!/usr/bin/env python
# -*- coding: utf-8 -*-

from public import *
import bottle
bottle.debug(True)
from bottle import *
from lib.weibo import APIClient

client = APIClient(app_key=consts.APP_KEY, app_secret=consts.APP_SECRET, redirect_uri=consts.CALLBACK_URL)

@route('/')
def index():
    temp = '<b>Weiin</b><br/>'
    temp += '<a href="%s">用微博账号登入</a>' % client.get_authorize_url()
    return temp

@route('/callback')
def callback():
    code = request.GET.get('code')
    r = client.request_access_token(code)
    at = r.access_token
    if at:
        expire = r.expires_in
        client.set_access_token(at,expire)
        user = client.get.account__get_uid()
        print user
        store.store_token(user['uid'],at,expire)
        sid = session.engage_session(user['uid'])
        print 'session_engaged'
        redirect('/main?sid=%s' % sid)
    else:
        redirect('/?error=error_retriving_access_token')

@route('/main')
def main():
    sid = request.GET.get('sid')
    uid = session.get_session(sid)
    if not uid:
        redirect('/')
    at,expire = store.get_token(uid)
    client.set_access_token(at,expire)
    print sid,uid,at
    cursor = 0
    users = []
    while 1:
        data = client.get.friendships__followers(uid=uid,count=200,cursor=cursor)
        print data['next_cursor'],data['total_number'],cursor
        for user in data['users']:
            user['_id'] = user['id']
            del user['id']
            print user['_id']
            db.weibo_users.save(user)
            users.append(user)

        cursor = data['next_cursor']
        if not cursor:
            break

    return stat.stat_users(uid,users).replace('\n','<br/>')

run(host='localhost', port='80', reloader=True)