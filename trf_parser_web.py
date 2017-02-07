#!/usr/bin/python3
# -*- coding: utf-8 -*-



import mylib_web as ml
import mylib_trf as lt
import argparse
import os
import pandas as pd
import sys
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

pd.options.mode.chained_assignment = None

import json
import shutil
import datetime
#import pylab
#import pickle
#import csv

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
import jinja2

myport=5001

# Initialization of the Flask application
app = Flask(__name__)
app.config.from_object(__name__) 

# Path to working directory
working_dir="static/working_dir/"

#version number
version=0.1

# output filenames
trf_input_file="trf_input.dat"
parsed_output_file="parsed_output.dat"

# maximum age of old files (days)
max_old_files=7

def myformat(value):
    return("{0:0.2f}".format(float(value)))
def FormatDecimal(value_list):
	if value_list != None:
		return(list(map(myformat, value_list)))
	else:
		return(None)
jinja2.filters.FILTERS['FormatDecimal'] = FormatDecimal






##########
# ROUTES #
##########


@app.route('/')
def input(): 
    return render_template('input_form.html', version=version, days=max_old_files)
    

@app.route('/exec',  methods=['GET', 'POST']) 
def myexec():   

	### removing old file
	ml.delete_old_files(working_dir, n_days=max_old_files)

	### temporary directory
	shortname_dir, fullname_dir = ml.create_temp_folder(directory=working_dir)

	### form parameters
	parameters = ml.get_parameters(request.form)
	input_files = ml.get_input_files(request.files, directory=fullname_dir)

	
	for ff in input_files:
		(outtable, nblines, nbwords, nbuwords, nbutags)  = lt.parse_trf(fullname_dir+'/'+ff, parameters['complement'])
		outtable.to_csv(fullname_dir+'/'+parsed_output_file, sep='\t')
		

	return render_template('output.html', 
			working_dir = fullname_dir,
			idd = shortname_dir, 
			dd = outtable, 
			nblines = nblines,
			nbwords = nbwords,
			nbuwords = nbuwords,
			nbutags = nbutags,
			parameters = parameters,
			outfile = parsed_output_file)

@app.route('/output_table/<idd>',  methods=['GET', 'POST']) 
def output_table(idd,  verbose=1):  
	print("hello") 
	table_data=ml.read_parsed_output_file(working_dir+"/"+idd+"/"+parsed_output_file)
	#print(request.form['page'])
	page = int(request.args.get('page'))
	if request.args.get('rows') == 'NaN':
		rows = 50
	else:
		rows = int(request.args.get('rows'))
	print("###############")
	print(rows)
	print(page)
	if verbose > 0:
		print(idd)
	#print(table_data.to_json())
	return(table_data.iloc[((page-1)*rows):((page-1)*rows+rows),:].to_json(orient='records'))


			
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=myport, debug=True)

