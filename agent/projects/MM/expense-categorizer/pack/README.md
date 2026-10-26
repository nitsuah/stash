# Expense Categorizer (CSV)

Turn a messy bank or card CSV export into categorized rows plus a per-category summary, using rules you control.
Plain Python 3, no installs, no AI, no accounts. Your data never leaves your computer.

## Use
    python categorize.py sample-transactions.csv rules.csv > categorized.csv

Your CSV needs columns `date`, `description`, `amount` (negative = money out). Extra columns are kept.
Rules are in `rules.csv` (`keyword,category`): the first keyword found in the description wins. Add your own
vendors; rows that match nothing are marked Uncategorized and counted so you know what to add.

## Notes
- Matching is case-insensitive substring, so keep keywords specific ("github", not "git").
- This is not tax or accounting advice. Check categories with your accountant.
- Personal and commercial use; do not resell.
