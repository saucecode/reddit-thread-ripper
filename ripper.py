from __future__ import print_function
import json, requests, os

sess = requests.Session()

def getjson(url):
	print('downloading',url)
	ret = sess.get(url, headers={'User-Agent': 'ripperino/1.0'}).json()
	return ret

def parseReplies(toplevelcomments, out):
	for comment in toplevelcomments:
		if comment['kind'] == 't1':
			newitem = {
				'author': comment['data']['author'],
				'created': comment['data']['created_utc'],
				'score': comment['data']['score'],
				'commentid': comment['data']['id'],
				'body': comment['data']['body'],
				'replies': []
			}
			out.append(newitem)

			if 'replies' in comment['data'] and len(comment['data']['replies']) > 0:
				parseReplies(comment['data']['replies']['data']['children'], newitem['replies'])

		elif comment['kind'] == 'more':
			idarray = [topic['permalink'] + x for x in comment['data']['children']]
			if len(idarray) == 0:
				continue
			print('MORE! grabbing', len(idarray), 'more comments using requests.get')
			newcomments = [getjson('https://reddit.com' + x + '/.json') for x in idarray]

			for camment in newcomments:
				if len(camment[1]['data']['children']) == 0:
					continue
				toplevel = camment[1]['data']['children'][0]['data']
				responses = toplevel['replies']

				newitem = {
					'author': toplevel['author'],
					'created': toplevel['created_utc'],
					'score': toplevel['score'],
					'commentid': toplevel['id'],
					'body': toplevel['body'],
					'replies': []
				}
				out.append(newitem)

				if not responses == '':
					parseReplies(responses['data']['children'], newitem['replies'])

def downloadCommentsSection(json_url):
	data = requests.get(json_url, headers={'User-Agent': 'ripperino/1.0'}).json()

	parsed = []
	topic = {
		'author': data[0]['data']['children'][0]['data']['author'],
		'created': data[0]['data']['children'][0]['data']['created_utc'],
		'score': data[0]['data']['children'][0]['data']['score'],
		'permalink': data[0]['data']['children'][0]['data']['permalink'],
		'url': data[0]['data']['children'][0]['data']['url'],
		'title': data[0]['data']['children'][0]['data']['title'],
		'body':  data[0]['data']['children'][0]['data']['body'] if 'body' in data[0]['data']['children'][0]['data'] else '',
		'id': data[0]['data']['children'][0]['data']['id']
	}

	parseReplies(data[1]['data']['children'], parsed)

	return topic, parsed

if __name__ == '__main__':

	import sys

	if not len(sys.argv) == 2:
		print('usage:', sys.argv[0], '[reddit thread URL]')
		sys.exit(0)

	topic, parsed = downloadCommentsSection(sys.argv[1] + '.json')

	with open('%s.json' % topic['id'],'w') as f:
		json.dump([topic, parsed], f, indent=4, separators=(',', ': '))
