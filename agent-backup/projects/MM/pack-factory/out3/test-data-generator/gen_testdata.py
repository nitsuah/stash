"""python gen_testdata.py --rows 100 --seed 1 --format csv|json > people.csv  (fake people and orders, no real data)"""
import csv, json, random, sys
from datetime import date, timedelta

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

n, seed, fmt = int(arg("--rows", 100)), int(arg("--seed", 1)), arg("--format", "csv")
rnd = random.Random(seed)
first = ["Ana", "Ben", "Chen", "Dara", "Eli", "Fay", "Gus", "Hana", "Ivan", "Jo", "Kai", "Lena", "Milo", "Nia", "Omar", "Pia"]
last = ["Lopez", "Ray", "Wu", "Singh", "Kim", "Okafor", "Novak", "Silva", "Haas", "Reyes", "Costa", "Dube"]
cities = ["Springfield", "Riverton", "Lakeside", "Fairview", "Georgetown", "Madison"]
rows = []
for i in range(1, n + 1):
    f, l = rnd.choice(first), rnd.choice(last)
    rows.append({"id": i, "name": f"{f} {l}", "email": f"{f}.{l}{i}@example.test".lower(), "phone": f"555-01{rnd.randint(0, 99):02d}",
                 "city": rnd.choice(cities), "signup": (date(2026, 1, 1) + timedelta(days=rnd.randint(0, 300))).isoformat(),
                 "order_total": round(rnd.uniform(5, 500), 2)})
if fmt == "json":
    print(json.dumps(rows, indent=2))
else:
    wr = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), lineterminator="\n")
    wr.writeheader()
    wr.writerows(rows)
