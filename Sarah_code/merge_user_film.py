## film has: [genres] dir_name [actors]

def get_relevant_fields(user_json, film_json):
	relevant = {}
	try:
		dir = film_json["director"]
		u_dir = user_json["average_rating_by_director"][dir]
		relevant[dir] =
		for g in film_json["genres"]:
			relevant[g] = user_json["average_rating_by_genre"][g]
	except KeyError: # user hasn't rated anything from this director/genre/actor : this is fine
		pass # will 'pass' return to where the
	except Exception as e: # this is not fine
		print("Something happened: ", e)
		print(traceback.format_exc())
		raise

def test_get_revelant_fields():
	film_s = """{
		"name": "Inception",
		"lid": "34722",
		"tmdb_id": "27205",
		"number_of_ratings": 533369,
		"avg_rating": 4.18,
		"genres": [
			"Science Fiction",
			"Action",
			"Adventure"
		],
		"director": [
			"christopher-nolan"
		],
		"actor": [
			"leonardo-dicaprio",
			"ken-watanabe",
			"joseph-gordon-levitt",
			"marion-cotillard",
			"elliot-page"
		]
	}""" # more info obviously added later
	film_dict = json.loads((film_s.lower())) # make sure everything is lower case
	# user who has watched Inception: "deathproof" from 000_099.json
	all = json.loads( read_f((folder_path+"pop_users_000_099.json"))
	for u in all["users"]:
		if u["lid"] == "deathproof":
			#
	#end for
	return
