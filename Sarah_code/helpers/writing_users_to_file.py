
def write_user_list_to_file(path, lid_list, time_log=True):
	try:
		write_f(path, "")
		if time_log:
			start = dt.now()
			s = (str(start) + " : starting json file write to " + path +
				 "\n total films = " + str(len(film_info_dict)))
			print(s)
		first_entry = True
		i = 0
		for lid in lid_list:
			if time_log:
				s = ("\n\n"+d_sp+" "+str(i))
				print(s)
			user = LBoxd_User(maps_api_key, username=lid)
			if len(user.ratings) is 0: ## user has no films rated: don't write to json
				i = i+1
				continue

			user_js = (json.dumps(user.get_json())) ## no formatting (each user on new line but no \n inside users)
			if first_entry:
				first_entry = False
				user_js = "\n" + user_js
			else:
				user_js = (",\n") + user_js
			append_f(path, user_js)

			write_film_info_dict(user.films_added_to_dict)
			i = i+1
		#end for
		append_f(path, "\n] }")

		write_film_info_dict()
		if time_log:
			end = dt.now()
			s = ("\n" + str(end) + " : finished json file write to " + path +
				 "\n" + d_sp + " : JSON is valid:" + str(valid_json(path)) +
				 "\n" + d_sp + " : Time Taken: " + str(end-start))
			print(s)
	except Exception as e:
		append_f(path, "\n] }")
		write_film_info_dict()
		print("writing users failed :", e)
		print(traceback.format_exc())
	return
#end write_user_list_to_file()

def get_list_x00_x99(start, lid_list):
	max = len(lid_list)
	end = start+100
	if end > max: end = max
	new_list = lid_list[start:end]
	return new_list
#end

def write_100_users_from_csv(first_00, user_type="pop"):
	lid_list = get_csv_contents(pop_usernames_csv_path.replace("pop", user_type))
	new_list = get_list_x00_x99(first_00*100, lid_list)

	path = (folder_path + file_name_generic.replace("X", str(first_00)).replace("TYPE", user_type) )
	print(dt.now(), path)
	write_user_list_to_file(path, new_list)
	return
#end

def write_users_range(list_range, user_type="pop"):
	for i in list_range:
		write_100_users_from_csv(i, user_type=user_type)
	#end for
#end
