import time 
import tempfile
import os
import shutil
from werkzeug import secure_filename
from subprocess import call
import pandas as pd

##############################################################
### create temporary directory
###############################################################
def create_temp_folder(directory, verbose=0):
	fullname_dir=tempfile.mkdtemp(dir=directory)
	shortname_dir=os.path.basename(fullname_dir)
	#print(shortname_dir)
	#print(fullname_dir)
	#try:
		#os.makedirs(shortname_dir)
	#except OSError as exc: 
		#if exc.errno == errno.EEXIST and os.path.isdir(shortname_dir):
			#pass
	if verbose >  5:
		print("#####")
		print("Directory full name: %s" % fullname_dir)
		print("Directory short name: %s" % shortname_dir)	
	return((shortname_dir, fullname_dir))

##############################################################
### deleting old files
###############################################################

def delete_old_files(path, n_days, verbose=9):	
	nb = 0	
	now = time.time()
	for dd in os.listdir(path):
		if os.stat(os.path.join(path, dd)).st_mtime < (now - (n_days * 24 * 60 * 60) ):
			if os.path.isdir(os.path.join(path, dd)):
				if verbose > 8:
					print("########################")
					print("Removing %s ..." % os.path.join(path, dd))
					print("########################")			
				shutil.rmtree(os.path.join(path, dd))
				nb = nb + 1
	return(nb)
	
##############################################################
### get parameter from form
###############################################################

def get_parameters(request_form):
	parameters={}
	#parameters['overlap'] = int(request_form['overlap'])
	parameters['complement'] = int(request_form['complement'])
	if parameters['complement'] == 1:
		parameters['complement'] = True
	else:
		parameters['complement'] = False
		
	return(parameters)

##############################################################
### get input files
###############################################################

def get_input_files(request_files, directory, verbose=0):
	nb_files=0
	input_files=[]
	### parsing file name from the form
	keys=['input1']
	for ii in range(len(keys)):	
		ri=request_files[keys[ii]]
		ri_name = secure_filename(ri.filename)
		if ri_name != "":
			nb_files+=1		
			ri.save(os.path.join(directory, 'input'+str(nb_files)+'.dat'))
			names=(	'input'+str(nb_files)+'.dat')
			input_files.append(names)
			if verbose > 5:
				print("#####")
				print("Uploading image file %d: %s (%s)" % (nb_files, ri_name, 'raw_image'+str(nb_files)+'_raw.png'))

	### example mode if no parsed file
	if nb_files == 0:
		nb_files+=1
		#call(["head", "-n 1005", "static/example.dat", str(os.path.join(directory, "input1.dat"))])	
		shutil.copyfile("static/example.dat", os.path.join(directory, "input1.dat"))
		names=('input1.dat')
		input_files.append(names)
		if verbose > 5:
			print("#####")
			print("Example mode ...")
			print("Uploading image file %d: %s (%s)" % (nb_files, 'example.png', 'raw_image'+str(nb_files)+'_raw.png'))
	return(input_files)

###############################################################
def read_parsed_output_file(infile, sep="\t"):
	df = pd.read_csv(infile, sep)
	return(df)
