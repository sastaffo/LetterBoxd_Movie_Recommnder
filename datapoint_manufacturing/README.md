# Manufacturing Datapoints

### Description   
Processes the files containing User data (collected by Sarah(sastaffo)) and Film data (collected by Philip(XanthusXX) and Shaun(ShaunJose)) to create datapoints to train our models.

**All py files are written to be run on [Google Colab](https://colab.research.google.com "Google Colab")**

### merge_user_film_pairs.py
Reads in user and film data and outputs the data in JSON form. Each 100 users is written to a distinct file so that no one file is too large.
Since the training and testing files were kept in different folders to avoid confusion, there are two different commands to run the program.

There are two "types" of users, `"pop"` refer to "popular" users whose IDs were collected from "popular reviewers" list on LetterBoxd. `"gen"` refers to "general" users, users whose IDs were collected because they had recently rated one of our collected films. `max` and `min` refer to the file that contains that hundred users (35 refers to users 3500 to 3599, for example)

#### Running
```
some_pairs(max=38, min=0, user_type="pop")
some_test_pairs(max=9, min=0, user_type="gen")
```

### user_film_pairs_to_csv.py
Reads in the "merged" JSON files created in the above program and generates CSV files that are quicker for the modelling program to read in.
Some methods collect metadata on the film information to determine the frequency of the release months/decades and the production companies/countries/continents

#### Running
One runnable method transforms the JSON files into CSV files and another merges existing CSV files into larger files to improve reading-in time. Training and testing sets are transformed/merged using different methods.
```
some_pairs_to_csv(max=38, min=0, user_type="pop")
some_test_pairs_to_csv(max=9, min=0, user_type="gen")
merge_csvs()
merge_test_csvs()
```
