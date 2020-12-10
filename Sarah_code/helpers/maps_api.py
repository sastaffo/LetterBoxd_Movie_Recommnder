def get_country(location_str, api_key, printbool=False, printjson=False):
	# country name = json["results"][i]["address_components"][j]["long_name"] (if "country" in ["types"])
	# for all results, for all address_components, if type==country, get long_name
	if location_str is None:
		if printbool: print("location_str is None")
		return None

	address = str.replace(location_str, " ", "+")
	maps_base_url = ("https://maps.googleapis.com/maps/api/geocode/json")
	maps_params = {"address": address, "key": maps_api_key}

	# JSON labels
	ctry = "country"
	adr_comps = "address_components"
	poi = "point_of_interest"
	ln = "long_name"
	try:
		page = requests.get(maps_base_url, params=maps_params, allow_redirects=True)
		json_str = page.text
		if printjson: print(json_str)
		loc_json = json.loads(json_str)
		if loc_json["status"] == "OK":
			results = loc_json["results"]
			for r in results:
				if ctry in r["types"]:
					if printbool: print(location_str, " is a ", ctry)
					return location_str
				elif poi in r["types"]:
					if printbool: print(location_str, " is a ", poi, " (",ctry," = None)")
					return None
				#end if
				comps = r["address_components"]
				for c in comps:
					if ctry in c["types"]:
						country = c[ln]
						if printbool: print(location_str, " -> ", ctry," = ", country, "\n")
						return country
					#end if
				#end for
			#end for
		else:
			if printbool: print(location_str, " returned ", loc_json["status"], " (",ctry," = None)")
			return None
		#end if
		return None
	except Exception as e:
		if printbool: print(traceback.format_exc())
		if printbool: print("couldn't get country of ", location_str, " (",ctry," = None)\n", e)
		return None
#end get_country()

print(dt.now())
