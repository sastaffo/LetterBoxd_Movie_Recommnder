# Item-based Collaborative Filtering    

### Description   

```filter_data.py``` - Takes all files data from a folder 'user_film_merge' and creates a refined list of these files (only the data needed for item-based collaboraitve filtering)   

```collab_filtering``` - Use the refined data file created by the code file above and performs collaborative filtering based on that data


### Run     

1. Creating a refined list first:     

**NB: You need a folder 'user_film_merge' in this directory, with all the film data files for this to work!**   

```
python filter_data.py
```

2. Run collaborative filtering using the refined list   
```
python collab_filtering.py
```
