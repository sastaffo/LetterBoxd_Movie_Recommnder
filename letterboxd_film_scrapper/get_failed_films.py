'''
Created on 7 Dec 2020

@author: bradishp
'''
import re
import jsonpickle

invalid_film_list = []

def export_invalid_film_list():
    with open("invalid_movies/invalid_movies.json", 'w') as f:
        json_format = jsonpickle.encode(invalid_film_list, unpicklable=False)
        print(json_format, file=f)

if __name__ == '__main__':
    with open("FirstHalfConsoleOutput.txt", 'r') as f:
        conents = f.readlines()
    last_line = None
    for line in conents:
        if "Invalid" in line:
            invalid_film_url = re.findall(r'h.*/', last_line)
            invalid_film_list.append(invalid_film_url[0])
            print(line, end="-")
            print(last_line, end="")
        elif "Outputing" in line:
            print(line, end="")
        last_line = line
    export_invalid_film_list()
    