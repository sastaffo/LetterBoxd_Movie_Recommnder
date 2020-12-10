folder_path = "/content/drive/MyDrive/4th_Year/ML Group Project/Sarah_data/safety/"

## uses old unmerged film data from Philip's Data/all_filmsV2.json 10/Dec/2020 8pm

"""
{  "34722": {
    "name": "Inception",
    "url": "/film/inception/",
    "lid": "34722",
    "tmdb_id": "27205",
    "number_of_ratings": 536165,
    "avg_rating": 4.18,
    "genres": [
      "Science Fiction",
      "Action",
      "Adventure"
    ],
    "director_url": "/director/christopher-nolan/",
    "actors_urls": [
      "/actor/leonardo-dicaprio/",
      "/actor/ken-watanabe/",
      "/actor/joseph-gordon-levitt/",
      "/actor/marion-cotillard/",
      "/actor/elliot-page/"
    ],
    "number_of_likes": 353380,
    "number_of_views": 926820
  }}
"""

def get_relevant_fields(user_json, film_json):
    relevant = {}
    relevant["user_lid"] = user_json["lid"]
    relevant["film_lid"] = film_json["lid"]
    relevant["user_country"] = user_json["country"]
    relevant["user_films_watched"] = len(user_json["ratings_by_film"])
    relevant["film_total_watches"] = film_json["number_of_views"]
    relevant["film_total_likes"] = film_json["number_of_likes"]
    relevant["director"] = try_json(user_json, film_json, "director")
    for i in range(len(film_json["genres"])):
        key = film_json["genres"][i]
        relevant[key] = try_json(user_json, film_json, "genre", index=i)
    for i in range(5):
        key = "actor"+str(i)
        relevant[key] = try_json(user_json, film_json, "actor", index=i)
    print(json.dumps(relevant, indent=2))
    return relevant
#end

def try_json(user_json, film_json, field, index=0):
    if field == "director":
        x = film_json[(field+"_url")]
        x = x.split("/")[2]
    elif field == "actor":
        x = film_json[(field+"s_urls")][index]
        x = x.split("/")[2]
    elif field == "genre":
        #print(film_json)
        x = film_json[(field+"s")][index]
    else: return None
    print(x, end=" : ")
    #end if
    try:
        u_x_avg = user_json[("average_rating_by_"+field)][x]["avg_minus_tot_avg"]
        print("got x")
        return u_x_avg
    except KeyError as ke:
        print("no x", ke)
        return None
    except Exception as e:
        print("Something happened: ", e)
        print(traceback.format_exc())
    #end try
#end

def test_get_revelant_fields():
    inception_lid = "34722"
    film_data_path = folder_path.replace("Sarah_data/safety/", "Philip's Data/all_filmsV2.json")
    all_films = json.loads(read_f(film_data_path).lower())
    inception = all_films[inception_lid]
    #print(json.dumps(inception,indent=2), "\n")

    # user who has watched Inception: "captstevezissou" from 000_099.json
    captstevezissou = {}
    all = json.loads( read_f((folder_path+"gen_users_5100_5199.json")) )
    for u in all["users"]:
        if u["lid"] == "captstevezissou":
            captstevezissou = u
            break
    #end for
    #print(json.dumps(captstevezissou, indent=2), "\n")
    get_relevant_fields(captstevezissou, inception)
    return

print(dt.now())
#test_get_revelant_fields()
