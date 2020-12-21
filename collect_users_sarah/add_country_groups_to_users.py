# file created 13 Dec 2020 sastaffo@tcd.ie

from google.colab import drive
drive.mount('/content/drive')

"""## imports / set up methods"""

import json
from json import JSONDecodeError
from datetime import datetime as dt
import traceback
print(dt.now())

"""# basic read/write methods"""

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

"""# global vars"""

folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/"
user_file_path = folder_path + "country_groups_added/TYPE_users_X00_X99.json"
dst_path_all = folder_path + "writing/user_film_pairs.json"

missed_path = folder_path + "missing_countries.csv"

print(dt.now())

all_films_path = folder_path.replace("Sarah_data", "Philip's Data") + "all_film_dataV3.json"
all_films_str = read_f(all_films_path)
all_films_dict = json.loads(all_films_str)

cont_path = folder_path.replace("Sarah_data", "Shaun's Data") + "countries_by_continent.json"
cont_str = read_f(cont_path)
country_groups = json.loads(cont_str)

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
            (new_c, group) = find_continent(c)
            if group is None:
                print("X:", new_c)
#end
print(dt.now())

"""# Get User Country Groups"""

"""### by file"""

def write_groups_by_file(all_json, dstpath):
    users_in_file = len(all_json["users"])
    not_added = users_in_file ## decrease by 1 when
    for i in range(users_in_file):
        u = all_json["users"][i]
        #print(i, end=": ")
        try:
            t = u["country_group"]
            not_added = not_added-1
            continue ## next loop
        except KeyError:
            pass
        if u["country"] is None:
            all_json["users"][i]["country_group"] = None
            not_added = not_added-1
            #print("country None")
        else:
            uc = (u["country"]).lower()
            (c, gr) = find_group(uc)
            if c is not None:
                all_json["users"][i]["country"] = c
                all_json["users"][i]["country_group"] = gr
                not_added = not_added-1
                #print("group added", uc, "->", gr)
            else:
                append_f(missed_path, (uc+"\n"))
        #end if
    #end for
    if not_added > 0:
        append_f(file_with_missing, (dstpath+"\n"))
        print("added to csv for", not_added, "missing users")
    else: print("all countries accounted for!")
    write_f(dstpath, json.dumps(all_json))
    print("    written")
    return
#end

def test():
    print(dt.now())
    p = folder_path+"user_files/gen_users_000_099.json"
    t = load_json(p)
    try:
        print("couldn't get json:", t["failure"])
        return
    except:
        pass
    add_groups_by_file(t, p.replace("user_files", "country_groups_added"))

#test()
print(dt.now())

"""### run ALL"""

check_path = folder_path + "user_files/TYPE_users_X00_X99.json"
def add_country_groups_all():
    # 0 - 57 gen
    # 0 - 38 pop
    for ut in ["pop", "gen"]:
        print(ut, dt.now())
        utpath = check_path.replace("TYPE", ut)
        ra = 39
        if ut == "gen": ra = 58

        for i in range(ra):
            ipath = utpath.replace("X", str(i))
            s = read_f(ipath)
            if s is None:
                print("can't find",ut,"users", i)
                continue
            else:
                try:
                    i_all = json.loads(s)
                    ipath = ipath.replace("user_files", "country_groups_added")
                    print(ut, i, end=": ")
                    write_groups_by_file(i_all, ipath)
                except JSONDecodeError as jde:
                    print("got error for pop", path, ":", jde)
                    print(traceback.format_exc())
        #end for
        print("done with", ut)
    #end for
add_country_groups_all()

"""### run from CSV"""

def add_country_groups_csv():
    l_str = read_f(folder_path + "country_groups_added/file_with_missing_groups.csv")
    l = l_str.split("\n")
    write_f((folder_path + "country_groups_added/file_with_missing_groups.csv"), "")
    for path in l:
        s = read_f(path)
        if s is None:
            print("can't find users", path)
            continue
        else:
            try:
                i_all = json.loads(s)
                print(path, ": ")
                write_groups_by_file(i_all, path)
            except JSONDecodeError as jde:
                print("got error for", path, ":", jde)
                print(traceback.format_exc())
        #end for
    #end for
    print("done")
#add_country_groups_csv()
