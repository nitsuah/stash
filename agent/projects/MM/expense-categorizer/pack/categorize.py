"""Categorize bank/card CSV exports with simple keyword rules. No AI, no network, no dependencies.
usage: python categorize.py transactions.csv [rules.csv] > categorized.csv
Input needs columns: date, description, amount (negative = money out). Extra columns are kept."""
import csv
import sys


def load_rules(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [(r["keyword"].strip().lower(), r["category"].strip()) for r in csv.DictReader(f) if r["keyword"].strip()]

def main():
    src = sys.argv[1]
    rules = load_rules(sys.argv[2] if len(sys.argv) > 2 else "rules.csv")
    with open(src, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        fields = list(rd.fieldnames or [])
        if "category" not in fields:
            fields.append("category")
        w = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        totals, unmatched = {}, 0
        for row in rd:
            desc = (row.get("description") or "").lower()
            cat = next((c for k, c in rules if k in desc), "Uncategorized")
            row["category"] = cat
            if cat == "Uncategorized":
                unmatched += 1
            raw_amount = (row.get("amount") or "").strip()
            if not __import__("re").fullmatch(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", raw_amount):
                raise ValueError(f"Invalid amount on CSV row {rd.line_num}: {raw_amount!r}")
            amount = float(raw_amount.replace(",", ""))
            totals[cat] = totals.get(cat, 0.0) + amount
            w.writerow(row)
    print("\nSummary:", file=sys.stderr)
    for c, t in sorted(totals.items(), key=lambda x: x[1]):
        print(f"  {c:<22}{t:>10.2f}", file=sys.stderr)
    print(f"  Uncategorized rows: {unmatched} (add keywords to rules.csv)", file=sys.stderr)

main()
