folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/"

api_file_path = folder_path.replace("Sarah_data/","API_keys/google_maps_api.txt")
maps_api_key = read_f(api_file_path)
print(maps_api_key)

pop_usernames_csv_path = (folder_path + "pop_usernames.csv")
pop_users_json_path = (folder_path + "pop_users.json")
test_json_path = (folder_path + "test_users.json")
film_info_path = (folder_path + "sarah_film_info.json")

file_name_generic = "TYPE_users_X00_X99.json"

film_info_dict = {} # {LID : {"director":[], "actors":[],"genres":[]}}
fi_str = read_f(film_info_path)
if fi_str is None:
	print("file not found")
else:
	if fi_str == "":
		print("no films found")
	else:
		try:
			film_info_dict = json.loads(fi_str)
			print("films found =", len(film_info_dict))
		except:
			print()


d_sp = "                          "
