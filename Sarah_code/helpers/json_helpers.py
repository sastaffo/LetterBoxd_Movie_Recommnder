file_name_generic = "TYPE_users_X00_X99.json"


def fix_json_mult_users(all):
	new_all_s = "{ \"users\": [\n"
	first_user = True
	i = 0
	for u in all["users"]:
		add_s = ""
		try:
			user_dump = json.dumps(u) ## user on all one line
			add_s = user_dump[0] + "\n" + user[1:] # inserts a newline after first open bracket (collapsable)
		except:
			try: s = u.lid
			except: s = "(couldn't get user.lid)"
			s = "failed on user:"+ i + ", lid=" + s +" >>\n" + traceback.format_exc()
			print(s)
			return
		if first_user:
			first_user = False
		else:
			add_s = ",\n" + add_s
		new_all_s = new_all_s + add_s
		if (i%45) == 0:
			print(i, end="\n    ")
		else: print(i, end=" ")
		i = i+1
	print()
	new_all_s = new_all_s + "\n] }"
	return new_all_s
#end


def fix_json_in_file(x00=0, user_type="pop"):
	file_name = (file_name_generic).replace("X", str(x00)).replace("TYPE", user_type)
	file_path = folder_path + file_name

	dest_name = (file_name).replace(".json", "_new.json")
	dest_path = (folder_path + dest_name)

	print(">",dest_name, "\n    users:", end=" ")
	f = open(file_path, "r")
	all = json.loads(f.read())
	f.close()
	new_all_s = fix_json_mult_users(all)
	try:
		json.loads(new_all_s)
		print("    valid json")
		f = open(dest_path, "w+")
		f.write(new_all_s)
		print("    written to file <", dest_path, ">")
		f.close()
	except Exception as e:
		try: f.close() # closes file if open, ignores if not
		except: pass
		print("\nfailed to write new file <", dest_path, "> :", e)
		print(traceback.format_exc())
		inv_path = dest_path.replace("new", "invalid")
		print("\nWriting to", inv_path, "instead")
		f = open(inv_path, "w+")
		f.write(new_all_s)
		f.close()
	return
#end

print(dt.now())

def fix_json_files_loop(range, user_type="pop"):
	for r in range:
		fix_json_in_file(r, user_type)
		print()
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


print(dt.now())
#validate_json(max_00=4, new=False, user_type="gen")
