
def pretty_print_dict(dictionary, indent = 0):

    tab = "\t"
    for key, value in dictionary.items():
          print(tab * indent + str(key))

          if isinstance(value, dict):
             pretty_print_dict(value, indent + 1)
          else:
             print(tab * (indent + 1) + str(value))
