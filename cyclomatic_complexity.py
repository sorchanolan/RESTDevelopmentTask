import lizard

def cyclo_complex(file_name):
	file_info = lizard.analyse_file(file_name)
	return file_info.average_cyclomatic_complexity