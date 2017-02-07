#! /usr/bin/python3.4


import mylib_trf as lt
import argparse
import os
import pandas as pd
pd.options.mode.chained_assignment = None


parser = argparse.ArgumentParser(description='Parse TRF output', epilog='')
parser.add_argument('-i', dest="trf_file", required=True)
parser.add_argument('-o', dest="output_file", required=True)
parser.add_argument("-c", dest="complement", default=True, action='store_false')
parser.add_argument('-verb',  dest="verbose",  type=int, default=10)
args = parser.parse_args()

if not os.path.exists(args.trf_file):
	print ("Input TRF file (%s) not found." % (args.trf_file))
	exit()
	
if os.path.exists(args.output_file):
    os.remove(args.output_file)
(outtable, nblines, nbwords, nbuwords, nbutags)  = lt.parse_trf(args.trf_file, args.complement)
if args.verbose > 0:
	print("Number of lines: %s" %(nblines))
	print("Number of patterns: %s" %(nbwords))
	print("Number of unique patterns: %s" %(nbuwords))
	print("Number of tags: %s" %(nbutags))

outtable.to_csv(args.output_file, sep='\t')

if args.verbose > 0:
	print("Bye bye !!!")

