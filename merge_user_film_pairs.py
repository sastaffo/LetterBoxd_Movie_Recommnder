# file created 14 Dec 2020 sastaffo@tcd.ie

from google.colab import drive
drive.mount('/content/drive')

"""# set up"""

"""## imports"""

import json
from json import JSONDecodeError
from datetime import datetime as dt
import traceback
import copy
!pip install ujson
import ujson
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

"""## global vars"""

folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/"
#user_file_path = folder_path + "country_groups_added/TYPE_users_X00_X99.json"
dst_path_all = folder_path + "writing/user_film_pairs.json"

missed_path = folder_path + "missing_countries.csv"

print(dt.now())

all_films_path = folder_path.replace("Sarah_data", "Philip's Data") + "test_all_film_data.json"
all_films_str = read_f(all_films_path)
all_films_dict = json.loads(all_films_str)
print("got all films")

cont_path = folder_path.replace("Sarah_data", "Shaun's Data") + "countries_by_continent.json"
cont_str = read_f(cont_path)
continents = json.loads(cont_str)
print("got country groups")

c_map_path = folder_path + "country_mappings.json"
c_map_str = read_f(c_map_path)
country_map = json.loads(c_map_str)
print("got country map")

print(dt.now())

"""## Country Groups"""

"""#### find_continent()"""

def find_continent(c, film_lid):
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
    s = (cnty_str + "," + film_lid + "\n")
    append_f(missed_path, s)
    return (cnty_str, None)
#end
print(dt.now())

"""#### get countries for all films"""

def get_film_countries():
    for film_lid in all_films_dict:
        film_info = all_films_dict[film_lid]
        for c in film_info["production_countries"]:
            (new_c, group) = find_continent(c, film_lid)
            if group is None:
                print("X:", new_c)
    print("checked all")
#end
print(dt.now())
#get_film_countries()

"""# User-Film Merging"""

"""## get one user-film pair and return json"""

"""### get_user_film_pair"""

def get_user_film_pair(user_json, film_json, dst_path):
    # numbers
    views = film_json["number_of_views"]
    rates = film_json["number_of_ratings"]
    likes = film_json["number_of_likes"]

    # production countries/continents (writes them in same format as user country for comparisons)
    prod_countries = []
    prod_continents = []
    for c in film_json["production_countries"]:
        (low_c, continent) = find_continent(c, film_json["lid"])
        prod_countries.append(low_c)
        if continent is None:
            print("no continent for", low_c)
            if low_c is not None:
                append_f(missed_path, (low_c+"\n")) ## add to missing countries to be added to the map
                append_f(file_with_missing, (dst_path))
        else: prod_continents.append(continent)
    #end for
    prod_continents = (list(dict.fromkeys(prod_continents))) # remove duplicate continents



    # user average ratings for director/genres/actors
    direc_avg = try_json(user_json, film_json, "director")
    director_avg = direc_avg[0] # straight average
    director_avg_minus = direc_avg[1] # average minus user total average
    director_count = direc_avg[2] # number of ratings
    genres = []
    genres_minus = []
    genres_count = []
    for i in range(len(film_json["genres"])):
        key = film_json["genres"][i]
        genre_avg = try_json(user_json, film_json, "genre", index=i)
        if genre_avg is not None:
            genres.append({key: genre_avg[0]}) # straight average
            genres_minus.append({key: genre_avg[1]}) # average minus user total average
            genres_count.append({key: genre_avg[2]}) # number of ratings
    actors = []
    actors_minus = []
    actors_count = []
    for i in range(len(film_json["actor"])):
        key = "actor"+str(i)
        act_avg = try_json(user_json, film_json, "actor", index=i)
        if act_avg is not None:
            actors.append({key: act_avg[0]}) # straight avg
            actors_minus.append({key: act_avg[1]}) # average minus user total average
            actors_count.append({key: act_avg[2]}) # number of ratings

    # user country/continent == film prod country/continent
    if user_json["country"] is not None:
        user_prod_continent = False # check for continent first, only check for country if continent is True
        user_prod_country = False
        if user_json["country_group"] is not None:
            for c in prod_continents:
                if c == user_json["country_group"]:
                    user_prod_continent = True
                    break
            #end for
            if user_prod_continent:

                for c in prod_countries:
                    if c == user_json["country"]:
                        user_prod_country = True
                        break
                #end for
            #end if
        #end if
    else:
        user_prod_continent = None
        user_prod_country = None

    u_avg = user_json["average_rating"]

    try: language = film_json["original_langauge"]
    except KeyError: language = None

    try: month = (film_json["release_date"]).split("-")[1] # date format = "YYYY-MM-DD"
    except: month = None

    year = film_json["release_year"]
    dec = (year // 10) # removes final digit
    decade = (str(dec) + "0s")

    try: usr_rating = user_json["this_film_rating"]
    except KeyError: usr_rating = None

    relevant = {
        # USER fields
        "user_lid" :             user_json["lid"],
        "user_rating_for_film" : usr_rating,
        "user_country" :         user_json["country"],
        "user_country_group" :   user_json["country_group"],
        "user_films_watched" :   len(user_json["ratings_by_film"]),
        "user_average_rating" :  user_json["average_rating"], ## since all of the other user-film averages are in relation to this, we might get an output which is +- the user's overall average rather than
        # FILM fields
        "film_lid" :             film_json["lid"],
        "film_avg_rating" :      film_json["avg_rating"],
        "film_total_views" :     views,
        "film_total_ratings" :   rates,
        "film_rate_ratio" :      (rates/views),
        "film_total_likes" :     likes,
        "film_like_ratio" :      (likes/views),
        "film_prod_companies":   film_json["production_companies"],
        "film_prod_countries" :  prod_countries,
        "film_prod_continents" : prod_continents,
        "film_release_year" :    year,
        "film_release_decade":   decade,
        "film_release_month" :   month,
        "film_age" :             film_json["movie_age"],
        "film_runtime_min" :     film_json["runtime"],
        "film_franchise" :       film_json["in_franchise"],
        "film_language" :        language,
        # USER-FILM fields
        "user_from_prod_country" :      user_prod_country,
        "user_from_prod_continent" :    user_prod_continent,
        "user_director_avg" :           director_avg,
        "user_director_avg_minus" :     director_avg_minus,
        "user_director_count" :         director_count,
        "user_genres_avg" :             genres, ## genres are lists of dicts for 1-hot-encoding = {genre_name : avg}
        "user_genres_avg_minus" :       genres_minus,
        "user_genres_count" :           genres_count,
        "user_actors_avg" :             actors,
        "user_actors_avg_minus" :       actors_minus,
        "user_actors_count" :           actors_count,
        "film_rating_minus_user_avg" :  (film_json["avg_rating"]-user_json["average_rating"]),
    }
    return relevant
#end


print(dt.now())

"""### try_json"""

d = "director"
a = "actor"
g = "genre"
u_pref = "average_rating_by_"

def try_json(user_json, film_json, field, index=0):
    if field == d:
        entry = film_json[d]
    elif field == a:
        entry = film_json[(a)][index]
    elif field == g:
        entry = film_json[(g+"s")][index]
    else: return None
    #print(entry, end=" : ")
    #end if
    try:
        u_x_avg = user_json[(u_pref+field)][entry]["avg"]
        u_x_avg_minus = user_json[(u_pref+field)][entry]["avg_minus_tot_avg"]
        u_x_count = user_json[(u_pref+field)][entry]["count"]
        #print("got")
        return (u_x_avg, u_x_avg_minus, u_x_count)
    except KeyError as ke:
        return (user_json["average_rating"], 0, 0) # hasn't seen a film of this genre before: return average
    except Exception as e:
        print("Something happened: ", e)
        print(traceback.format_exc())
        return None
    #end try
#end

print(dt.now())

"""### remove_film() => remove film A from user B's stats"""

def remove_film(user_json, film_json):
    film_lid = film_json["lid"]
    #new_user_json = copy.deepcopy(user_json) """BOTTLENECK"""
    if film_lid not in user_json["ratings_by_film"]:
        return user_json

    old_tot_count = len(user_json["ratings_by_film"])

    if old_tot_count < 2:
        new_user_json = {
            "lid": user_json["lid"],
            "country": user_json["country"],
            "country_group": user_json["country_group"],
            "average_rating": 0,
            "ratings_by_film": {},
            "average_rating_by_genre": {},
            "average_rating_by_director": {},
            "average_rating_by_actor": {}
        }
        return new_user_json

    new_user_json = ujson.loads(ujson.dumps(user_json))
    user_film_rating = new_user_json["ratings_by_film"].pop(film_lid)
    new_user_json["this_film_rating"] = user_film_rating

    new_tot_count = len(new_user_json["ratings_by_film"])
    # (avg*count - this_film_avg) / (count-1)

    old_user_avg = user_json["average_rating"]
    new_user_avg = ((old_user_avg*old_tot_count) - user_film_rating) / new_tot_count
    new_user_json["average_rating"] = new_user_avg

    dir_avg_key = "average_rating_by_director"
    film_dir = film_json["director"]
    new_dir = fix_x_json(user_json, dir_avg_key, film_dir, film_lid, user_film_rating, new_user_avg)
    if new_dir is None:
        try: new_user_json[dir_avg_key].pop(film_dir)
        except KeyError: pass
    else: new_user_json[dir_avg_key][film_dir] = new_dir

    gen_avg_key = "average_rating_by_genre"
    for g in film_json["genres"]:
        new_gen = fix_x_json(user_json, gen_avg_key, g, film_lid, user_film_rating, new_user_avg)
        if new_gen is None:
            try: new_user_json[gen_avg_key].pop(g)
            except KeyError: pass
        else: new_user_json[gen_avg_key][g] = new_gen
    #end

    act_avg_key = "average_rating_by_actor"
    for a in film_json["actor"]:
        new_act = fix_x_json(user_json, act_avg_key, a, film_lid, user_film_rating, new_user_avg)
        if new_act is None:
            try: new_user_json[act_avg_key].pop(a)
            except KeyError: pass
        else: new_user_json[act_avg_key][a] = new_act
    #end
    return new_user_json
#end
print(dt.now())

def fix_x_json(user_json, key, x, film_lid, user_film_rating, user_new_tot_avg):
    try: x_json = user_json[key][x]
    except KeyError: return None
    old_count = x_json["count"]
    if old_count == 1: return None

    new_x_lids = copy.copy(x_json["film-lids"])
    try:
        new_x_lids.remove(film_lid)
    except ValueError:
        return x_json
    new_count = len(new_x_lids)
    new_avg = ((x_json["avg"]*old_count) - user_film_rating) / new_count
    new_avg_minus = new_avg - user_new_tot_avg
    new_x = {
        "avg" : new_avg,
        "count" : new_count,
        "avg_minus_tot_avg" : new_avg_minus,
        "film-lids" : new_x_lids
    }
    return new_x

print(dt.now())

"""## get user-film pairs for 1 user (and write all to json)"""

def write_film_pairs_for_user(user_json, dstpath=dst_path_all, first_user=False):
    first_elem = False
    if first_user: first_elem = True ## first line in the file needs to not be preceeded by a comma
    user_pairs_str = ""
    for film_lid in user_json["ratings_by_film"]:
        if film_lid in all_films_dict:
            film_js = all_films_dict[film_lid]
            user_json_without_film = remove_film(user_json, film_js)
            uf_pair = get_user_film_pair(user_json_without_film, film_js, dst_path=dstpath)
            add_s = "\n" + json.dumps(uf_pair)
            if first_elem: first_elem = False
            else: add_s = "," + add_s
            user_pairs_str = user_pairs_str + add_s
        #end if
    #end for
    if not (len(user_pairs_str) == 0):
        append_f(dstpath, user_pairs_str)
    return

print(dt.now())

"""##### test"""

# user_file_path = folder_path + "country_groups_added/TYPE_users_X00_X99.json"
# dst_path = folder_path + "writing/user_film_pairs.json"

def test_film_pairs_for_pop_099():
    start = dt.now()
    print(start)
    b_path = dst_path.replace("user", "test_pop_099")
    f_str = read_f(user_file_path.replace("TYPE", "pop").replace("X", "0"))
    all = json.loads(f_str)
    write_f(b_path, "[")
    first_user = True
    i = 0
    for u in all["users"]:
        print(i)
        write_film_pairs_for_user(u, dstpath=b_path, first_user=first_user)
        if first_user: first_user= False
        i = i+1
    #end for
    append_f(b_path, "\n]")
    valid = valid_json(b_path)
    if valid: print("json valid")
    else: print("json not valid")
    end = dt.now()
    print("time:", (end-start))
    return
#end

print(dt.now())
#test_film_pairs_for_pop_099()

"""## get user-film pairs for file of 100 users"""

user_file_path_training = folder_path + "all_users_unzip/TYPE_users_X00_X99.json"
dst_path_training = folder_path + "writing_pairs/TYPE_X00_X99_film_pairs.json"

def user_film_pairs_for_file(index, ut="pop", user_file_path=user_file_path_training, dst_path=dst_path_training, valid_folder="valid_user_film_merge"):
    start = dt.now()
    print(ut, index, start)
    this_dstpath = dst_path.replace("TYPE", ut).replace("X", str(index))
    f_str = read_f(user_file_path.replace("TYPE", ut).replace("X", str(index)))
    all = json.loads(f_str)
    write_f(this_dstpath, "[")
    first_user = True
    i = 0
    for u in all["users"]:
        print("    ", dt.now(), "-", i)
        try:
            write_film_pairs_for_user(u, dstpath=this_dstpath, first_user=first_user)
        except Exception as e:
            # stops for any reason, write to invalid and return (I'll come back to these)
            print("\n\nstopped at user", i, u["lid"], ": written to inv_json")
            print(traceback.format_exc())
            write_f(this_dstpath.replace("writing_pairs", "inv_json"), read_f(this_dstpath))
            return
        if first_user: first_user= False
        i = i+1
    #end for
    append_f(this_dstpath, "\n]")
    print("\nfinished write")
    res_str = read_f(this_dstpath)
    try:
        res_js = json.loads(res_str)
        print("json valid!")
        write_f(this_dstpath.replace("writing_pairs", valid_folder), json.dumps(res_js))
    except JSONDecodeError:
        write_f(this_dstpath.replace("writing_pairs", "inv_json"), res_str)
        print("writing to inv_json folder")
        return
    except Exception as e:
        print("Something Happened", e)
        print(traceback.format_exc())


    end = dt.now()
    print("time:", (end-start))
    return
#end
print(dt.now())

"""# run
loops through all user files: loads f into a dict and gets all pairs
"""

p = folder_path + "inv_json/test_pop_users_1500_1599.json"
s = read_f(p)
j = json.loads(s)

def some_pairs(max, min=0, ut="pop"):
    start = dt.now()
    print(start)
    for i in range(min, max+1):
        user_film_pairs_for_file(index=i, ut=ut)
    #end for
    print("done with", ut, min, "-", max, "in:", (dt.now()-start))
    #end
#end

#some_pairs(max=5, min=5, ut="pop")
#some_pairs(max=57, min=25, ut="gen")

def some_test_pairs(max, min=0, ut="pop"):
    user_path_testing = folder_path + "safety/test_TYPE_users_X00_X99.json"
    dst_path_testing = folder_path + "writing_pairs/test_TYPE_users_X00_X99.json"
    valid_folder = "valid_test_user_film_merge"
    start = dt.now()
    print(start)
    for i in range(min, max+1):
        user_film_pairs_for_file(index=i, ut=ut, user_file_path=user_path_testing, dst_path=dst_path_testing, valid_folder=valid_folder)
    #end for
    print("done with", ut, min, "-", max, "in:", (dt.now()-start))
    #end
#end

#some_test_pairs(max=23, min=0, ut="pop")
#some_test_pairs(max=13, min=1, ut="gen")

#some_test_pairs(max=15, min=15, ut="pop")

"""#### find bottleneck"""

import cProfile
import pstats

p35_str = read_f(folder_path + "all_users_unzip/pop_users_3500_3599.json")
p35 = json.loads(p35_str)
test_user = p35["users"][0] # ghadius
test_u_path = folder_path + "bneck_test_ghadius_pairs_2_ujson.json"

def bottleneck_file():
    write_film_pairs_for_user(test_user, dstpath=test_u_path, first_user=True)

def bottleneck_test():
    profile = cProfile.Profile()
    profile.runcall(bottleneck_file)
    ps = pstats.Stats(profile)
    ps.print_stats()
    return

#bottleneck_test()
