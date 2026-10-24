"""Builds the Freelancer Starter Kit from code. Zero LLM calls. Output: dist/ + freelancer-starter-kit.zip"""
import csv, zipfile, pathlib, shutil
root = pathlib.Path(__file__).parent
dist = root / "dist" / "freelancer-starter-kit"
shutil.rmtree(root / "dist", ignore_errors=True)
dist.mkdir(parents=True)

CSS = "body{font-family:Arial,sans-serif;max-width:760px;margin:40px auto;color:#222}table{width:100%;border-collapse:collapse}th,td{border-bottom:1px solid #ddd;padding:8px;text-align:left}th{background:#f4f4f4}.r{text-align:right}h1{margin-bottom:0}.muted{color:#666}"
def html(title, body): return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"

rows = "".join(f"<tr><td>[Description {i}]</td><td class='r'>[Qty]</td><td class='r'>[Rate]</td><td class='r'>[Amount]</td></tr>" for i in range(1, 6))
(dist / "01-invoice.html").write_text(html("Invoice", f"""
<h1>INVOICE</h1><p class='muted'>Invoice # [0001] · Date [YYYY-MM-DD] · Due [YYYY-MM-DD]</p>
<p><b>From:</b> [Your name / business]<br>[Address] · [Email]</p>
<p><b>Bill to:</b> [Client name]<br>[Client address]</p>
<table><tr><th>Description</th><th class='r'>Qty</th><th class='r'>Rate</th><th class='r'>Amount</th></tr>{rows}
<tr><td colspan='3' class='r'><b>Total due</b></td><td class='r'><b>[$0.00]</b></td></tr></table>
<p class='muted'>Payment terms: Net [14]. Pay by [method]. Thank you for your business.</p>"""))

(dist / "02-proposal.html").write_text(html("Project Proposal", """
<h1>Project Proposal</h1><p class='muted'>Prepared for [Client] by [Your name] · [Date]</p>
<h2>1. Overview</h2><p>[One paragraph: the client's problem and your outcome.]</p>
<h2>2. Scope</h2><ul><li>[Deliverable 1]</li><li>[Deliverable 2]</li><li>Not included: [out-of-scope items]</li></ul>
<h2>3. Timeline</h2><table><tr><th>Milestone</th><th>Date</th></tr><tr><td>[Kickoff]</td><td>[ ]</td></tr><tr><td>[First draft]</td><td>[ ]</td></tr><tr><td>[Final delivery]</td><td>[ ]</td></tr></table>
<h2>4. Pricing</h2><p>[Fixed fee $X / hourly $Y]. Deposit [50%] on acceptance.</p>
<h2>5. Terms</h2><p>[Revisions included: 2. Payment: Net 14. Ownership transfers on full payment.]</p>
<h2>Acceptance</h2><p>Signed: ____________________ Date: __________</p>"""))

(dist / "03-client-onboarding-checklist.md").write_text("""# Client Onboarding Checklist

- [ ] Signed proposal and deposit received
- [ ] Kickoff call scheduled
- [ ] Logins / assets / brand files collected
- [ ] Shared folder and communication channel created
- [ ] Milestone dates added to calendar
- [ ] First invoice scheduled
- [ ] Offboarding: final files delivered, final invoice sent, testimonial requested
""")

with open(dist / "04-income-expense-tracker.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Type (income/expense)", "Client / Vendor", "Category", "Amount", "Invoice #", "Paid? (Y/N)", "Notes"])
    for _ in range(25): w.writerow([""] * 8)

with open(dist / "05-project-time-log.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Client", "Project", "Task", "Hours", "Billable (Y/N)"])
    for _ in range(25): w.writerow([""] * 6)

(dist / "README.txt").write_text("""Freelancer Starter Kit
======================
01-invoice.html ................ open in a browser, edit the [brackets], Print > Save as PDF
02-proposal.html ............... same workflow
03-client-onboarding-checklist.md ... any text editor / Notion / Obsidian
04-income-expense-tracker.csv .. opens in Excel, Google Sheets, Numbers
05-project-time-log.csv ........ same

No sign-up, no subscription. Edit freely for your own business. Do not resell the files as-is.
""")

zp = root / "freelancer-starter-kit.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(dist.iterdir()): z.write(p, f"freelancer-starter-kit/{p.name}")
print("built", zp, zp.stat().st_size, "bytes")
