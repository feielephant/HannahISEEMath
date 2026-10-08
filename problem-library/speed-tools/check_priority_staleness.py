"""
Flags topics where the tracked priority may be stale against the actual wrong/graded
evidence. Does NOT change anything automatically -- raw correctness counts can mislead
(a "wrong" answer can be a calculation slip, a confidence habit, or a stale label, not a
real gap -- see set 2's #22 and #36 for confirmed examples). This only surfaces candidates
for a human to review with the same kind of qualitative check (click log, talking to her)
used throughout this project, before touching student-tracker.json.

Run after updating wrong/graded counts from a newly graded set.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))

DOWNGRADE_MIN_GRADED = 3
DOWNGRADE_MAX_RATE = 0.15
ESCALATE_MIN_GRADED = 2
ESCALATE_MIN_RATE = 0.5

flags = []
for x in t['topics']:
    g, w, p = x.get('graded'), x.get('wrong'), x.get('priority')
    if g is None or w is None or g < 2:
        continue
    rate = w / g
    if p == 'high' and g >= DOWNGRADE_MIN_GRADED and rate <= DOWNGRADE_MAX_RATE:
        flags.append((x['topic'], p, w, g, rate, 'STRONG PERFORMANCE -- consider downgrading from high'))
    elif p in ('maintain', 'low', 'medium', 'unknown') and g >= ESCALATE_MIN_GRADED and rate >= ESCALATE_MIN_RATE:
        flags.append((x['topic'], p, w, g, rate, 'HIGH WRONG RATE -- consider escalating'))

if not flags:
    print('No priority/evidence mismatches found.')
else:
    print(f'{len(flags)} topic(s) flagged for review (not auto-changed):\n')
    for topic, p, w, g, rate, note in sorted(flags, key=lambda f: -f[4]):
        print(f'  [{p:9s}] {topic}')
        print(f'             {w}/{g} wrong ({rate:.0%}) -- {note}')
    print('\nBefore changing any of these, check WHY (click log / direct conversation),')
    print('the same way #22 and #36 were corrected -- a raw ratio alone has been wrong before.')
