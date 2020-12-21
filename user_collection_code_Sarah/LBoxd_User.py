# file created 29 Nov 2020 sastaffo@tcd.ie

from google.colab import drive
drive.mount('/content/drive')

"""## IMPORTS"""

from bs4 import BeautifulSoup as BSoup
import requests
from datetime import datetime as dt
import random
import traceback
import copy
import json
import csv
from json import JSONDecodeError

print(dt.now())

"""## basic read/write methods"""

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

def read_csv_1d(path):
    read = read_f(path)
    if read is not None:
        return read.split("\n")
    return None

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

def write_csv_1d(path, s_list):
    s = "\n".join(s_list)
    write_f(path, s)
    return
#end

def valid_json(path):
    j = read_f(path)
    try:
        json.loads(j)
        return True
    except:
        return False
#end

print(dt.now())

"""## Set Up Global Vars"""

folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/"
test_folder_path = folder_path + "test_dataset/"

api_file_path = folder_path.replace("Sarah_data/","API_keys/google_maps_api.txt")
maps_api_key = read_f(api_file_path)
print(maps_api_key)

film_info_path = (folder_path + "sarah_film_info.json")


film_info_dict = {} # {LID : {"director":[], "actors":[],"genres":[]}}
fi_str = read_f(film_info_path)
if fi_str is None:
    print("file not found")
else:
    if fi_str == "":
        print("no films found")
    else:
        film_info_dict = json.loads(fi_str)
        print("films found =", len(film_info_dict))

cont_path = folder_path.replace("Sarah_data", "Shaun's Data") + "countries_by_continent.json"
cont_str = read_f(cont_path)
continents = json.loads(cont_str)
print("got continent data")


c_map_path = folder_path + "country_mappings.json"
c_map_str = read_f(c_map_path)
country_map = json.loads(c_map_str)
print("got country map")

d_sp = ""
for i in range(26):
    d_sp = d_sp + " "
#end

print(dt.now())

"""## Country + Continent"""

"""### get_country() => Google Maps API"""

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

"""### find_continent()"""

write_missing_path = folder_path + "missing_countries.csv"

def find_continent(c, username):
    if c is None:
        return (None, None)
    cnty_str = c.lower()
    if cnty_str in country_map:
        cnty_str = country_map[cnty_str]
    for cont in continents:
        cont_list = continents[cont]
        if cnty_str in cont_list:
            return (cnty_str, cont)
    #end for
    s = (cnty_str + "," + username + "\n")
    append_f(write_missing_path, s)
    return (cnty_str, None)
#end
print(dt.now())

"""# LBoxd_User class"""

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
        s = (str(setup_time_start) + " : " + self.lid)
        if self.time_log: print(s, "START")
        else: print(self.lid, end=" >> ")
        #end if
        self.films_added_to_dict = 0

        self.maps_api_key = maps_api_key

        profile_page = requests.get(self.profile_url, allow_redirects=True)
        self.profile_bsoup = BSoup(profile_page.content, 'html.parser')
        self._generate_name()

        self.location_str = None
        self._generate_location_str()
        tmp_country = get_country(self.location_str, self.maps_api_key)
        (self.country, self.country_group) = find_continent(tmp_country, self.lid)

        self.ratings_base_url = (self.profile_url + "films/ratings/")
        self.ratings_pages_bsoups = {}
        self._generate_ratings_pages()
        self._generate_ratings_pages_bsoups()

        self.ratings = {}
        self._generate_ratings()
        if len(self.ratings) is 0:
            end_time = dt.now()
            if self.time_log: s = (str(end_time) + " : " + str(end_time - setup_time_start) + " : " + self.lid + " END: no films")
            else: s = (str(end_time - setup_time_start) + " END: no films")
            print(s)
            return

        self._setup_averages()
        self.json = None
        end_time = dt.now()
        if self.time_log: s = (str(end_time) + " : " + str(end_time - setup_time_start) + " : " + self.lid + " END: " + str(len(self.ratings)) + " films (new=" + str(self.films_added_to_dict) + ")")
        else: s = (str(end_time - setup_time_start) + " END: " + str(len(self.ratings)) + " films (new=" + str(self.films_added_to_dict) + ")")
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
                    (film_genres, film_director, film_actors) = generate_film_info(film_url, film_lid, film_name)
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
                "country_group": self.country_group,
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

"""# helper methods

## misc methods
"""

def generate_film_info(film_url, film_lid, film_name):
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
#end generate_film_info

"""### write_film_info_dict()"""

def write_film_info_dict(new_films = 0):
    if new_films > 0:
        j = json.dumps(film_info_dict)
        write_f(film_info_path, j)
        num_film = len(film_info_dict)
    return
print(dt.now())

"""## writing users to file"""

"""### write_user_list_to_file()"""

write_folder_path = folder_path + "writing/"
def write_user_list_to_file(file_name, lid_list, time_log=True):
    path = write_folder_path + file_name

    try:
        write_f(path, "{ \"users\" : [\n")
        if time_log:
            start = dt.now()
            s = (str(start) + " : starting json file write to " + path +
                 "\n total films = " + str(len(film_info_dict)))
            print(s)
        first_entry = True
        i = 0
        for lid in lid_list:
            if time_log:
                s = ("\n"  + str(i) + " > " + str(dt.now()))
                print(s)
            user = LBoxd_User(maps_api_key, username=lid)
            if len(user.ratings) is 0: ## user has no films rated: don't write to json
                i = i+1
                continue

            user_js = (json.dumps(user.get_json())) ## no formatting
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


        if valid_json(path):
            s = read_f(path)
            path = path.replace("writing", "safety")
            write_f(path, s)
            print("writing to safety")
        else:
            s = read_f(path)
            path = path.replace("writing", "inv_json")
            write_f(path, s)
            print("writing to inv_json")


        write_film_info_dict()
        if time_log:
            end = dt.now()
            s = ("\n" + str(end) + " : finished json file write"
                 "\n" + d_sp + " : Time Taken: " + str(end-start))
            print(s)
    except Exception as e:
        append_f(path, "\n] }")
        write_film_info_dict()
        print("writing users failed :", e)
        print(traceback.format_exc())
    return
#end write_user_list_to_file()

print(dt.now())

"""### get_list_x00_x99()
get sublist of 100 users from list
"""

def get_list_x00_x99(start, lid_list):
    max = len(lid_list)
    end = start+100
    if end > max: end = max
    new_list = lid_list[start:end]
    return new_list
#end

"""### write_100_users_from_csv()"""

file_name_generic = "TYPE_users_X00_X99.json"
def write_100_users_from_csv(first_00, csv_path, user_type="pop"):
    lid_list = read_csv_1d(csv_path)
    new_list = get_list_x00_x99(first_00*100, lid_list)

    file_name = ( file_name_generic.replace("X", str(first_00)).replace("TYPE", user_type) )
    print(dt.now(), file_name)
    write_user_list_to_file(file_name, new_list)
    return
#end


"""# Running

### check all files in writing/ exist and are valid
"""

check_path = folder_path + "writing/TYPE_users_X00_X99.json"
def check_all_exists():
    # 0 - 57 gen
    # 0 - 38 pop
    ppath = check_path.replace("TYPE", "pop")
    for p in range(39):
        s = read_f(ppath.replace("X", str(p)))
        if s is None:
            print("can't find pop users", p)
        else:
            try:
                json.loads(s)
            except JSONDecodeError as jde:
                print("got error for pop", p, ":", jde)
    #end for
    print("read all pop")

    upath = check_path.replace("TYPE", "gen")
    for u in range(58):
        s = read_f(upath.replace("X", str(u)))
        if s is None:
            print("can't find gen users", u)
        else:
            try:
                json.loads(s)
            except JSONDecodeError as jde:
                print("got error for gen", u, ":", jde)
    #end for
    print("read all gen")
    return
#end
#check_all_exists()

"""### write_users_range()"""

def write_users_range(csv_path, list_range=None, max=0, min=0, user_type="pop"):
    if list_range is None:
        list_range = []
        for i in range(min, max+1):
            list_range.append(i)

    for i in list_range:
        write_100_users_from_csv(i, user_type=user_type, csv_path=csv_path)
    return
#end
#pop_test_csv_path = test_folder_path + "pop_users_merged.csv"
#write_users_range(pop_test_csv_path, max=23, min=9, user_type="test_pop")
#gen_test_csv_path = test_folder_path + "gen_users_merged.csv"
#write_users_range(gen_test_csv_path, max=0, min=0, user_type="test_gen")

"""# other running

### fix invalid gen jsons
"""

src_path = folder_path + "gen_users_X00_X99.json"

for i in range(0):
    i_path = src_path.replace("X", str(i))
    i_str = "{ \"users\" : [\n" + read_f(i_path)
    try:
        i_json = json.loads(new_str_i) # checks if new json is valid
        print("    new json valid")
        write_f(i_path, new_str_i)
        print("    written", i_path)
    except JSONDecodeError as jde:
        print("    json invalid", jde)
        inv_path = i_path.replace("99", "99_invalid").replace("gen", "inv_json/gen")
        write_f(inv_path, new_str_i)
        print("    written to", inv_path)

"""### general_users: remove_duplicates()"""

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

"""### validate_json()
loads in jsons and checks if valid. prints #users if valid
"""

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
        except JSONDecodeError as jde:
            print("    json invalid", jde)
        except Exception as e:
            print("    oops", e)
        #end try
        print()
    #end for


print(dt.now())
#validate_json(max_00=4, new=False, user_type="gen")


"""### rename_json()

"""

src_file = "pop_users/pop_users_X00_X99_new.json"
dst_file = "pop_users_X00_X99.json"

def rename_json():
    for i in range(39):
        print(i, ":")
        dst_path = folder_path + dst_file.replace("X", str(i))
        src_path = folder_path + src_file.replace("X", str(i))
        i_s = read_f(old_path)
        try:
            i_json = json.loads(i_s)
            print("    json loaded", end=" ")
            write_f(dst_path, i_s)
            s = ("(written to " + dst_path + ")")
            print(s)
        except Exception as e:
            print(" noped out because", e, "\n", traceback.format_exc(), "\n")
            continue
        #end try
    #end for
#end

"""### other"""

#write_f(user_films_csv_path, "")
print(user_films_csv_path)

"""
s = read_f(folder_path+"gen_users_5400_5499.json")
s = s[0] + "\"users\" :" + s[1:]
json.loads(s)
write_f(folder_path+"safety/gen_users_5400_5499.json", s)
"""

fp = folder_path+"safety/gen_users_X00_X99.json"
def append_user_films()
    for i in range(5,54):
        print(i, end=" : ")
        fi = fp.replace("X", str(i))
        all = json.loads(read_f(fi))
        print("loaded", end=", ")
        for u in all["users"] :
            s = "\"" + u["lid"] + "\""
            for lid in u["ratings_by_film"]:
                s = s+","+lid
            append_f(user_films_csv_path, (s+"\n"))
        print("all users appended")
#end
