__author__ = 'Horea Christian'
import pandas as pd
import numpy as np
from os import path

maps = [
	{0:2, 1:1, 2:0, 3:0}, # SQ, EQ
	{0:0, 1:0, 2:1, 3:2}, # SQ, EQ
	{0:1, 1:1, 2:0, 3:0}, # AQ
	{0:0, 1:0, 2:1, 3:1} # AQ
	]

def simple_map(test_questions, test_key):
	for map_num in set(test_key['use_map']):
		test_questions_slice = test_questions.T.ix[test_key[test_key['use_map']==map_num].index] # this is the slice of values remapped in this loop
		test_questions_slice = test_questions_slice.applymap(maps[map_num].get) # this maps the values
		test_questions.T.ix[test_key[test_key['use_map']==map_num].index] = test_questions_slice # this writes the values back to tha DataFrame
	scored_questions = test_questions.T.sum()
	return scored_questions
	
def BDI2(test_questions, test_key):
	scored_questions = np.dot(test_questions, test_key['valence'])
	return scored_questions
	
def SQ(test_questions, test_key):
	scored_questions = simple_map(test_questions, test_key)
	return scored_questions
	
def EQ(test_questions, test_key):
	scored_questions = simple_map(test_questions, test_key)
	return scored_questions

def AQ(test_questions, test_key):
	scored_questions = simple_map(test_questions, test_key)
	return scored_questions
