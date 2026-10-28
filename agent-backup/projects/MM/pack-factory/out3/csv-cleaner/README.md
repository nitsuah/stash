# CSV Cleaner
    python csv_clean.py messy.csv clean.csv --dedupe --lower-emails --phones --dates signup
Trims and collapses spaces, removes exact duplicate rows, lowercases email columns, normalizes US phone numbers and dates (YYYY-MM-DD).
Columns are matched by name (columns containing "email" or "phone"). Review the output before using it. Plain Python 3.

Personal and commercial use. Do not resell or redistribute the files themselves.
