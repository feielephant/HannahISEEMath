import json, random, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
tracker = json.load(open(os.path.join(HERE, 'student-tracker.json')))
banks = json.load(open(os.path.join(HERE, 'problem-library-banks.json')))
log_path = os.path.join(HERE, 'practice-log.json')
log = json.load(open(log_path)) if os.path.exists(log_path) else {"sets": []}

WEIGHT = {"high": 3, "medium": 2, "low": 1, "maintain": 1, "unknown": 1}
RANK = {"Easy": 1, "Medium": 2, "Hard": 3}
set_no = len(log["sets"]) + 1
random.seed(set_no)

last_seen, times = {}, Counter()
for s in log["sets"]:
    for t in s["topics"]:
        last_seen[t] = s["set_no"]; times[t] += 1

tracked = {t["topic"]: t for t in tracker["topics"]}
pools = {}
for tier in ["Easy", "Medium", "Hard"]:
    pools[tier] = [tracked.get(n, {"topic": n, "tier": tier, "priority": "unknown", "habits": []}) for n in banks[tier]]
    pools[tier] += [t for t in tracker["topics"] if t["tier"] == tier and t["topic"] not in banks[tier]]

MIX = {"Easy": 11, "Medium": 20, "Hard": 7}
def pick(tier, n):
    def score(t):
        gap = set_no - last_seen.get(t["topic"], 0)
        return WEIGHT[t["priority"]] * (1 + min(gap, 3) * 0.5) * random.uniform(0.8, 1.2) / (1 + times[t["topic"]] * 0.2)
    ranked = sorted(pools[tier], key=score, reverse=True)
    counts, out = Counter(), []
    while len(out) < n:
        for t in ranked:
            if counts[t["topic"]] < 3:
                counts[t["topic"]] += 1; out.append(t); break
        else:
            break
    return out

slots = []
for tier, n in MIX.items():
    for t in pick(tier, n):
        slots.append({"tier": tier, "topic": t["topic"], "priority": t.get("priority"), "habits": t.get("habits", [])})

# soft ramp matched to real tests: ~2 Hard in first half, ~5 in second half; the rest shuffle freely
hard = [s for s in slots if s["tier"] == "Hard"]
rest = [s for s in slots if s["tier"] != "Hard"]
random.shuffle(rest)
first_hard, second_hard = hard[:2], hard[2:]
first_pos = sorted(random.sample(range(19), 2))
second_pos = sorted(random.sample(range(19, 38), len(second_hard)))
ordered = [None] * 38
for pos, h in zip(first_pos + second_pos, first_hard + second_hard):
    ordered[pos] = h
free = [i for i in range(38) if ordered[i] is None]
for i, r in zip(free, rest):
    ordered[i] = r
slots = ordered

# balanced answer letters: 10/10/9/9, then shuffled, avoid 3 identical in a row
letters = ["A"]*10 + ["B"]*10 + ["C"]*9 + ["D"]*9
for _ in range(1000):
    random.shuffle(letters)
    if not any(letters[i] == letters[i+1] == letters[i+2] for i in range(len(letters)-2)):
        break
for s, L in zip(slots, letters):
    s["correct_letter"] = L

# diagrams: real test is ~55% diagram/chart/table questions -> ~21 of 38
diag_idx = set(random.sample(range(38), 21))
for i, s in enumerate(slots):
    s["needs_diagram"] = i in diag_idx
    t = tracked.get(s["topic"])
    s["reference"] = {
        "wrong_so_far": (t or {}).get("wrong"), "graded_so_far": (t or {}).get("graded"),
        "times_practised_before": times[s["topic"]], "last_practised_set": last_seen.get(s["topic"]),
    }

plan = {"set_no": set_no, "slots": [dict(n=i+1, **s) for i, s in enumerate(slots)]}
log["sets"].append({"set_no": set_no, "topics": [s["topic"] for s in slots]})
json.dump(log, open(log_path, "w"), indent=1)
print(json.dumps(plan, indent=1))
print("letters:", Counter(letters), "diagram slots:", len(diag_idx),
      "hard in 2nd half:", sum(1 for s in slots[19:] if s["tier"] == "Hard"), "hard in 1st half:", sum(1 for s in slots[:19] if s["tier"] == "Hard"))
