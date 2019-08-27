import sys

from Loading.load_data import create_input_pickles

city_name = sys.argv[1]
create_input_pickles\
    (city_name, [9, 10], 500)
