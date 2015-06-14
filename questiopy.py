#!/usr/bin/env python
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian' #if you contribute add your name to the end of this list
import numpy as np
from os import path, listdir
import pandas as pd
from chr_helpers import get_config_file
import fnmatch

def parse_results(input_file=False, source=False, data_format=""):
	localpath = path.dirname(path.realpath(__file__)) + '/'
	config = get_config_file(localpath)

	#IMPORT VARIABLES
	output_dir = config.get('Directories', 'output_dir')
	formats_dir = config.get('Directories', 'formats_dir')
	keys_dir = config.get('Directories', 'keys_dir')
	if not input_file:
		if not source:
			source = config.get('Source', 'source')
		data_path = config.get('Addresses', source)
		file_name = config.get('Addresses', 'file_name')
		input_file = data_path + file_name
	if not data_format:
		data_format = config.get('Parameters', 'data_format')
	#END IMPORT VARIABLES

	input_file = path.expanduser(input_file)

	keys_dir = path.dirname(path.realpath(__file__))+'/'+keys_dir
	formats_dir = path.dirname(path.realpath(__file__))+'/'+formats_dir
	keys_list = [path.splitext(i)[0] for i in listdir(keys_dir) if i.endswith('.csv')] #list of questionnare IDs for which we provide decoding
	format_processing = pd.read_csv(formats_dir+data_format+'.csv')

	if data_format == 'testmaker':
		import key_functions
		raw_data = pd.read_csv(input_file, sep='/').set_index(['ID_v'])
		question_ids = set([i.partition('_')[0] for i in raw_data.columns])
		question_ids = [i for i in question_ids if i in keys_list]
		results = pd.DataFrame(index=raw_data.index, columns=question_ids)
		for sub_test in question_ids: # for sub_test in question_ids:
			test_key = pd.read_csv(keys_dir+sub_test+'.csv') # load the key used to score the answers
			test_fields = fnmatch.filter(raw_data.columns, sub_test+'_*')
			test_questions = raw_data[test_fields] # slice the relevant answers from the raw results
			test_questions = test_questions + format_processing['add'][0] # preprocess data typically for testmaker
			results = getattr(key_functions, sub_test)(test_questions, test_key, results)
	elif data_format in ['surveygizmo', "surveymonkey"]:
		raise ValueError('The \'surveygizmo\' format is not yet supported. If you cannot make due without this please direct your query to h.chr@mail.ru.')
	elif data_format == "berich1":
		raw_data = pd.read_csv(input_file, sep=';')
	return results

if __name__ == '__main__':
	parse_results()
