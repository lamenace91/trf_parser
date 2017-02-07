import pandas as pd
import sys
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
pd.options.mode.chained_assignment = None

###############################################
def get_synonymous_words(word, complement=True):
	synonymous = []
	biword = word + word
	ll= len(word)
	for xx in range(0,len(word)):
		newword = biword[xx:xx+ll]
		synonymous.append(newword)
		if complement:
			compword = Seq(newword, generic_dna).reverse_complement()
			synonymous.append(compword)
	return(synonymous)
		
###############################################
def parse_trf_to_table(trf_file):
	output = []
	inputfile = open(trf_file)	
	for line in inputfile:
		tab = line.rstrip().split(' ')
		if tab[0] == "Sequence:":
			sq = tab[1]
		elif len(tab) == 15:
			tab.append(sq)
			tab.append('notselected')
			#print(tab)
			output.append(tab)

	inputfile.close()
	return(pd.DataFrame(output, columns=['begin', 'end', 'period_size', 'copy_number', 'consensus_size', 'percent_matches', 'percent_indels', 'score', 'A', 'C', 'G', 'T', 'entropy', 'word', 'array', 'sequence_name', 'word_group']))
	
###############################################
def  parse_trf(trf_file, complement = 1, overlap = 1):
	table = parse_trf_to_table(trf_file)
	words = table['word']
	uniq_words = set(words)
	uniq_words_selected ={elem : True for elem in uniq_words}
	outtable = (table.loc[table['word'].isin(['coucou'])])
	nb = 0

	for word in uniq_words:
		if uniq_words_selected[word] == False:
			continue

		synonymous_words = get_synonymous_words(word, complement)
		
		for ww in synonymous_words:
			if ww in uniq_words_selected:
				uniq_words_selected[ww] = False
		subtable = (table.loc[table['word'].isin(synonymous_words)])
		subtable['word_group'] = word
		outtable = outtable.append(subtable)
	
	uniq_tags = set(outtable['word_group'])
	return((outtable, len(table), len(words), len(uniq_words), len(uniq_tags)) )

