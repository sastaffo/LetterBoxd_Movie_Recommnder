lboxd_url = "https://letterboxd.com"
director = "director"
actor = "actor"
genre = "genre"
url = "url"
name = "name"

class LBoxd_User():
	def __init__(self, maps_api_key, profile_url=None, username=None, time_log=False):
		self.lid = None
		self.profile_url = None
		if profile_url is not None:
			if profile_url[-1] == "/": self.profile_url = profile_url
			else: self.profile_url = (profile_url + "/")

			self._generate_lid()
			if username is not None and username != self.lid: raise ValueError("URL does not match username provided")

		elif profile_url is None and username is not None:
			self.lid = username
			self.profile_url = (lboxd_url + "/" + self.lid + "/")
		else:
			error_s = ("please initialise LBoxd_User object with one of profile_url and username\n" + "Found: profile_url=" + profile_url + " and username=" + username)
			raise ValueError(error_s)
		#end if

		self.time_log = time_log
		setup_time_start = dt.now()
		s = (str(setup_time_start) + " : " + self.lid + " START")
		print(s)
		#end if
		self.films_added_to_dict = 0

		self.maps_api_key = maps_api_key

		profile_page = requests.get(self.profile_url, allow_redirects=True)
		self.profile_bsoup = BSoup(profile_page.content, 'html.parser')
		self._generate_name()

		self.location_str = None
		self._generate_location_str()
		self.country = get_country(self.location_str, self.maps_api_key)

		self.ratings_base_url = (self.profile_url + "films/ratings/")
		self.ratings_pages_bsoups = {}
		self._generate_ratings_pages()
		self._generate_ratings_pages_bsoups()

		self.ratings = {}
		self._generate_ratings()
		if len(self.ratings) is 0:
			end_time = dt.now()
			s = (str(end_time) + " : " + str(end_time - setup_time_start) + " : " + self.lid + " END: no films")
			print(s)
			return

		self._setup_averages()
		self.json = None
		end_time = dt.now()
		s = (str(end_time) + " : " + str(end_time - setup_time_start) + " : " + self.lid + " END")
		print(s)
	#end init()

	def _setup_averages(self):
		self._generate_average_rating()
		self.average_rating_by_genre = self._generate_average_rating_by_X(genre)
		self.average_rating_by_director = self._generate_average_rating_by_X(director)
		self.average_rating_by_actor = self._generate_average_rating_by_X(actor)
	#end

	def _generate_name(self):
		name_div = self.profile_bsoup.find("div", {"class" : "profile-name-wrap"})
		try:
			self.name = (name_div.find("h1")).text
		except: self.name = self.lid
		return
	#end _generate_name()

	def _generate_location_str(self):
		location_pin_d = "M4.25 2.735a.749.749 0 111.5 0 .749.749 0 11-1.5 0zM8 4.75c0-2.21-1.79-4-4-4s-4 1.79-4 4a4 4 0 003.5 3.97v6.53h1V8.72A4 4 0 008 4.75z"
		try:
			meta_div = self.profile_bsoup.find("div", {"class" : "profile-metadata js-profile-metadata"})
			sub_meta_divs = meta_div.find_all("div", {"class" : "metadatum -has-label js-metadatum"})
			for sub in sub_meta_divs:
				sub.find("path", {"d" : location_pin_d})
				self.location_str = sub.find("span", {"class" : "label"}).text
				return
		except Exception as e:
			self.location_str = None
			return
		return
	#end _generate_location_str

	def _generate_ratings_pages(self):
		ratings_page = requests.get(self.ratings_base_url, allow_redirects=True)
		pg1_soup = BSoup(ratings_page.content, 'html.parser')
		self.ratings_pages_bsoups[self.ratings_base_url] = pg1_soup

		pagin_div = pg1_soup.find("div", {"class" : "paginate-pages"})
		if pagin_div is None:
			self.ratings_pages = 1
		else:
			list_items = pagin_div.find_all("li")
			last_page = list_items[-1]
			self.ratings_pages = int(last_page.find("a").text)
		return
	#end _generate_ratings_pages()

	def _generate_ratings_pages_bsoups(self):
		if len(self.ratings_pages_bsoups) is 0:
			page = requests.get(self.ratings_base_url, allow_redirects=True)
			soup = BSoup(page.content, 'html.parser')
			self.ratings_pages_bsoups[self.ratings_base_url] = bsoup
		#end if
		if self.time_log:
			s = (str(dt.now()) + " : pages souped (out of "+str(self.ratings_pages)+"): \n"+ d_sp+" : 1")
			print(s, end =", ")
		for i in range(1, self.ratings_pages):
			url = (self.ratings_base_url + "page/" + str(i+1) + "/")
			page = requests.get(url, allow_redirects=True)
			bsoup = BSoup(page.content, 'html.parser')
			self.ratings_pages_bsoups[url] = bsoup
			if self.time_log: print_num((i+1))
		#end for
		if self.time_log:
			s = ("\n" + str(dt.now()) + " : finished souping")
			print(s)
		return
	#end _generate_ratings_pages_bsoups()


	def _generate_film_info(self, film_url, film_lid, film_name):
		page = requests.get(film_url, allow_redirects=True)
		pg_soup = BSoup(page.content, 'html.parser')
		crew_div = pg_soup.find("div", {"id" : "tab-crew"})
		film_director = []
		if crew_div is not None:
			crew_link_list = crew_div.find_all("a", href=True)
			for a in crew_link_list:
				link = a['href']
				link_split = link.split("/") # -> ["", "crew-type", "name", ""]
				if link_split[1] == director:
					film_director.append(link_split[2])
					break
				#end if
			#end for
		#end if
		cast_div = pg_soup.find("div", {"id": "tab-cast"})
		film_actors = []
		if cast_div is not None:
			cast_link_list = cast_div.find_all("a", href=True)
			for a,i in zip(cast_link_list, range(5)): # get first 5 actors (will only run for i<5)
				link = a['href']
				link_split = link.split("/") # -> ["", "actor", "name", ""]
				film_actors.append(link_split[2])
			#end for
		#end if
		genres_div = pg_soup.find("div", {"id" : "tab-genres"})
		film_genres = []
		if genres_div is not None:
			genre_links = genres_div.find_all("a")
			for a in genre_links:
				film_genres.append(a.text)
			#end for
		#end if
		film_info_dict[film_lid] = {url : film_url,
									name: film_name,
									genre : film_genres ,
									director : film_director,
									actor : film_actors }
		return (film_genres, film_director, film_actors) # returns 3 lists: director, actors, genres
	#end _generate_film_info

	def _generate_ratings_by_page(self, bsoup):
		# add each to self.ratings dict
		cols_div = bsoup.find("section", {"class" : "section col-main overflow"})
		if cols_div is None: return

		ul_list = cols_div.find("ul", {"class" : "poster-list -p150 -grid"})
		if ul_list is None: return
		list_items = ul_list.find_all("li")
		i = 1
		for li in list_items:
			try:
				div = li.find("div")
				film_lid = div["data-film-id"]
				film_link = div["data-target-link"]
				film_name = (film_link.split("/"))[2]
				film_url = lboxd_url + film_link

				p = li.find("p")
				rating_l = p.find("span")["class"]
				rating_10_s = (rating_l[1]).split("-")[1]
				film_rating = float(rating_10_s)/2.

				new_film=" "
				if film_lid in film_info_dict:
					film_director = film_info_dict[film_lid][director]
					film_actors = film_info_dict[film_lid][actor]
					film_genres = film_info_dict[film_lid][genre]
				else:
					new_film = "n"
					self.films_added_to_dict = self.films_added_to_dict + 1
					(film_genres, film_director, film_actors) = self._generate_film_info(film_url, film_lid, film_name)
				#end if
				self.ratings_simple[film_lid] = film_rating
				self.ratings[film_lid] = {"rating": film_rating,
											url : film_url,
											name : film_name,
											genre: film_genres,
											director: film_director,
											actor: film_actors }
				if self.time_log: print_num(i, n=new_film)
				i = i+1
			except Exception as e:
				print("\nFilm Collection Failed: ", e)
				print(traceback.format_exc())
				print("content: ", li, "\n")
		#end for
		return
	#end get_rating_by_page()

	def _generate_ratings(self):
		self.ratings = {}
		self.ratings_simple = {}
		# scrapes all bsoups in self.page_bsoups for all user urls on the page
		i = 1
		for bsoup in self.ratings_pages_bsoups.values():
			if self.time_log:
				s = ("    Parsing films on pg"+str(i))
				print(s, end =": ")
			self._generate_ratings_by_page(bsoup)
			i = i+1
			if self.time_log: print()
		#end for
		return
	#end _generate_ratings()

	def _generate_average_rating(self):
		sum = 0
		count = len(self.ratings)
		for film in self.ratings:
			rating = self.ratings[film]["rating"]
			sum = sum + rating
		#end for
		self.average_rating = (sum/count)
		return
	#end _generate_average_rating

	def _generate_average_rating_by_X(self, X_str):
		ratings_by_X = {}
		# add rating for each film to dict of genres
		for film in self.ratings:
			rating = self.ratings[film]["rating"]
			Xs = self.ratings[film][X_str]
			if Xs is None: return
			for x in Xs:
				try:
					ratings_by_X[x].append({"film_lid" : film, "rating" : rating})
				except:
					ratings_by_X[x]= [{"film_lid" : film, "rating" : rating}]
			#end for
		#end for
		if self.time_log:
			s = ("    Averages by "+ X_str +"("+ str(len(ratings_by_X)) +")")
			print(s, end=": ")
		# get sum/count of ratings for each x, find average value, add to average_rating_by_X
		average_rating_by_X = {}
		for x in ratings_by_X: # eg each genre found in self.ratings
			x_lids = []
			x_ratings = ratings_by_X[x]
			sum = 0.
			count = len(x_ratings)
			for film in x_ratings:
				x_lids.append(film["film_lid"])
				sum = sum + film["rating"]
			#end for
			x_avg = (sum/count)
			average_rating_by_X[x] = { "avg" : x_avg,
									   "count" : count,
									   "avg_minus_tot_avg" : (x_avg - self.average_rating),
									   "film-lids" : x_lids }
		#end for
		if self.time_log: print("done")
		return average_rating_by_X
	#end _generate_average_rating_by_X()

	def print_all(self):
		print("LID = ", self.lid)
		print("    name=", self.name)
		print("    obj=", self)
		print("    profile_url=", self.profile_url)
		print("    location_str = ", self.location_str)
		print("    country = ", self.country)
		print("    #ratings pages = ", self.ratings_pages)
		print("    #ratings = ", len(self.ratings))
		print("    average rating = ", self.average_rating)
		print("    #genres = ", len(self.average_rating_by_genre))
		print("    average by genre (3) = ", self._X_str(self.average_rating_by_genre))
		print("    #directors = ", len(self.average_rating_by_director))
		print("    average by directors (3) = ", self._X_str(self.average_rating_by_director))
		print("    #actors = ", len(self.average_rating_by_actor))
		print("    average by actors (3) = ", self._X_str(self.average_rating_by_actor))
		print("    json exists = ", (self.json != None))
		print("\n\n")
		return
	#end print_all()

	def _X_str(self, avg_dict):
		sub_dict = {}
		if len(avg_dict) > 3:
			avg_keys = list(avg_dict.keys())
			for i in range(3):
				x = random.choice(avg_keys)
				sub_dict[x] = avg_dict[x]
			#end for
		else: sub_dict = avg_dict
		#end if
		x_str = ""
		for x in sub_dict:
			x_str = x_str + ("\n        " + x + "("+ str(sub_dict[x]["count"]) +") = " + str(sub_dict[x]["avg"]))
		#end for
		return x_str
	#end

	def get_json(self):
		if self.json is not None:
			return self.json
		else:
			# generate json
			self.json = {
				"lid" : self.lid,
				"name" : self.name,
				"profile_url" : self.profile_url,
				"location_string" : self.location_str,
				"country" : self.country,
				"average_rating" : self.average_rating,
				"ratings_by_film" : self.ratings_simple,
				"average_rating_by_genre" : self.average_rating_by_genre,
				"average_rating_by_director" : self.average_rating_by_director,
				"average_rating_by_actor" : self.average_rating_by_actor,
			}
			return self.json
	#end get_json()

#end Letterboxd_User

def print_num(i, n=""):
	s = (str(i) + n)
	if (i % 30) is 0:
		s = s + (",\n" + d_sp + " :")
	else:
		s = s + (",")
	print(s, end=" ")
#end
print(dt.now())
