"""
Catches two opposite classes of diagram bug, both found in speed-set-3:

1. OVER-specified (set 3 #37): an explanation states a specific value for a labeled
   point ("Q = 10", "P is 30") that was never actually shown anywhere on the page
   (question text or diagram) -- the problem wasn't solvable as printed, even though
   the stated final answer is mathematically correct.
2. UNDER-specified / wrong presentation (set 3 #23): a topic that the real test always
   presents with a diagram (number line, shaded figure, bar graph, ...) instead states
   its point values directly in the question text with no diagram at all -- a different,
   easier task than the authentic one, and not how the real test ever does it.

Both are heuristic, not exhaustive -- a flag means "go look at this one," not "this is
definitely broken." Never auto-fixes.

Run before publishing/taking any new or edited set, and after editing any diagram.
"""
import re, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSHEETS = os.path.join(HERE, '..', '..', 'worksheets')

GIVEN_RE = re.compile(r'(?<!to )\b([A-Z])\s*(?:=|is)\s*(-?\d[\d,]*(?:\.\d+)?)\b(?!\s*(?:units?|ticks?|marks?|×|\*))')
NUM_TOKEN_RE = re.compile(r'-?\d[\d,]*(?:\.\d+)?')

# Topics where the real test's own convention is to show a diagram and have her
# read values off it, never state them directly in the question text. Added
# 2026-10-11 after set 3 #23 (Split Line Segments / midpoint) shipped with values
# stated in plain text instead of a number-line diagram.
DIAGRAM_EXPECTED_KEYWORDS = [
    'number line', 'line segment', 'midpoint', 'bar graph', 'shaded',
    'composite shape', 'pictograph', 'coordinate',
]

def card_text_pool(q, diag):
    """Numbers considered 'shown on the page' for this problem."""
    pool = set()
    for blob in (q, diag):
        for m in NUM_TOKEN_RE.finditer(re.sub(r'<[^>]+>', ' ', blob)):
            pool.add(m.group(0).replace(',', ''))
    return pool

def check_file(path):
    html = open(path).read()
    cards = html.split('<div class="card">')[1:]
    value_flags = []
    missing_diag_flags = []
    for chunk in cards:
        m_num = re.search(r'<div class="num">(\d+)\. ', chunk)
        if not m_num:
            continue
        n = m_num.group(1)
        m_q = re.search(r'<div class="q">(.*?)</div>', chunk, re.S)
        q = m_q.group(1) if m_q else ''
        after_q = chunk[m_q.end():] if m_q else chunk
        diag = ''
        idx_choices = after_q.find('<div class="choices">')
        if idx_choices > 0:
            between = after_q[:idx_choices].strip()
            if between.startswith('<div class="diag">'):
                diag = between

        m_ref = re.search(r'Tier: \w+ · Topic: ([^<·]+)', chunk)
        topic = m_ref.group(1).strip().replace('&amp;', '&') if m_ref else ''

        if not diag:
            if topic and any(kw in topic.lower() for kw in DIAGRAM_EXPECTED_KEYWORDS):
                missing_diag_flags.append((n, topic))
            continue  # the value-mismatch bug only applies to diagram-bearing problems

        m_key = re.search(r'<div class="key"><b>Answer: [A-D]\.</b> (.*?)</div>', chunk, re.S)
        why = m_key.group(1) if m_key else ''
        why_plain = re.sub(r'<[^>]+>', ' ', why)
        pool = card_text_pool(q, diag)
        for letter, num in GIVEN_RE.findall(why_plain):
            num_clean = num.replace(',', '')
            if num_clean not in pool:
                value_flags.append((n, letter, num_clean, why_plain.strip()[:160]))
    return value_flags, missing_diag_flags

def main():
    files = sorted(glob.glob(os.path.join(WORKSHEETS, '*-answer-key.html')))
    total_flags = 0
    for path in files:
        value_flags, missing_diag_flags = check_file(path)
        if value_flags or missing_diag_flags:
            print(f"\n{os.path.basename(path)}:")
            for n, letter, num, why in value_flags:
                print(f"  #{n}: explanation says {letter} = {num}, but '{num}' doesn't appear in the question or diagram")
                print(f"       why: {why}")
            for n, topic in missing_diag_flags:
                print(f"  #{n}: topic '{topic}' usually needs a diagram by real-test convention, but this has none")
            total_flags += len(value_flags) + len(missing_diag_flags)
    if total_flags == 0:
        print("No flags. (Heuristic check -- absence of flags isn't proof of correctness, just no detected cases of these specific bugs.)")
    else:
        print(f"\n{total_flags} flag(s) total. Review each by hand -- some will be false positives.")

if __name__ == '__main__':
    main()
