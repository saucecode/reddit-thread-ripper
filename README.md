# reddit-thread-ripper
A program to download an entire Reddit thread's comment section. It can be used as a standalone script or as part of a python program.

## Library Usage

    import ripper
	url = "https://www.reddit.com/r/Cyberpunk/comments/5xepe6/hong_kong_side_street_on_a_dark_rainy_night/.json"
	topic, comments = ripper.downloadCommentsSection(url)

	print('Downloaded', len(comments), 'top-level comments for thread:', topic['title'])

## Script Usage

    $ python ripper.py https://www.reddit.com/r/Cyberpunk/comments/5xepe6/hong_kong_side_street_on_a_dark_rainy_night/

Will write to a file `5xepe6.json`. This file will (by default) contain the following structure. The root element is an array of length 2. First element is a dictionary containing details about the main post. Second element is an array of all the comments. Each comment contains an array of reply comments.

	[
		{
			"body": null,
			"permalink": "/r/newzealand/comments/5xl1uc/nz_post_meridiem_random_discussion_thread_sun_05/",
			"score": 8,
			"author": "AutoModerator",
			"url": "https://www.reddit.com/r/newzealand/comments/5xl1uc/nz_post_meridiem_random_discussion_thread_sun_05/",
			"title": "NZ Post Meridiem Random Discussion Thread - Sun 05 March, 2017",
			"created": 1488686704.0,
			"id": "5xl1uc"
		},

		[
			{
				"body": "Miss17 has been in her room crying because she managed to lose her bikini top at the beach, in front of her schools entire crop of year 13s.",
				"created": 1488687185.0,
				"author": "awfulrob",
				"score": 12,
				"replies": [
					{
						"body": "Oh noooo that is a pretty fair call for crying.",
						"created": 1488688330.0,
						"author": "thecosmicradiation",
						"score": 7,
						"replies": [],
						"commentid": "deix7f6"
					},
					{
						"body": "Poor thing, I'd be crying too! Get that girl some ice cream ",
						"created": 1488689364.0,
						"author": "Chutlyz",
						"score": 1,
						"replies": [],
						"commentid": "deixtga"
					}
				],
				"commentid": "deiwiq3"
			},
			{
				"body": "What's Sunday dinner at your place? Some apple and chicken creation on the cards here. Not sure how I'm feeling about it. ",
				"created": 1488686748.0,
				"author": "Roysterbout",
				"score": 4,
				"replies": [
					...
				],
				"commentid": "deiwbus"
			},

			...
		]
	]

You can view this file in full by viewing `5xl1uc.json` in this repo. It is a rip of [this thread from /r/NewZealand](https://www.reddit.com/r/newzealand/comments/5xl1uc/nz_post_meridiem_random_discussion_thread_sun_05/)
