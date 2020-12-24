# User Collection

### Description   
Collects usernames and user information from LetterBoxd for use in training and testing models.

**All py files are written to be run on [Google Colab](https://colab.research.google.com "Google Colab")**

### LBoxd_Popular_Users.py
Collects the usernames of any users featured on the 128 pages of "popular" reviewer pages on LetterBoxd and generates a CSV of usernames.

#### Running
Method takes in a path a csv file where the usernames are written and a LetterBoxd link. Default value for the `link` parameter is <https://letterboxd.com/reviewers/popular/this/all-time/>. All of LetterBoxd "popular" lists have 128 pages.
```
CSV_write_all_popular_usernames(dst_path="folder/usernames.csv")
```

### LBoxd_User.py
Collects data on each user based on their username in a given CSV.
This method can be slow for running a lot of users, but increases in speed as the director/actors/genres of a film are added to a dictionary the first time a film is encountered, which reduces the number of web calls. Users are collected in batches of 100 and each 100 is written to a distinct JSON file.

There are two "types" of users, `"pop"` refer to "popular" users whose IDs were collected from "popular reviewers" list on LetterBoxd. `"gen"` refers to "general" users, users whose IDs were collected because they had recently rated one of our collected films. `max` and `min` refer to the file that contains that hundred users (35 refers to users 3500 to 3599, for example). Each 100 users will be written to a file with a name like "pop_users_500_599.json"


*NB: LBoxd_User reads in a key for the Google Maps API that was not uploaded to Github for security reasons*

#### Running
```
write_users_range(csv_path="folder/usernames.csv", max=37, min=0, user_type="pop")
```      
