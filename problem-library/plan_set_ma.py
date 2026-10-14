import json, random, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
tracker = json.load(open(os.path.join(HERE, 'student-tracker.json')))
banks = json.load(open(os.path.join(HERE, 'ma-library-banks.json')))
log_path = os.path.join(HERE, 'practice-log.json')
log = json.load(open(log_path)) if os.path.exists(log_path) else {"ma_sets": []}

WEIGHT = {"high": 3, "medium": 2, "low": 1, "maintain": 1, "unknown": 1}
RANK = {"Easy": 1, "Medium": 2, "Hard": 3}
# Same timing-pressure logic as the QR planner (plan_set.py) -- see its comment
# for the full rationale. Topic tier/priority/avg_seconds all live in the same
# shared student-tracker.json, so this reuses identical constants.
SLOW_SECONDS = 90
SLOW_BONUS = 1.4
N_PROBLEMS = 30
set_no = len(log["ma_sets"]) + 1
random.seed(1000 + set_no)  # offset from the QR seed space so QR/MA shuffles never collide

last_seen, times = {}, Counter()
for s in log["ma_sets"]:
    for t in s["topics"]:
        last_seen[t] = s["set_no"]; times[t] += 1

tracked = {t["topic"]: t for t in tracker["topics"]}
pools = {}
for tier in ["Easy", "Medium", "Hard"]:
    pools[tier] = [tracked.get(n, {"topic": n, "tier": tier, "priority": "unknown", "habits": []}) for n in banks[tier]]
    # Unlike the QR banks (118 topics, a near-complete canonical list), the MA
    # banks (33 topics, built 2026-10-13 from tracker topics that have actual
    # ma_library.json evidence) are not guaranteed complete -- don't also pull
    # in every tracker topic of this tier like the QR planner does, since most
    # QR-only tracker topics (Cryptarithm, Who-Am-I puzzles, etc.) have never
    # shown up in an MA set and shouldn't be eligible for one.

# MIX and diagram ratio follow MA1's real, parent-reviewed composition
# (Easy 11 / Medium 15 / Hard 4 = 30) and the empirically-measured MA diagram
# rate (71.1%, see reference_qr_vs_ma_distinction memory) rather than copying
# QR's 11/20/7-of-38 and ~55%-diagram numbers verbatim.
MIX = {"Easy": 11, "Medium": 15, "Hard": 4}

def pick(tier, n):
    # Same coverage-first / decay / slow-bonus scoring as plan_set.py's pick().
    def score(t):
        gap = set_no - last_seen.get(t["topic"], 0)
        decay = 1 if t["priority"] == "high" else (1 + times[t["topic"]] * 0.2)
        slow_bonus = SLOW_BONUS if (t.get("avg_seconds") or 0) > SLOW_SECONDS else 1
        return WEIGHT[t["priority"]] * (1 + min(gap, 3) * 0.5) * slow_bonus * random.uniform(0.8, 1.2) / decay
    ranked = sorted(pools[tier], key=score, reverse=True)
    counts, out = Counter(), []
    while len(out) < n:
        progressed = False
        for t in ranked:
            if len(out) >= n:
                break
            if counts[t["topic"]] < 3:
                counts[t["topic"]] += 1; out.append(t); progressed = True
        if not progressed:
            break
    return out

slots = []
for tier, n in MIX.items():
    for t in pick(tier, n):
        slots.append({"tier": tier, "topic": t["topic"], "priority": t.get("priority"), "habits": t.get("habits", [])})

# soft ramp: with only 4 Hard slots for 30 problems, put ~1 in the first half
# and the rest in the second half, same spirit as QR's 2-then-5 split.
hard = [s for s in slots if s["tier"] == "Hard"]
rest = [s for s in slots if s["tier"] != "Hard"]
random.shuffle(rest)
first_hard, second_hard = hard[:1], hard[1:]
first_pos = sorted(random.sample(range(15), len(first_hard)))
second_pos = sorted(random.sample(range(15, N_PROBLEMS), len(second_hard)))
ordered = [None] * N_PROBLEMS
for pos, h in zip(first_pos + second_pos, first_hard + second_hard):
    ordered[pos] = h
free = [i for i in range(N_PROBLEMS) if ordered[i] is None]
for i, r in zip(free, rest):
    ordered[i] = r
slots = ordered

# balanced answer letters for 30 problems: 8/8/7/7, shuffled, no 3-in-a-row
letters = ["A"]*8 + ["B"]*8 + ["C"]*7 + ["D"]*7
for _ in range(1000):
    random.shuffle(letters)
    if not any(letters[i] == letters[i+1] == letters[i+2] for i in range(len(letters)-2)):
        break
for s, L in zip(slots, letters):
    s["correct_letter"] = L

# diagrams: MA's measured real rate is ~71.1% (vs QR's ~50.4%) -> ~21 of 30
diag_idx = set(random.sample(range(N_PROBLEMS), round(N_PROBLEMS * 0.711)))
for i, s in enumerate(slots):
    s["needs_diagram"] = i in diag_idx
    t = tracked.get(s["topic"])
    s["reference"] = {
        "wrong_so_far": (t or {}).get("wrong"), "graded_so_far": (t or {}).get("graded"),
        "times_practised_before": times[s["topic"]], "last_practised_set": last_seen.get(s["topic"]),
    }

plan = {"set_no": set_no, "slots": [dict(n=i+1, **s) for i, s in enumerate(slots)]}
log["ma_sets"].append({"set_no": set_no, "topics": [s["topic"] for s in slots]})
json.dump(log, open(log_path, "w"), indent=1)
print(json.dumps(plan, indent=1))
print("letters:", Counter(letters), "diagram slots:", len(diag_idx),
      "hard in 2nd half:", sum(1 for s in slots[15:] if s["tier"] == "Hard"), "hard in 1st half:", sum(1 for s in slots[:15] if s["tier"] == "Hard"))
