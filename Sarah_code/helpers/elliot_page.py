## replace all instances of "ellen-page" with "elliot-page" in ALL files
## writes to csv if both names occur
def file_replace_elliot_page(user_type="pop"):
	fi_path = film_info_path.replace(".json", "_new.json")
	fi_s = read_f(film_info_path)
	fi_s = fi_s.replace("ellen-page", "elliot-page")
	print("film info string replaced", dt.now())
	write_f(fi_path, fi_s)
	print("film info written", dt.now())

	uj_path = (folder_path + "TYPE_users_X00_X99_new.json").replace("TYPE", user_type)
	u_start = dt.now()
	u_prev = u_start
	for i in range(39):
		i_path = uj_path.replace("X", str(i))
		i_s = read_f(i_path)
		print("\n",i, "file read")
		if (i_s.find("ellen-page")) == -1:
			# if file contains neither, no action needed
			# if file contains 'elliot-page' but not 'ellen-page', no action needed
			print("    no replacement needed")
			u_prev = dt.now()
			continue
		else:
			if (i_s.find("elliot-page")) == -1:
				# if file contains 'ellen-page' but not 'elliot-page', straight replace
				i_s = i_s.replace("ellen-page", "elliot-page")
				print("    straight replace done")
				write_f(i_path, i_s)
				print("    written in", (dt.now()-u_prev))
				u_prev = dt.now()
			else:
				# if file contains both: add to csv to deal with later
				elliot_fixes = folder_path + "elliot_fixes.csv"
				s = i_path + "\n"
				append_f(elliot_fixes, s)
				print("    contains both: added to elliot_fixes.csv ", (dt.now()-u_prev))
				u_prev = dt.now()
			#end if
		#end if
	#end for
	print("\nall user json files parsed in ", (dt.now()-u_start))
	return
#end


## replace all instances in the files where both names exist
def apply_elliot_fixes():
	csv_path = folder_path + "elliot_fixes.csv"
	file_paths = read_f(csv_path).split("\n")
	for path in file_paths:
		print("file: ", path.split("/")[-1] )
		users_dict = json.loads(read_f(path))
		for i in range(len(users_dict["users"])):
			print("  ",i, end=":\n")
			u = users_dict["users"][i]
			ellen_avg = {}
			elliot_avg = {}
			try:
				ellen_avg = u["average_rating_by_actor"]["ellen-page"]
			except KeyError:
				# user does not have ellen-page as an actor
				print()
				continue # to next user
				try:
					elliot_avg = u["average_rating_by_actor"]["elliot-page"]
				except KeyError:
					# user does not have elliot-page but *does* have ellen-page
					users_dict["users"][i]["average_rating_by_actor"]["elliot-page"] = ellen_avg
					continue # to next user
					# user has both elliot-page and ellen-page
					# todo: merge
					#
