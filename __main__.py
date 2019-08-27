import sys
city_name = sys.argv[1]

# from Loading.create_input_pickles import run_create_pickles
# run_create_pickles(city_name)

# from ModelValidation.model_validation import run_model_validation
# run_model_validation(city_name)

# from MultipleRun.multiple_runs import multiple_runs
# multiple_runs(city_name)

from MultipleRun.only_hub import run_only_hub
run_only_hub(city_name)
