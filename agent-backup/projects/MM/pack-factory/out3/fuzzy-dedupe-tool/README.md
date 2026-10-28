# Fuzzy Dedupe Tool
    python dedupe.py sample.csv company > report.csv
Finds likely duplicates in one column: exact matches after ignoring case, spaces and punctuation, plus similar spellings (default
similarity 0.88; lower with `--threshold 0.8`). It only reports groups with row numbers; you decide what to merge or delete.
Comparison is pairwise, so it suits files up to a few thousand rows. Plain Python 3.

Personal and commercial use. Do not resell or redistribute the files themselves.
