# -*- coding: utf-8 -*-

from public import *

def stat_users(uid,users):
	sex = [0,0]
	verified = []
	followers_count = 0
	locations = {}
	onlines = []
	for user in users:
		if user['verified']:
			verified.append([user['screen_name'],user['verified_reason'],user['followers_count']])
		if user['online_status']:
			onlines.append(user['screen_name'])
		locations[user['location'].split()[0]] = locations.get(user['location'].split()[0],0) + 1
		followers_count += user['followers_count']
		if user['gender'] == 'm':
			sex[0] += 1
		elif user['gender'] == 'f':
			sex[1] += 1

	locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
	verified = sorted(verified, key=lambda x: x[2], reverse=True)
	score = followers_count * 0.1 + 1.2 * sex[1] + len(locations) * 1.1 + len(verified) * 100 + len(users)
	db.user_stats.save({
		'_id': uid, 
		'sex': sex, 
		'verified': verified, 
		'fc': followers_count, 
		'loc': locations,
		'score': score,
		'nf': len(users)
	})
	return u'''你的微博影响力报告：


你共有微博粉丝： %d人 


其中： 	男性%d人，女性%d人

		
		已认证%d名，他们是：

			%s

你的粉丝来自%d个城市，分布如下：

	%s

当前在线的粉丝%d名：

	%s
	''' % (
		len(users),
		sex[0],
		sex[1],
		len(verified),
		'\n'.join([x[0] + ', ' + x[1] + u'(TA有' + str(x[2]) + u'名粉丝)' + '\n' for x in verified]),
		len(locations),
		'\n'.join([x[0] + ', ' + str(x[1]) + '\n' for x in locations]),
		len(onlines),
		'\n'.join(onlines),
	)