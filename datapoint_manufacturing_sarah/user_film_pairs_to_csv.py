# file created 20 Dec 2020 sastaffo@tcd.ie

from google.colab import drive
drive.mount('/content/drive')
from datetime import datetime as dt
print(dt.now())

"""# set up

## IMPORTS
"""

from bs4 import BeautifulSoup as BSoup
import requests
import random
import traceback
import copy
import json
import csv
!pip install ujson
import ujson
from json import JSONDecodeError
import pandas as pd


print(dt.now())

"""## basic read/write methods"""

def read_f(path):
    try:
        f = open(path, "r")
        s = f.read()
        f.close()
        return s
    except FileNotFoundError:
        #print("file not found")
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
merge_folder_path = folder_path + "valid_user_film_merge/"

pairs_json_path = merge_folder_path + "TYPE_X00_X99_film_pairs.json"
pairs_csv_path = folder_path + "user_film_pairs_csv/training_pairs_SIZE.csv"

films_path = folder_path.replace("Sarah_data", "Philip's Data") + "all_film_dataV3.json"
films_dict = ujson.loads(read_f(films_path))

csv_header_str = read_f(folder_path+"header.csv")
csv_header = csv_header_str.split(",")

genre_names = ["action", "adventure", "animation", "comedy", "crime", "documentary", "drama", "family", "fantasy", "history", "horror", "music", "mystery", "romance", "science fiction", "thriller", "tv movie", "war", "western"]
one_hot_decades = ["1880s", "1890s", "1900s", "1910s", "1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
one_hot_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "None"]
one_hot_continents = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America", "South America (Portuguese)"]

print(dt.now())

def list_to_csv_str(lst):
    for i in range(len(lst)):
        lst[i] = str(lst[i])
    lst_str = (",".join(lst)) + "\n"
    return lst_str

"""# JSON to CSV

## methods
"""

def pair_to_csv_str(pj):
    if pj["user_rating_for_film"] is None:
        return ""

    if pj["user_from_prod_country"]: user_from_prod_country = 1
    else: user_from_prod_country = 0

    if pj["user_from_prod_continent"]: user_from_prod_continent = 1
    else: user_from_prod_continent = 0

    if pj["film_franchise"]: franchise = 1
    else: franchise = 0


    pcsv = [pj["user_rating_for_film"], pj["user_films_watched"], pj["user_average_rating"], pj["film_avg_rating"], pj["film_total_views"], pj["film_total_ratings"], pj["film_rate_ratio"],
            pj["film_total_likes"], pj["film_like_ratio"], pj["film_runtime_min"], pj["film_release_year"], pj["film_age"], franchise, user_from_prod_country,
            user_from_prod_continent, pj["user_director_avg"], pj["user_director_avg_minus"], pj["user_director_count"]
    ]
    # add actors
    for key in ["user_actors_avg", "user_actors_avg_minus", "user_actors_count"]:
        for i in range(5):
            try: a = pj[key][i]
            except: a = {("actor"+str(i)): -1}
            act_key = list(a)[0]
            act_val = a[act_key]
            pcsv.append(act_val)

    # add one-hot
    #genres
    for key_suff in ["_avg", "_avg_minus", "_count"]:
        g_dict = {}
        key = "user_genres"+key_suff
        for g in pj[key]:
            gen_key = list(g)[0]
            gen_val = g[gen_key]
            g_dict[gen_key] = gen_val
        for genre in genre_names:
            g = g_dict.get(genre, -1)
            pcsv.append(g)

    # decade
    for dec in one_hot_decades:
        d = 0
        if dec == pj["film_release_decade"]: d = 1
        pcsv.append(d)

    # months
    pj_mon = pj["film_release_month"]
    if pj_mon is None: pj_mon = "None"
    for mon in one_hot_months:
        m = 0
        if mon == pj_mon: m = 1
        pcsv.append(m)

    # film_continent
    for con in one_hot_continents:
        c = 0
        if con in pj["film_prod_continents"]: c = 1
        pcsv.append(c)

    pcsv_str = list_to_csv_str(pcsv)
    pcsv_str = pcsv_str.replace("None", "-1")
    return pcsv_str

def test_write_pair_to_csv():
    all_pairs = json.loads(read_f(merge_folder_path+"pop_3700_3799_film_pairs.json"))
    test_pair = all_pairs[0]
    print(test_pair["user_lid"], test_pair["user_films_watched"])
    start = dt.now()
    write_pair_to_csv(test_pair)
    print(dt.now() - start)
    return
#end
#test_write_pair_to_csv()

def file_to_csv(src_path, dst_path):
    jstr = read_f(src_path)
    if jstr is None: return
    pairs = json.loads(jstr)
    print("loaded", end=" ")
    #"valid_user_film_merge/TYPE_X00_X99_film_pairs.json"
    write_f(dst_path, csv_header_str)
    all_str = ""
    for p in pairs:
        all_str = all_str + pair_to_csv_str(p)
    append_f(dst_path, all_str)
    print(len(pairs))
    return

"""## run"""

csv_header_str = read_f(folder_path+"header.csv")
csv_header = csv_header_str.split(",")

test_src_path = folder_path + "test_valid_user_film_merge/test_TYPE_users_X00_X99.json"
test_dst_path = folder_path + "test_user_film_pairs_csv/test_TYPE_X00_X99_pairs.csv"
def some_test_pairs_to_csv(max, min=0, ut="pop"):
    start = dt.now()
    print(start)
    for i in range(min, max+1):
        print(i, end=" ")
        i_path = test_src_path.replace("TYPE", ut).replace("X", str(i))
        i_dst_path = test_dst_path.replace("TYPE", ut).replace("X", str(i))
        file_to_csv(i_path)
    #end for
    print("done with", ut, min, "-", max, "in:", (dt.now()-start))
    #end
#end

#some_test_pairs_to_csv(max=19, min=0, ut="pop")
#some_test_pairs_to_csv(max=23, min=20, ut="pop")
#some_test_pairs_to_csv(max=13, min=0, ut="gen")

csv_header_str = read_f(folder_path+"header.csv")
csv_header = csv_header_str.split(",")

def some_pairs_to_csv(max, min=0, ut="pop"):
    start = dt.now()
    print(start)
    for i in range(min, max+1):
        print(i, end=" ")
        i_path = pairs_json_path.replace("TYPE", ut).replace("X", str(i))
        i_dst_path = i_path.replace("valid_user_film_merge", "user_film_pairs_csv").replace("json", "csv")
        file_to_csv(i_path, i_dst_path)
    #end for
    print("done with", ut, min, "-", max, "in:", (dt.now()-start))
    #end
#end

#some_pairs_to_csv(max=38, min=0, ut="pop")
#some_pairs_to_csv(max=27, min=25, ut="pop")
#some_pairs_to_csv(max=57, min=55, ut="gen")

def all_pairs_to_csv():
    for i in range(60):
        start = dt.now()
        print(start, i)
        dones = "done: "
        pi_path = pairs_json_path.replace("TYPE", "pop").replace("X", str(i))
        pi_str = read_f(pi_path)
        if pi_str is not None:
            print("    pop :", end=" ")
            file_to_csv(pi_path)
        gi_path = pi_path.replace("pop", "gen")
        gi_str = read_f(gi_path)
        if gi_str is not None:
            print("    gen :", end=" ")
            file_to_csv(gi_path)
        print("    done", (dt.now()-start), "\n")
    print("done")
    return

#p = folder_path + "inv_json/test_gen_users_000_099.json"
#s = read_f(p)
#j = json.loads(s)

"""# merge_csvs"""

def merging(a_path, b_path, c_path, d_path):
    try: a = pd.read_csv(a_path, header=0, index_col=False)
    except: a = pd.read_csv((folder_path+"header.csv"), header=0, index_col=False)
    (la, _) = a.shape
    try: b = pd.read_csv(b_path, header=0, index_col=False)
    except: b = pd.read_csv((folder_path+"header.csv"), header=0, index_col=False)
    (lb, _) = b.shape
    try: c = pd.read_csv(pop_i1_path, header=0, index_col=False)
    except: c = pd.read_csv((folder_path+"header.csv"), header=0, index_col=False)
    (lc, _) = c.shape
    try: d = pd.read_csv(d_path, header=0, index_col=False)
    except: d = pd.read_csv((folder_path+"header.csv"), header=0, index_col=False)
    (ld, _) = d.shape
    sum = la + lb + lc + ld

    list_to_merge = [a, b, c, d]
    merged_pd = pd.concat(list_to_merge, axis=0, join='outer', ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False, copy=True)
    (lm, _) = merged_pd.shape
    if sum != lm:
        print("didn't concat correctly: sum=", sum, "  concat length=", lm)
        return None
    else: print("concatted", end=" ")
    return merged_pd

csv_header_str = read_f(folder_path+"header.csv")
csv_header = csv_header_str.split(",")

def test_merge_csvs():
    src_generic = folder_path + "test_user_film_pairs_csv/test_TYPE_X00_X99_pairs.csv"
    dst_generic = folder_path + "test_merged_csv_pairs/test_pairs_ZZ.csv"
    j = 0
    for i in range(0,13,2):
        # get: pop(i), gen(i), pop(i+1), gen(i+1)
        print(j, i, end=" ")
        a_path = src_generic.replace("TYPE", "pop").replace("X", str(i))
        b_path = src_generic.replace("TYPE", "gen").replace("X", str(i))
        c_path = src_generic.replace("TYPE", "pop").replace("X", str(i+1))
        d_path = src_generic.replace("TYPE", "gen").replace("X", str(i+1))

        merged_pd = merging(a_path, b_path, c_path, d_path)
        i_dst = dst_generic.replace("ZZ", str(j))
        if merged_pd is not None:
            merged_pd.to_csv(i_dst, mode="w+", line_terminator="\n", index=False, header=True)
            print("written")
        j = j+1
    #end for
    print("finished pop-gen")
    for i in range(14, 23, 4):
        print(j, i, end=" ")
        a_path = src_generic.replace("TYPE", "pop").replace("X", str(i))
        b_path = src_generic.replace("TYPE", "pop").replace("X", str(i+1))
        c_path = src_generic.replace("TYPE", "pop").replace("X", str(i+2))
        d_path = src_generic.replace("TYPE", "pop").replace("X", str(i+3))

        merged_pd = merging(a_path, b_path, c_path, d_path)
        i_dst = dst_generic.replace("ZZ", str(j))
        if merged_pd is not None:
            merged_pd.to_csv(i_dst, mode="w+", line_terminator="\n", index=False, header=True)
            print("written")
        j = j+1
    print("finished gen")
    return

#test_merge_csvs()

csv_header_str = read_f(folder_path+"header.csv")
csv_header = csv_header_str.split(",")

def merge_csvs():
    src_generic = folder_path + "user_film_pairs_csv/TYPE_X00_X99_film_pairs.csv"
    dst_generic = folder_path + "merged_csv_pairs/pairs_ZZ.csv"
    j = 0
    for i in range(0,39,2):
        # get: pop(i), gen(i), pop(i+1), gen(i+1)
        print(j, i, end=" ")
        a_path = src_generic.replace("TYPE", "pop").replace("X", str(i))
        b_path = src_generic.replace("TYPE", "gen").replace("X", str(i))
        c_path = src_generic.replace("TYPE", "pop").replace("X", str(i+1))
        d_path = src_generic.replace("TYPE", "gen").replace("X", str(i+1))

        merged_pd = merging(a_path, b_path, c_path, d_path)
        i_dst = dst_generic.replace("ZZ", str(j))
        if merged_pd is not None:
            merged_pd.to_csv(i_dst, mode="w+", line_terminator="\n", index=False, header=True)
            print("written")
        j = j+1
    #end for
    print("finished pop-gen")
    for i in range(40, 58, 4):
        print(j, i, end=" ")
        a_path = src_generic.replace("TYPE", "gen").replace("X", str(i))
        b_path = src_generic.replace("TYPE", "gen").replace("X", str(i+1))
        c_path = src_generic.replace("TYPE", "gen").replace("X", str(i+2))
        d_path = src_generic.replace("TYPE", "gen").replace("X", str(i+3))

        merged_pd = merging(a_path, b_path, c_path, d_path)
        i_dst = dst_generic.replace("ZZ", str(j))
        if merged_pd is not None:
            merged_pd.to_csv(i_dst, mode="w+", line_terminator="\n", index=False, header=True)
            print("written")
        j = j+1
    print("finished gen")
    return

#merge_csvs()

"""# fixing jsons

### counties-countries
"""

def fix_countries():
    for i in range(60):
        dones = "done: "
        pi_path = pairs_json_path.replace("TYPE", "pop").replace("X", str(i))
        pi_str = read_f(pi_path)
        if pi_str is not None:
            dones = dones + "pop "
            pi_str = pi_str.replace("counties", "countries")
            write_f(pi_path, pi_str)
        gi_path = pi_path.replace("pop", "gen")
        gi_str = read_f(gi_path)
        if gi_str is not None:
            dones = dones + "gen "
            gi_str = gi_str.replace("counties", "countries")
            write_f(gi_path, gi_str)
        print(dones, i)
    print("done")
    return

#fix_countries()
print(dt.now())

"""### fix_decades"""

def fix_decades(pair_path):
    start = dt.now()
    print( start, ">", (pair_path.split("/")[-1]) )
    pairs = ujson.loads(read_f(pair_path))
    for p in pairs:
        new_dec = p["film_release_year"] // 10
        p["film_release_decade"] = (str(new_dec) + "0s")
    write_f(pair_path, json.dumps(pairs))
    print( "    written @ ", str(dt.now()-start) )
    return

def fix_all_decades():
    for i in range(60):
        dones = "done: "
        pi_path = pairs_json_path.replace("TYPE", "pop").replace("X", str(i))
        pi_str = read_f(pi_path)
        if pi_str is not None:
            dones = dones + "pop "
            fix_decades(pi_path)
        gi_path = pi_path.replace("pop", "gen")
        gi_str = read_f(gi_path)
        if gi_str is not None:
            dones = dones + "gen "
            fix_decades(gi_path)
        print(dones, i, "\n")
    print("done")
    return

#fix_all_decades()
print(dt.now())

"""# make header"""

def make_header():
    header = ["output", "user_film_watched", "user_avg_rating", "film_avg_rating", "film_total_views", "film_total_ratings", "film_rate_ratio", "film_total_likes", "film_like_ratio",
              "film_runtime_min", "film_release_year", "film_age", "film_franchise", "user_from_prod_country", "user_from_prod_continent", "director_avg", "director_avg_minus",
              "director_count"]

    actors_avg = []
    actors_minus = []
    actors_count = []
    for i in range(5):
        actors_avg.append(("actor"+str(i)+"_avg"))
        actors_minus.append(("actor"+str(i)+"_avg_minus"))
        actors_count.append(("actor"+str(i)+"_count"))

    header.extend(actors_avg)
    header.extend(actors_minus)
    header.extend(actors_count)

    one_hot_genres_avg = ["action_avg", "adventure_avg", "animation_avg", "comedy_avg", "crime_avg", "documentary_avg", "drama_avg", "family_avg", "fantasy_avg",
                        "history_avg", "horror_avg", "music_avg", "mystery_avg", "romance_avg", "science fiction_avg", "thriller_avg", "tv movie_avg", "war_avg", "western_avg"]
    one_hot_genres_avg_min = ["action_avg_minus", "adventure_avg_minus", "animation_avg_minus", "comedy_avg_minus", "crime_avg_minus", "documentary_avg_minus", "drama_avg_minus",
                            "family_avg_minus", "fantasy_avg_minus", "history_avg_minus", "horror_avg_minus", "music_avg_minus", "mystery_avg_minus", "romance_avg_minus",
                            "science fiction_avg_minus", "thriller_avg_minus", "tv movie_avg_minus", "war_avg_minus", "western_avg_minus"]
    one_hot_genres_count = ["action_count", "adventure_count", "animation_count", "comedy_count", "crime_count", "documentary_count", "drama_count", "family_count", "fantasy_count",
                            "history_count", "horror_count", "music_count", "mystery_count", "romance_count", "science fiction_count", "thriller_count", "tv movie_count", "war_count",
                            "western_count"]
    one_hot_decades = ["1880s", "1890s", "1900s", "1910s", "1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
    one_hot_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "None"]
    one_hot_continents = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America", "South America (Portuguese)"]

    header.extend(one_hot_genres_avg)
    header.extend(one_hot_genres_avg_min)
    header.extend(one_hot_genres_count)
    header.extend(one_hot_decades)
    header.extend(one_hot_months)
    header.extend(one_hot_continents)

    h_str = list_to_csv_str(header)

    write_f((folder_path+"header.csv"), h_str)
    print("written")
    return
#end

make_header()
print(dt.now())

"""## get types for 1 hot encoding"""

def write_film_meta(meta_path):
    films_md = ujson.loads(read_f(meta_path))
    """
    "genres": {},
    "decades": {},
    "months": {},
    "prod_companies": {},
    "prod_countries": {},
    "prod_continents": {},
    """
    gen = sorted(list(films_md["genres"]))
    dec = sorted(list(films_md["decades"]))
    mon = sorted(list(films_md["months"]))
    prod_cont = sorted(list(films_md["prod_continents"]))
    add_indie(films_md)
    prod_comp = sorted(list(films_md["prod_companies_w_indie"]))
    film_meta_lists = {
        "genres" : gen,
        "decades" : dec,
        "months" : mon,
        "prod_continents" : prod_cont,
        "one_hot_genres_avg" : [],
        "one_hot_genres_avg_min" : [],
        "one_hot_genres_count" : [],
    }
    for g in gen:
        film_meta_lists["one_hot_genres_avg"].append((g+"_avg"))
        film_meta_lists["one_hot_genres_avg_min"].append((g+"_avg_minus"))
        film_meta_lists["one_hot_genres_count"].append((g+"_count"))
    write_f(meta_path.replace(".json", "_lists.json"), json.dumps(film_meta_lists))

#write_film_meta(films_seen_path)
print(dt.now())

films_seen_path = (folder_path+"films_seen.json")
films_seen = ujson.loads(read_f(films_seen_path))

#films_seen["languages"] = {}

def get_1hot_values(src_str):
    src_pairs = ujson.loads(src_str)
    for p in src_pairs:
        if p["film_lid"] not in films_seen["lids"]:
            films_seen["lids"].append(p["film_lid"])
            dec = p["film_release_decade"]
            increment("decades", dec)
            mon = p["film_release_month"]
            increment("months", mon)
            for gen in p["user_genres_count"]:
                g = list(gen)[0]
                increment("genres", g)
            for com in p["film_prod_companies"]:
                increment("prod_companies", com)
            for cou in p["film_prod_countries"]:
                increment("prod_countries", cou)
            for con in p["film_prod_continents"]:
                increment("prod_continents", con)

def increment(field, key):
    try: count = films_seen[field][key]
    except KeyError: count = 0
    films_seen[field][key] = count + 1
    return

def check_all_films_seen():
    missing_count = 0
    for f_lid in films_dict:
        if f_lid not in films_seen["lids"]:
            missing_count = missing_count +1
            #print(missing_count, f_lid)
    print("    checked all films ( missed", missing_count, "of", len(films_dict) ,")")
    return missing_count

def add_to_films_seen():
    for i in range(60):
        dones = "done: "
        pi_path = pairs_json_path.replace("TYPE", "pop").replace("X", str(i))
        pi_str = read_f(pi_path)
        if pi_str is not None:
            dones = dones + "pop "
            get_1hot_values(pi_str)
        gi_path = pi_path.replace("pop", "gen")
        gi_str = read_f(gi_path)
        if gi_str is not None:
            dones = dones + "gen "
            get_1hot_values(gi_str)
        print(dones, i)
        if pi_str is None and gi_str is None:
            continue
        try:
            write_f(films_seen_path, json.dumps(films_seen))
        except Exception as e:
            print("write failed:", e)
        missing = check_all_films_seen()
        if missing == 0:
            print("seen all")
            write_f(films_seen_path.replace(".json", "_final.json"), json.dumps(films_seen, indent=2))
    return

#add_to_films_seen()

def add_indie(films):
    films["prod_companies_w_indie"] = { "Indie" : 0 }
    films["indies"] = []
    pci = films["prod_companies_w_indie"]

    pc = films["prod_companies"]
    for comp in pc:
        count = pc[comp]
        if count > 5:
            pci[comp] = count
        else:
            pci["Indie"] = pci["Indie"] + count
            films["indies"] = comp
    return

def check_prod_company_count():
    prod_comp_count = {}
    for f_lid in films_dict:
        companies = films_dict[f_lid]["production_companies"]
        for comp in companies:
            if comp in prod_comp_count:
                prod_comp_count[comp] = (prod_comp_count[comp] + 1)
            else:
                prod_comp_count[comp] = 1
    #end

    prod_count_count = {}
    for comp in prod_comp_count:
        c_count = prod_comp_count[comp]
        c_str = str(c_count)
        if c_str in prod_count_count:
            prod_count_count[c_str] = (prod_count_count[c_str] + 1)
        else:
            prod_count_count[c_str] = 1
    #end

    dst = folder_path + "prod_companies_by_count.json"
    pcc_str = json.dumps(prod_count_count, indent=2)
    write_f(dst, pcc_str)
    return

#check_prod_company_count()
print(dt.now())
