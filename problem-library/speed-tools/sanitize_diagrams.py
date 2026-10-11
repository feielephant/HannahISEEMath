"""
Catches the class of bug found in speed-set-3 #37: an explanation states a specific
value for a labeled point ("Q = 10", "P is 30") that was never actually shown anywhere
on the page (question text or diagram) -- meaning the problem wasn't solvable as
printed, even though the stated final answer is mathematically correct.

Heuristic, not exhaustive: scans each problem's "why" explanation for "LETTER = NUMBER"
/ "LETTER is NUMBER" patterns, then checks whether that NUMBER appears anywhere in the
diagram's own <text>/table content or the question text. A flag means "go look at this
one," not "this is definitely broken" -- some flags will be false positives (e.g. a
number that's part of general reasoning, not a specific given value). Never auto-fixes.

Run before publishing/taking any new or edited set, and after editing any diagram.
"""
import re, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSHEETS = os.path.join(HERE, '..', '..', 'worksheets')

GIVEN_RE = re.compile(r'(?<!to )\b([A-Z])\s*(?:=|is)\s*(-?\d[\d,]*(?:\.\d+)?)\b(?!\s*(?:units?|ticks?|marks?|×|\*))')
NUM_TOKEN_RE = re.compile(r'-?\d[\d,]*(?:\.\d+)?')

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
    flags = []
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
        if not diag:
            continue  # only diagram-bearing problems can have this bug
        m_key = re.search(r'<div class="key"><b>Answer: [A-D]\.</b> (.*?)</div>', chunk, re.S)
        why = m_key.group(1) if m_key else ''
        why_plain = re.sub(r'<[^>]+>', ' ', why)
        pool = card_text_pool(q, diag)
        for letter, num in GIVEN_RE.findall(why_plain):
            num_clean = num.replace(',', '')
            if num_clean not in pool:
                flags.append((n, letter, num_clean, why_plain.strip()[:160]))
    return flags

def main():
    files = sorted(glob.glob(os.path.join(WORKSHEETS, '*-answer-key.html')))
    total_flags = 0
    for path in files:
        flags = check_file(path)
        if flags:
            print(f"\n{os.path.basename(path)}:")
            for n, letter, num, why in flags:
                print(f"  #{n}: explanation says {letter} = {num}, but '{num}' doesn't appear in the question or diagram")
                print(f"       why: {why}")
            total_flags += len(flags)
    if total_flags == 0:
        print("No flags. (Heuristic check -- absence of flags isn't proof of correctness, just no detected cases of this specific bug.)")
    else:
        print(f"\n{total_flags} flag(s) total. Review each by hand -- some will be false positives.")

if __name__ == '__main__':
    main()
