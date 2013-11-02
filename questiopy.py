#!/usr/bin/env python
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian' #if you contribute add your name to the end of this list
#from import_data import get_data
import numpy as np
from os import path, listdir
import pandas as pd 
from chr_helpers import get_config_file
import fnmatch

def main(pre_format='testmaker', source = False):
    localpath = path.dirname(path.realpath(__file__)) + '/'
    config = get_config_file(localpath)
    
    #IMPORT VARIABLES
    output_dir = config.get('Directories', 'output_dir')
    formats_dir = config.get('Directories', 'formats_dir')
    keys_dir = config.get('Directories', 'keys_dir')
    if not source:
	source = config.get('Source', 'source')
    data_path = config.get('Addresses', source)
    file_name = config.get('Addresses', 'file_name')
    data_format = config.get('Parameters', 'data_format')
    #END IMPORT VARIABLES
    
    if data_path[0] == '~':
	data_path = path.expanduser(data_path)
    
    input_file = data_path + file_name
    keys_dir = path.dirname(path.realpath(__file__))+'/'+keys_dir
    formats_dir = path.dirname(path.realpath(__file__))+'/'+formats_dir
    keys_list = [path.splitext(i)[0] for i in listdir(keys_dir) if i.endswith('.csv')] #list of questionnare IDs for which we provide decoding
    format_processing = pd.read_csv(formats_dir+data_format+'.csv')
    if data_format == 'testmaker':
	import key_functions
	raw_data = pd.read_csv(input_file, sep='/').set_index(['ID_v'])
	#~ print(raw_data.columns)
	question_ids = set([i.partition('_')[0] for i in raw_data.columns])
	question_ids = [i for i in question_ids if i in keys_list]
	results = pd.DataFrame(index=raw_data.index, columns=question_ids)
	for sub_test in ['BDI2', 'SQ', 'EQ', 'AQ']: # for sub_test in question_ids:
	    test_key = pd.read_csv(keys_dir+sub_test+'.csv') # load the key used to score the answers
	    test_fields = fnmatch.filter(raw_data.columns, sub_test+'_*') 
	    test_questions = raw_data[test_fields] # slice the relevant answers from the raw results
	    test_questions = test_questions + format_processing['add'][0]
	    #~ print(test_questions)
	    #~ print(np.shape(test_key), np.shape(test_questions))
	    scored_questions = getattr(key_functions, sub_test)(test_questions, test_key)
	    #~ print(scored_questions)
	    results[sub_test] = scored_questions
	    print results
    elif data_format == 'surveygizmo':
	raise ValueError('The \'surveygizmo\' format is not yet supported. If you cannot do without this please direct your query to h.chr@mail.ru.')
    
if __name__ == '__main__':
	main()
