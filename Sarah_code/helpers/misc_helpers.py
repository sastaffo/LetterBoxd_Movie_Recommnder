def write_film_info_dict(new_films = 0, printbool=True):
	if new_films > 0:
		j = json.dumps(film_info_dict)
		write_f(film_info_path, j)
		num_film = len(film_info_dict)
		if printbool: print("film_info_dict written. total films = " + str(num_film) + " [new=" +str(new_films)+"]")
	else:
		if printbool: print("no films added to film_info_dict")
	return

def get_csv_contents(path=pop_usernames_csv_path):
	with open(path) as f:
		csv_dump = csv.reader(f)
		nested_list = list(csv_dump)

	list_1d = []
	for nest in lid_nested_list:
		for el in nest:
			list_1d.append(el)
	return list_1d
#end


def rm_duplicates():
	philip_path = folder_path.replace("Sarah_data", "Philip's Data")
	s = read_f((philip_path+"all_users.json"))
	users = json.loads(s)
	print("on open:", len(users))
	pop_users = get_csv_contents(pop_usernames_csv_path)
	for u in pop_users:
		try:
			users.remove(u)
		except ValueError:
			pass
	print("rm populars:", len(users))
	## remove internal duplicates
	users_2 = (list(dict.fromkeys(users)))
	print("rm duplicates:", len(users_2))
	write_user_lids(users_2, (gen_usernames_csv_path))
	print("written")
	return
#end


def validate_json(list_range=None, max_00=38, new=True, user_type="pop"):
	path = (folder_path + "TYPE_users_X00_X99.json").replace("TYPE", user_type)
	if new: path = path.replace(".json", "_new.json")
	if list_range is None:
		list_range = []
		for j in range(max_00+1): list_range.append(j)

	for i in list_range:
		i_path = path.replace("X", str(i))
		s = (str(i) + " - <" + i_path + ">" + ":")
		print(s)
		try:
			f = open(i_path, "r")
			i_json = json.loads(f.read())
			print("    json valid", end=": ")
			num = len(i_json["users"])
			print(" len('users') =", num)
		except FileNotFoundError as fnfe:
			print("    couldn't find", path)
		except simplejson.decoder.JSONDecodeError as jde:
			print("    json invalid", jde)
		except Exception as e:
			print("    oops", e)
		#end try
		print()
	#end for
#end
