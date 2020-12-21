# file created 5 Dec 2020 sastaffo@tcd.ie

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

## fix names inside files
def apply_elliot_fixes():
    csv_path = folder_path + "elliot_fixes_to_do.csv"
    file_paths = read_f(csv_path).split("\n")
    for path in file_paths:
        read_in = read_f(path)
        if read_in is None: continue

        print("file:", path.split("/")[-1])
        yes = read_in.count("elliot-page")
        no = read_in.count("ellen-page")
        print("  yes=", yes)
        print("  no =", no)
        users_dict = json.loads(read_in)
        for i in range(len(users_dict["users"])):
            u = users_dict["users"][i]
            ellen_avg = {}
            elliot_avg = {}
            u_s = json.dumps(u)
            yes = u_s.count("elliot-page")
            no = u_s.count("ellen-page")
            if (no == 0): ## DN is not present
                continue
            else:
                pad = ""
                if i<10: pad = "  "
                print(" ",i, pad, "yes=", yes," no =", no, end=" ")
                ellen_avg = u["average_rating_by_actor"]["ellen-page"]
                if (yes == 0): ## DN is present, elliot is not
                    u["average_rating_by_actor"]["elliot-page"] = ellen_avg # creates elliot
                    u["average_rating_by_actor"].pop("ellen-page") # deletes ellen
                    print("    replacing")
                else: ## both names are present, *merge*
                    print("    merging")
                    elliot_avg = u["average_rating_by_actor"]["elliot-page"]
                    tmplist = elliot_avg["film-lids"]
                    for lid in ellen_avg["film-lids"]:
                        tmplist.append(lid)
                    # all films added to lids
                    sum = 0
                    count = len(tmplist)
                    for lid in tmplist:
                        sum = sum + u["ratings_by_film"][lid]
                    # sum of all new_page film ratings
                    avg = sum/count
                    new_page = {
                        "avg" : (avg),
                        "count" : count,
                        "avg_minus_tot_avg" : (avg-u["average_rating"]),
                        "film-lids" : tmplist
                    }
                    # filled new dict
                    u["average_rating_by_actor"]["elliot-page"] = new_page # replaces 'elliot-page'
                    u["average_rating_by_actor"].pop("ellen-page") # deletes ellen
                #end if yes
            #end if no
            users_dict["users"][i] = u # updates user in dict
        #end for users
        write_elliot(path.replace("safety", "elliot"), users_dict)
    #end for paths
    print("DONE")
    return
#end

def write_elliot(path, out_dict):
    write_f(path, "{ \"users\" : [\n")
    first = True
    for u in out_dict["users"]:
        user_js = (json.dumps(u)) ## no formatting
        user_js = user_js[0] + "\n" + user_js[1:] ## a little formatting, as a treat
        if first: first = False
        else: user_js = (",\n") + user_js
        append_f(path, user_js)
    #end for
    append_f(path, "\n] }")
    print("  written")

    check = read_f(path)
    yes = check.count("elliot-page")
    no = check.count("ellen-page")
    print("  new yes=", yes)
    print("  new no =", no)
    return

#apply_elliot_fixes()

elliot_fixes = folder_path + "elliot_fixes_to_do.csv"
## replace all instances of "ellen-page" with "elliot-page" in ALL files where only DN occurs
## writes others to csv

def film_dict_replace_elliot_page():
    fi_path = film_info_path.replace("data", "data/elliot").replace(".json", "_old.json")
    fi_old = read_f(film_info_path)
    fi_new = fi_old.replace("ellen-page", "elliot-page")
    print("film info string replaced")
    write_f(fi_path, fi_old)
    write_f(film_info_path, fi_new)
    print("film info written\n")
    return;

def file_replace_elliot_page(ulist, user_type="pop"):
    uj_path = (folder_path + "safety/TYPE_users_X00_X99.json").replace("TYPE", user_type)
    u_start = dt.now()
    print(user_type, ":", u_start)
    for i in ulist:
        i_path = uj_path.replace("X", str(i))
        i_s = read_f(i_path)
        if i_s is None: continue

        pad = ""
        if i<10: pad = "  "
        print(i_path.split("/")[-1], pad, ". read", end=" . ")
        yes = i_s.count("elliot-page")
        no = i_s.count("ellen-page")
        print("yes=", yes, ". no =", no, end=" . ")
        if (no) == 0:
            # if file contains neither, no action needed
            # if file contains 'elliot-page' but not 'ellen-page', no action needed
            print("skip")
            continue
        else:
            if (yes) == 0:
                # if file contains 'ellen-page' but not 'elliot-page', straight replace
                i_s = i_s.replace("ellen-page", "elliot-page")
                print("replaced", end=" . ")
                write_f(i_path, i_s)
                print("written")
                u_prev = dt.now()
            else:
                # if file contains both: add to csv to deal with later
                s = i_path + "\n"
                append_f(elliot_fixes, s)
                print("added to csv")
                u_prev = dt.now()
            #end if
        #end if
    #end for
    print("all", user_type, "parsed in", (dt.now()-u_start))
    return
#end

gen_file = "safety/TYPE_users_X00_X99.json"
def elliot_checkfix_all_files():
    write_f(elliot_fixes, "")
    print("clearing csv\n")

    ns = []
    for n in range(39):
        ns.append(n)
    file_replace_elliot_page(ns, user_type="pop")
    print()

    for n in range(39,58):
        ns.append(n)
    file_replace_elliot_page(ns, user_type="gen")
    print()

    apply_elliot_fixes()
    return
#end
