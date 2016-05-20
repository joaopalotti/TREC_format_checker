#!/usr/bin/env python

import argparse
import os
import re
import sys

"""
tfc -- TREC Format Checker
Author: Joao Palotti - joaopalotti@gmail.com
Version 1.0 (May/2016)

Goal: check if a participant run respects the following TREC format:
    1. <queryID> Q0 <docname> <rank> <score> <teamID>

        Examples:
        5 Q0 clueweb12-enwp02-06-01125 1 32.38 example
        5 Q0 clueweb12-en0011-25-31331 2 29.73 example
        5 Q0 clueweb12-en0006-97-08104 3 21.93 example

        Separators can be either single/multiple spaces (' ') or tab (\t)

    2. Rank numbers start from 1. Always.
    3. The scores are in descending order.
    4. A document cannot appear twice in the list of document for the same query.
    5. The same teamID/runID is used all over the run.
    6. QueryIDs are in ascending order
"""

INV_DOC_RANK=-10

def cancast(s, t=int):
    '''
        Check if it is possible to cast value s to type t.
    '''
    try:
        t(s)
        return True
    except ValueError:
        return False

def check_line(nline, curr_top_id, prev_top_id, curr_doc, docs_so_far, curr_rank, prev_rank, curr_score, prev_score, curr_system_name, system_name, filename):
    """
        Main checker -- checks whether a line in the run file is correct comparing the values found in this line with previous seen values.
    """
    #print "Nline %d -- Ctop: %s, ptop: %s, cdoc: %s, crank: %s, prank: %s, cscore: %s, pscore: %s, csystem: %s, psystem: %s" % (nline, curr_top_id, prev_top_id, curr_doc, curr_rank, prev_rank, curr_score, prev_score, curr_system_name, system_name)

    if not cancast(curr_top_id):
        print "Line %d -- Topic '%s' should be integer." % (nline, curr_top_id)
	return False

    if not cancast(curr_rank):
        print "Line %d -- Rank '%s' should be integer." % (nline, curr_top_id)
	return False

    if not cancast(curr_score, float):
        print "Line %d -- Score  '%s' should be integer." % (nline, curr_top_id)
	return False

    if int(curr_top_id) < int(prev_top_id):
        print "Line %d -- Topic '%s' should be bigger than '%s'." % (nline, curr_top_id, prev_top_id)
        return False

    if int(curr_rank) - 1 != int(prev_rank):
	if int(prev_rank) == INV_DOC_RANK and int(curr_rank) != 1:
            print "Line %d -- The first document of topic '%s' should have rank '1'." % (nline, curr_top_id)
            print "We recommend you run the fix_zero_rank.py script:"
            print "> python fix_zero_rank.py %s" % (filename)
            return False

        if int(prev_rank) != INV_DOC_RANK:
	    print "Line %d -- Rank '%s' should have been '%d'." % (nline, curr_rank, int(prev_rank)+1)
            return False

    if float(curr_score) > float(prev_score):
        print "Line %d -- Score '%s' should be smaller than '%s'." % (nline, curr_score, prev_score)
        return False

    if curr_doc in docs_so_far:
        print "Line %d -- Document '%s' should be unique for topic '%s'." % (nline, curr_doc, curr_top_id)
	return False
    docs_so_far.add(curr_doc)

    if curr_system_name != system_name:
        print "Line %d -- Found system name '%s'. Shouldn't it be '%s'." % (nline, curr_system_name, system_name)
        return False

    return True

def check_filename(filename):
    """
    This is not an extensive check, just a light error check for filenames in an incorrect format.
    """

    fields = os.path.basename(filename).split("_")
    valid_query_languages = ["EN", "CS", "FR", "HU", "DE", "PL", "SV"]

    if filename[-4:] != ".txt":
        return "Name your file as .txt"

    if len(fields) != 3:
        return "Your filename should have 2 and only 2 underlines (_)"

    if fields[1] not in valid_query_languages:
        return "%s not found. The <QueryLanguage> should be one of %s" % (fields[1], valid_query_languages)

    return "OK"

def check(filename):
    '''
     Check whether file is a valid TREC run.
    '''
    if not os.path.isfile(filename):
        print "File '%s' does not exist." % (filename)
        return

    status = check_filename(filename)
    if status != "OK":
        print "There is something wrong with your filename"
        print "%s" % (status)
        print "Be sure to name it correctly: <TeamName>_<QueryLanguage>_Run<RunNumber>.dat. Example: TUW_EN_Run1.dat or TUW_DE_Run2.dat"
        return

    f = open(filename)

    line = f.readline()
    nline = 1
    fields = re.split("\s+", line.strip())

    current_topic_id = fields[0]
    q0 = fields[1]
    current_document = fields[2]
    current_doc_rank = fields[3]
    current_score = fields[4]
    current_system_name = fields[5]
    docs_so_far = set([])
    previous_topic_id = 0
    previous_doc_rank = INV_DOC_RANK
    previous_score = sys.float_info.max

    system_name = current_system_name
    if not check_line(nline, current_topic_id, previous_topic_id, current_document, docs_so_far, current_doc_rank,\
            previous_doc_rank, current_score, previous_score, current_system_name, system_name, filename):
        f.close()
	return

    # Read rest of lines. nline starts from 2.
    for nline, line in enumerate(f.readlines(), 2):
        fields = re.split("\s+", line.strip())

        previous_topic_id = current_topic_id
	previous_doc_rank = current_doc_rank
        previous_score = current_score

	current_topic_id = fields[0]
	q0 = fields[1]
	current_document = fields[2]
	current_doc_rank = fields[3]
	current_score = fields[4]
	current_system_name = fields[5]

	if current_topic_id != previous_topic_id:
	    docs_so_far = set([])
    	    previous_doc_rank = INV_DOC_RANK
            previous_score = sys.float_info.max

        if not check_line(nline, current_topic_id, previous_topic_id, current_document, docs_so_far, current_doc_rank,\
            previous_doc_rank, current_score, previous_score, current_system_name, system_name, filename):
            f.close()
	    return

    f.close()
    print "Your run '%s' has the correct format!" % (system_name)

if __name__ == "__main__":
    '''
    Main method: collection command line args and call 'check'.
    '''

    arg_parser = argparse.ArgumentParser(description="Run checker")
    arg_parser.add_argument("trec_run_file", help="TREC style run file (a participating system)")

    args = arg_parser.parse_args()
    check(args.trec_run_file)




