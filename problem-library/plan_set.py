import json, random, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
tracker = json.load(open(os.path.join(HERE, 'student-tracker.json')))
log_path = os.path.join(HERE, 'practice-log.json')
log = json.load(open(log_path)) if os.path.exists(log_path) else {"sets": []}

WEIGHT = {"high": 3, "medium": 2, "low": 1, "maintain": 1, "unknown": 1}
set_no = len(log["sets"]) + 1
last_seen = {}
for s in log["sets"]:
    for t in s["topics"]:
        last_seen[t] = s["set_no"]

random.seed(set_no)
slots = []
TOTAL = 38
MIX = {"Easy": 11, "Medium": 20, "Hard": 7}  # ~28/53/16 of 38, rounded
topics_by_tier = {}
for t in tracker["topics"]:
    topics_by_tier.setdefault(t["tier"], []).append(t)
banks = json.load(open(os.path.join(HERE, 'problem-library-banks.json')))
tracked = {t["topic"] for t in tracker["topics"]}
for tier, names in banks.items():
    for nm in names:
        if nm not in tracked:
            topics_by_tier.setdefault(tier, []).append({"topic": nm, "tier": tier, "priority": "unknown"})

for tier, n in MIX.items():
    pool = topics_by_tier.get(tier, [])
    # rotation: topics not practised in the last 2 sets get a boost, so strong topics keep getting reps
    def score(t):
        gap = set_no - last_seen.get(t["topic"], 0)
        return WEIGHT[t["priority"]] * (1 + min(gap, 3) * 0.5) * random.uniform(0.8, 1.2)
    ranked = sorted(pool, key=score, reverse=True)
    counts = {}
    for _ in range(n):
        for t in ranked:
            if counts.get(t["topic"], 0) < 3:
                counts[t["topic"]] = counts.get(t["topic"], 0) + 1
                slots.append((tier, t["topic"]))
                break

plan = {"set_no": set_no, "slots": [{"n": i+1, "tier": tier, "topic": topic} for i,(tier,topic) in enumerate(slots)]}
print(json.dumps(plan, indent=1))
log["sets"].append({"set_no": set_no, "topics": [s[1] for s in slots]})
json.dump(log, open(log_path, "w"), indent=1)
