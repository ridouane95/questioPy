# -*- coding: utf-8 -*-
__author__ = 'Horea Christian'
import pandas as pd
import numpy as np
from os import path

maps = [
	{0:2, 1:1, 2:0, 3:0}, 	#0: SQ, EQ
	{0:0, 1:0, 2:1, 3:2}, 	#1: SQ, EQ
	{0:1, 1:1, 2:0, 3:0}, 	#2: AQ
	{0:0, 1:0, 2:1, 3:1}, 	#3: AQ
	{0:1, 1:0} 				#4: SPQ
	]
	
split_scoring_tests = {
    'ERQ':	['ERQ_re', 'ERQ_su'], #reappraisal, suppression
    'SPQ':	['SPQ_ri', 'SPQ_sa', 'SPQ_md', 'SPQ_uw', 'SPQ_ev', 'SPQ_kef', 'SPQ_us', 'SPQ_ea', 'SPQ_aw', 'SPQ_sum'], # Referenzideen, Soziale Angst, Ungewöhnliche Glaubensinhalte/magisches Denken, Ungewöhnliche Wahrnehmungen, Ungewöhnliches oder exzentrisches Verhalten, Keine engen Freunde, Ungewöhnliche Sprache, Eingeschränkter Affekt, Argwohn/wahnähnliche Vorstellungen, sum.
    'ASRS':	['ASRS_ad', 'ASRS_hy', 'ASRS_sum'] #attention deficit, hyperactivity, sum
    }
	
###BEGIN GENERAL FUNCTIONS
def simple_map(test_questions, test_key):
	for map_num in set(test_key['use_map']):
		test_questions_slice = test_questions.T.ix[test_key[test_key['use_map']==map_num].index] # this is the slice of values remapped in this loop
		test_questions_slice = test_questions_slice.applymap(maps[map_num].get) # THIS maps the values
		test_questions.T.ix[test_key[test_key['use_map']==map_num].index] = test_questions_slice # this writes the values back to tha DataFrame
	scored_questions = test_questions.T.sum()
	return scored_questions
	
def weighted_items(test_questions, test_key_df, key='valence'):
	scored_questions = np.dot(test_questions, test_key_df[key])
	return scored_questions
	
def split_scoring(question_id):
    result_ids=[]
    result_ids = split_scoring_tests.get(question_id, [question_id])
    return result_ids
###END GENERAL FUNCTIONS 

###BEGIN PER-TEST FUNCTIONS
def BSL23(test_questions, test_key, results):
	scored_questions = weighted_items(test_questions, test_key)
	results['BSL23'] = ''
	results['BSL23'] = scored_questions
	return results

def BDI2(test_questions, test_key, results):
	scored_questions = weighted_items(test_questions, test_key)
	results['BDI2'] = ''
	results['BDI2'] = scored_questions
	return results
	
def SQ(test_questions, test_key, results):
	scored_questions = simple_map(test_questions, test_key)
	results['SQ'] = ''
	results['SQ'] = scored_questions
	return results
	
def EQ(test_questions, test_key, results):
	scored_questions = simple_map(test_questions, test_key)
	results['EQ'] = ''
	results['EQ'] = scored_questions
	return results

def AQ(test_questions, test_key, results):
	scored_questions = simple_map(test_questions, test_key)
	results['AQ'] = ''
	results['AQ'] = scored_questions
	return results
	
def ASRS(test_questions, test_key, results):
	results = results.drop('ASRS', 1)
	result_ids = split_scoring(ASRS.__name__)
	for result_id in result_ids:
		scored_questions = weighted_items(test_questions, test_key, key=result_id.split('_', 1 )[1])
		results[result_id] = ''
		results[result_id] = scored_questions
	return results

def SPQ(test_questions, test_key, results):
	test_questions = test_questions.applymap(maps[4].get) # remao (invert) values
	results = results.drop('SPQ', 1)
	result_ids = split_scoring(SPQ.__name__)
	for result_id in result_ids:
		print result_id.split('_', 1 )
		scored_questions = weighted_items(test_questions, test_key, key=result_id.split('_', 1 )[1])
		results[result_id] = ''
		results[result_id] = scored_questions
	return results
	
def ERQ(test_questions, test_key, results):
	test_questions = test_questions + 1 # for this test the "lowest" answer is already scored as 1
	results = results.drop('ERQ', 1)
	result_ids = split_scoring(ERQ.__name__)
	for result_id in result_ids:
		scored_questions = weighted_items(test_questions, test_key, key=result_id.split('_', 1 )[1])
		results[result_id] = ''
		results[result_id] = scored_questions
	return results
###END PER-TEST FUNCTIONS
