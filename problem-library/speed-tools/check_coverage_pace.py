"""
Secondary coverage-floor check, NOT a priority re-ranking. The planner (plan_set.py)
should keep doing what it does -- weight topics by wrong-rate/priority, so the topics
she obviously struggles with or is obviously slow on keep getting the most practice.
This script only catches the failure mode where a low-weight topic (priority
unknown/low/maintain) could keep losing that weighted lottery indefinitely and still
have almost no data by test day, the way "Volume of Solids" sat at 1 graded instance
for weeks until QR5 happened to draw it.

Run before building a new set, alongside (not instead of) the usual priority check
in check_priority_staleness.py. Flags topics behind pace for a MINIMUM number of
appearances by the test date; does not touch student-tracker.json or override the
planner's normal priority-driven selection. When building the next set, if a flagged
topic can reasonably fit without displacing a genuinely high-priority/high-wrong-rate
slot, prefer it -- otherwise it's fine to wait, these are floor minimums, not targets.
"""
import json, os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
tracker = json.load(open(os.path.join(HERE, '..', 'student-tracker.json')))
log = json.load(open(os.path.join(HERE, '..', 'practice-log.json')))
banks = json.load(open(os.path.join(HERE, '..', 'problem-library-banks.json')))

TEST_DATE = date(2026, 12, 10)
QR_PER_WEEK, MA_PER_WEEK = 2, 1
QR_SLOTS, MA_SLOTS = 38, 30
MIN_APPEARANCES_BY_TEST = 4  # floor target; not a cap, not a priority override


def thanksgiving_week(year):
    nov = [date(year, 11, d) for d in range(1, 31)]
    thursdays = [d for d in nov if d.weekday() == 3]
    thanksgiving = thursdays[3]
    start = thanksgiving - timedelta(days=thanksgiving.weekday())
    return start, start + timedelta(days=6)


def remaining_full_weeks(today, test_date):
    tg_start, tg_end = thanksgiving_week(today.year if today.month <= 11 else today.year)
    weeks = 0
    cursor = today - timedelta(days=today.weekday())  # Monday of current week
    cursor += timedelta(days=7)  # start counting from NEXT Monday
    while cursor + timedelta(days=6) < test_date:
        if not (tg_start <= cursor <= tg_end):
            weeks += 1
        cursor += timedelta(days=7)
    return weeks


def main():
    today = date.today()
    weeks = remaining_full_weeks(today, TEST_DATE)
    qr_sessions = weeks * QR_PER_WEEK
    ma_sessions = weeks * MA_PER_WEEK
    total_slots = qr_sessions * QR_SLOTS + ma_sessions * MA_SLOTS

    print(f"Today: {today} ({today.strftime('%A')}). Test: {TEST_DATE} ({TEST_DATE.strftime('%A')}).")
    print(f"Full practice weeks remaining (Thanksgiving week excluded): {weeks}")
    print(f"  -> {qr_sessions} more QR sessions, {ma_sessions} more MA sessions, {total_slots} total problem slots")
    print(f"Floor target: every topic reaches >= {MIN_APPEARANCES_BY_TEST} total graded instances by test day.\n")

    tracked_names = set(t['topic'] for t in tracker['topics'])
    all_bank_names = set()
    for tier in ['Easy', 'Medium', 'Hard']:
        all_bank_names |= set(banks.get(tier, []))
    never_tracked = sorted(all_bank_names - tracked_names)

    # also pick up topics queued (but not yet graded) in the latest planned-but-ungraded set,
    # so a topic already sitting in a just-published set isn't double-flagged as untouched
    queued_topics = set()
    for s in log.get('sets', []) + log.get('ma_sets', []):
        if not any(k.startswith('graded') for k in s):
            queued_topics |= set(s.get('topics', []))

    behind = []
    for t in tracker['topics']:
        if t.get('priority') == 'high':
            continue  # high-priority topics are already guaranteed heavy rotation; not what this check is for
        graded = t.get('graded') or 0
        if graded < MIN_APPEARANCES_BY_TEST:
            behind.append((t['topic'], t.get('priority'), graded, t.get('wrong') or 0))

    zero_untracked = [n for n in never_tracked if n not in queued_topics]
    zero_queued = [n for n in never_tracked if n in queued_topics]

    if zero_untracked:
        print(f"*** {len(zero_untracked)} topic(s) with ZERO data ever -- not in any graded OR queued set. Highest priority to fix: ***\n")
        for n in zero_untracked:
            print(f"  [NEVER TESTED] {n}")
        print()
    if zero_queued:
        print(f"{len(zero_queued)} topic(s) with zero graded data, but already queued in an un-graded set (will get their first point once graded):")
        for n in zero_queued:
            print(f"  [queued, ungraded] {n}")
        print()

    if not behind:
        print("No tracked topics below the thin-data floor.")
        return

    behind.sort(key=lambda x: x[2])  # furthest behind first
    print(f"{len(behind)} tracked topic(s) below the floor (priority != high, graded < {MIN_APPEARANCES_BY_TEST}):\n")
    for topic, p, g, w in behind:
        print(f"  [{p or 'unknown':9s}] graded={g}  {topic}")

    print(f"\n{total_slots} slots remain across {qr_sessions + ma_sessions} sets -- plenty of room to close this")
    print("without displacing high-priority slots (closing it fully costs well under half of remaining capacity).")
    print("This is a secondary check: when building the next set, if one of these fits naturally alongside the")
    print("usual wrong-rate/slow-rate priority picks, prefer it. Don't let it crowd out a genuinely high-need slot.")


if __name__ == '__main__':
    main()
