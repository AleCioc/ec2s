import sys
city_name = sys.argv[1]

# from Loading.create_input_pickles import run_create_pickles
# run_create_pickles(city_name)

from ModelValidation.model_validation import run_model_validation
run_model_validation(city_name)
