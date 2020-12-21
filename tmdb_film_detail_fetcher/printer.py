"""
@author: Shaun
"""

# NOTE: not used in main code but helpful for debugging
def pretty_print_dict(dictionary, indent = 0):
    """
    Pretty prints a dictionary
    """

    tab = "\t"
    for key, value in dictionary.items():
          print(tab * indent + str(key))

          if isinstance(value, dict):
             pretty_print_dict(value, indent + 1)
          else:
             print(tab * (indent + 1) + str(value))
