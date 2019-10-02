import os

def create_output_folders (city_name):

	results_path = os.path.join \
		(os.getcwd(), "Results")
	if not os.path.exists(results_path):
		os.mkdir(results_path)

	results_path = os.path.join \
		(os.getcwd(), "Figures")
	if not os.path.exists(results_path):
		os.mkdir(results_path)

	results_path = os.path.join \
		(os.getcwd(), "Results", city_name)
	if not os.path.exists(results_path):
		os.mkdir(results_path)

	results_path = os.path.join \
		(os.getcwd(), "Figures", city_name)
	if not os.path.exists(results_path):
		os.mkdir(results_path)
