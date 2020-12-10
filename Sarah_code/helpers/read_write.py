def read_f(path):
	try:
		f = open(path, "r")
		s = f.read()
		f.close()
		return s
	except FileNotFoundError:
		print("file not found")
		return None
	except Exception as e:
		raise e
#end


def append_f(path, s):
	f = open(path, "a+")
	f.write(s)
	f.close()
	return
#end


def write_f(path, s):
	f = open(path, "w+")
	f.write(s)
	f.close()
	return
#end
print(dt.now())
