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
            s = (str(dt.now())+" : pages (max:"+self.pages+")")
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
        f = open(path, "w+")
        file_s = ""
        for lid in self.users_lid_list:
            file_s = file_s + (lid + "\n")
        #end for
        f.write(file_s)
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
def CSV_write_all_popular_usernames():
    pop = LBoxd_populars()
    pop.write_user_lids(pop_usernames_csv_path)
#end
#CSV_write_all_popular_usernames()
