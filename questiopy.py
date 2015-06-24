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

	if type(input_file) is list:
		input_file = [path.expanduser(input_file_item) for input_file_item in input_file]
	else:
		input_file = path.expanduser(input_file)

	keys_dir = path.dirname(path.realpath(__file__))+'/'+keys_dir
	formats_dir = path.dirname(path.realpath(__file__))+'/'+formats_dir
	keys_list = [path.splitext(i)[0] for i in listdir(keys_dir) if i.endswith('.csv')] #list of questionnare IDs for which we provide decoding

	if data_format == 'testmaker':
		format_processing = pd.read_csv(formats_dir+data_format+'.csv')
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
	elif data_format == "cuQuest1":
		response_data = pd.read_csv(input_file[0], sep=';')
		self_data = pd.read_csv(input_file[1], sep=';')
		self_data = self_data[(self_data['curiosity'].notnull()) & (self_data['knowledge'].notnull())]
		self_data["memory"]=""
		self_data["confabulation"]=""
		print(self_data.columns.values)

		participant_list = list(set(self_data["participant"].values.tolist()))
		correlation_df_columns=["participant", "pCvK", "pCvCo", "pCvM", "pKvCo", "pKvM", "pMvCo", "kCvK", "kCvCo", "kCvM", "kKvCo", "kKvM", "kMvCo", "sCvK", "sCvCo", "sCvM", "sKvCo", "sKvM", "sMvCo"]
		category_list = list(set(self_data["categories"].values.tolist()))

		correlations_df = pd.DataFrame(index=participant_list, columns=correlation_df_columns)
		correlations_df = correlations_df.fillna(0) # with 0s rather than NaNs
		correlations_df["participant"] = participant_list
		for participant in participant_list:
			for correlation_type in ["pearson", "kendall", "spearman"]:
				correlation = self_data[(self_data["participant"] == participant)][["curiosity","knowledge"]].corr(method=correlation_type, min_periods=1)["curiosity"]["knowledge"]
				correlations_df.loc[(correlations_df['participant'] == participant),correlation_type[0]+"CvK"] = correlation
			for category in category_list:
				confabulation_score = response_data.loc[(response_data['participant'] == participant) & (response_data['category'].str.contains(category)) & (response_data['on screen'] == "no"),"responses"].mean()



		#print(self_data.columns.values, category_list)
		#print(response_data)

if __name__ == '__main__':
	parse_results(input_file=["~/data/curquest/data-finale.csv","~/data/curquest/data-cu_kn.csv"],data_format="cuQuest1")
