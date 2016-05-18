#!/usr/bin/env python

import argparse
import os
import re
import sys

"""
fix_zero_rank
Author: Joao Palotti - joaopalotti@gmail.com
Version 1.0 (May/2016)

Goal: reads a file in the following TREC format (no checks are made):
     <queryID> Q0 <docname> <rank> <score> <teamID>

     and increases by one the rank of every document.
     It outputs a file .fix at the end.
"""

def fix_rank(filename):
    '''
       Add one to every document rank
    '''

    if not os.path.isfile(filename):
        print "File '%s' does not exist." % (filename)
        return

    f = open(filename, "r")
    fout = open(filename + ".fix", "w")

    for nline, line in enumerate(f.readlines(), 1):
        fields = re.split("\s+", line.strip())
        if len(fields) != 6:
            print "File %s -- line %d: it should contain 6 fields, but %d were found. Stoped here!" % (filename, nline, len(fields))
            print fields
            return

        qid = fields[0]
	q0 = fields[1]
	docid = fields[2]
	doc_rank = fields[3]
	doc_score = fields[4]
	system_name = fields[5]

        fout.write("%s %s %s %d %s %s\n" % (qid,q0,docid,int(doc_rank)+1,doc_score,system_name))

    print "OK! All went right. Document %s created." % (filename + ".fix")
    fout.close()
    f.close()

if __name__ == "__main__":
    '''
    Main method: collection command line args and call 'fix_rank'.
    '''

    arg_parser = argparse.ArgumentParser(description="Run checker")
    arg_parser.add_argument("trec_run_file", help="TREC style run file (a participating system)")

    args = arg_parser.parse_args()
    fix_rank(args.trec_run_file)











