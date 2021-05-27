from __future__ import print_function
import json, markdown, time, sys

if not len(sys.argv) == 2:
	print('usage:', sys.argv[0], '[threadfile.json]')
	print('will output to [threadfile.json].html')

	sys.exit(0)

with open(sys.argv[1], 'r') as f:
	data = json.load(f)[1]

html = '''<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>output</title>
		<style>
			body {
				font-family: sans-serif;
			}

			.comment {
				margin-left: 32px;
				padding: 4px;
				border: 1px solid black;
			}

			.username {
				color: #22f;
			}

			p {
				font-size: 10pt;
			}
		</style>
	</head>
	<body>
%s
	</body>
</html>
'''

def formComment(comment):
	ret = '<div class="comment"><small><span class="username">%s</span> %s <b>%i</b></small><p>%s</p><!--__REPLIES__--></div>' % (
		comment['author'],
		time.ctime(comment['created']),
		comment['score'],
		markdown.markdown(comment['body'])
	)

	return ret

def doTheDing(comment):
	base = formComment(comment)

	if len(comment['replies']) > 0:
		replies = []
		for reply in comment['replies']:
			replies.append(doTheDing(reply))

		base = base.replace('<!--__REPLIES__-->', '\n'.join(replies))

	return base


out = []

for comment in data:
	out.append(doTheDing(comment))

html = html % ('\n\n'.join(out),)

with open(sys.argv[1] + '.html','w') as f:
	f.write(html)
