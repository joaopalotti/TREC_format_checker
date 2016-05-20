# TREC_format_checker
A simple Python script to check if a run is in the correct TREC format


```
> tfc.py <trec_run_file>
```

TREC format is the following:
<queryID> Q0 <docname> <rank> <score> <teamID>

Examples:
```
5 Q0 clueweb12-enwp02-06-01125 1 32.38 example
5 Q0 clueweb12-en0011-25-31331 2 29.73 example
5 Q0 clueweb12-en0006-97-08104 3 21.93 example
```

Separators can be either single/multiple spaces (' ') or tab (\t)


Some of the necessary conditions to have a valid run for CLEF eHealth 2016 are:

1. Rank numbers start from 1. Always. If it is the case that your run starts from 0, we provide the script  "fix_zero_rank.py" to solve this issue.
2. The document scores for the same query should be in descending order.
3. A document cannot appear twice in the list of document for the same query.
4. The same teamID/runID is used all over the run.
5. QueryIDs are in ascending order
6. Filename follows the convention: <TeamName>_<QueryLanguage>_Run<RunNumber>.<FileFormat>. Example: TUW_EN_Run1.txt

