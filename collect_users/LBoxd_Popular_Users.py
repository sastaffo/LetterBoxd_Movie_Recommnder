# file created 29 Nov 2020 sastaffo@tcd.ie

from google.colab import drive
drive.mount('/content/drive')

"""# IMPORTS"""

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

"""# Set Up Global Vars"""

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

print(dt.now())

folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/"
test_folder_path = folder_path + "test_dataset/"


d_sp = ""
for i in range(26):
    d_sp = d_sp + " "
#end

pop_link_members = "https://letterboxd.com/members/popular/this/TIME/"
csv_dst_path_generic = test_folder_path + "pop_users_TIME.csv"

pop_link_wk = pop_link_members.replace("TIME", "week")
dst_path_wk = csv_dst_path_generic.replace("TIME", "wk")

pop_link_mth = pop_link_members.replace("TIME", "month")
dst_path_mth = csv_dst_path_generic.replace("TIME", "mth")

pop_link_yr = pop_link_members.replace("TIME", "year")
dst_path_yr = csv_dst_path_generic.replace("TIME", "yr")


train_csv_path = folder_path + "TYPE_usernames.csv"


print(dt.now())

"""# LBoxd_populars
Scraping usernames from letterboxd most popular reviewers pages
"""

populars_url = "https://letterboxd.com/reviewers/popular/this/all-time/"
max_page = 128


class LBoxd_populars():
    def __init__(self, url=populars_url, pages=max_page, time_log=True):
        self.time_log = time_log
        if self.time_log:
            setup_time_start = dt.now()
            print(setup_time_start, " : START popular")

        self.base_url = url
        if isinstance(pages, int) and pages >= 1:
            self.pages = pages
        else:
            raise TypeError("pages must be an integer >= 1")

        self.page_bsoups = {} # dict {url : bsoup_obj}
        self._fill_page_bsoups()
        self._generate_users_lid_list()

        if self.time_log:
            end_time = dt.now()
            print(end_time, " : ", str(end_time - setup_time_start), " : END\n")
    #end __init__

    def _fill_page_bsoups(self):
        if self.time_log:
            s = (str(dt.now()) + " : pages (max:" + str(self.pages) + ")")
            print(s, end=": ")
        for i in range(self.pages):
            pg = i+1
            if pg is 1:
                url = self.base_url
            else:
                url = (self.base_url + "page/" + str(pg) + "/")
            page = requests.get(url, allow_redirects=True)
            bsoup = BSoup(page.content, 'html.parser')
            self.page_bsoups[url] = bsoup
            if self.time_log: print(i, end=", ")
        #end for
        if self.time_log:
            s = ("\n", dt.now(), " : finished souping")
            print(s)
        return
    #end fill_page_bsoups

    def _generate_users_lid_list(self):
        # scrapes all bsoups in self.page_bsoups for all user urls on each page
        lids = []
        pg = 1
        i = 1
        for bsoup in self.page_bsoups.values():
            if self.time_log:
                s = (str(dt.now())+" : parsing users on page "+str(pg))
                print(s, end=": ")
            pg = pg+1
            table = bsoup.find("table", {"class" : "person-table"})
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")

            for row in rows:
                h3 = row.find("h3", {"class" : "title-3"})
                user_link = h3.find('a', href=True)['href'] # '/lid/'
                user_lid = user_link.split("/")[1]
                lids.append(user_lid)
                if self.time_log: print(i, end=", ")
                i = i+1
            #end for
            print()
        #end for
        self.users_lid_list = lids
        return
    #end _generate_users_lid_list()

    def write_user_lids(self, path):
        file_s = ""
        for lid in self.users_lid_list:
            file_s = file_s + (lid + "\n")
        #end for
        write_f(path, file_s)
        return
    #end

    def print_all(self, random_users=0):
        print(self)
        print("url: ", self.base_url)
        print("pages: ", self.pages)
        print("#page_bsoups: ", len(self.page_bsoups))
        print("#LBoxd Users: ", len(self.users_lid_list))

        if random_users > 0:
            print("\nrandom user lids: ")
        for i in range(random_users):
            print("    ",random.choice(self.users_lid_list))
        #end for
        return
    #end print_all()

#end LBoxd_populars

print(dt.now())

"""# running"""

"""### general_users: remove_duplicates()"""

def rm_duplicates(to_merge_list, existing_users_csvs_list, merged_dst_path):
    combined_to_merge = []
    for tm_path in to_merge_list:
        tm = read_csv_1d(tm_path)
        combined_to_merge.extend(tm)
    print("total before deduplication:", len(combined_to_merge))
    combined_no_dup = (list(dict.fromkeys(combined_to_merge)))
    print("total after deduplication:", len(combined_no_dup))

    for ex_path in existing_users_csvs_list:
        ex = read_csv_1d(ex_path)
        for u in ex:
            try:
                combined_no_dup.remove(u)
            except ValueError:
                pass

    print("total after rm existing  :", len(combined_no_dup))
    write_csv_1d(merged_dst_path, combined_no_dup)
    print("written")
    return
#end


def merge_pop_members():
    mer_list = [dst_path_wk, dst_path_mth, dst_path_yr]
    exs_list = [train_csv_path.replace("TYPE", "gen"), train_csv_path.replace("TYPE", "pop")]
    merged_dst_path = csv_dst_path_generic.replace("TIME", "merged")
    rm_duplicates(mer_list, exs_list, merged_dst_path)
    return
#end

#merge_pop_members()

def rm_dup_test_gen():
    philip_path = (folder_path.replace("Sarah_data", "Philip's Data") + "test_users.json")
    philip_users = json.loads(read_f(philip_path))
    src_testgen_path = csv_dst_path_generic.replace("TIME", "raw").replace("pop", "gen")
    write_csv_1d(src_testgen_path, philip_users)
    mer_list = [src_testgen_path]
    exs_list = [train_csv_path.replace("TYPE", "gen"), train_csv_path.replace("TYPE", "pop"), csv_dst_path_generic.replace("TIME", "merged")]
    dst_testgen_path = src_testgen_path.replace("raw", "merged")
    rm_duplicates(mer_list, exs_list, dst_testgen_path)
    return

rm_dup_test_gen()

"""### gather pop users"""

pop_link_wk = "https://letterboxd.com/members/popular/this/week/"
dst_path_wk = test_folder_path + "pop_users_wk.csv"

pop_link_mth = "https://letterboxd.com/members/popular/this/month/"
dst_path_mth = test_folder_path + "pop_users_mth.csv"
def CSV_write_all_popular_usernames(dst_path, link=None):
    if link is None:
        pop = LBoxd_populars()
    else:
        pop = LBoxd_populars(url=link)
    pop.write_user_lids(dst_path)
#end

#CSV_write_all_popular_usernames(dst_path_wk, link=pop_link_wk)
#CSV_write_all_popular_usernames(dst_path_mth, link=pop_link_mth)
#CSV_write_all_popular_usernames(dst_path_yr, link=pop_link_yr)
