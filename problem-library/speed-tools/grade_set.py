"""
Automates grading a taken speed set: pulls the EXACT as-published worksheet
(via the commit hash recorded by mark_published.py, never the live HEAD file,
which may have been edited/fixed since she took it), scores it against the
downloaded times CSV, flags possible unsolvable-diagram bugs, updates
practice-log.json and student-tracker.json, and renders the local review page.

Hard rule this enforces: the review page must show problems EXACTLY as she saw
them. If a diagram had a bug, the review shows the buggy diagram too -- never
a silently-fixed version. That's the whole point of sourcing from the
published commit instead of the live file.

What this does NOT do: decide whether a wrong answer is a real gap, a slip,
or inconclusive. That takes actually reading each wrong problem and her
answer pattern -- real judgment, not boilerplate. Any wrong problem without a
supplied note renders as "NEEDS DIAGNOSIS" in the review, on purpose, so an
unreviewed problem can never silently ship.

Typical use (called from a short one-off script, not really a CLI tool,
since the notes dict naturally wants to be authored alongside the analysis):

    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from grade_set import *

    problems = load_published_problems('qr', 4)
    grading = grade(problems, '/path/to/speed-set-4-times.csv')
    print(grading['wrong'])  # go look at each one

    flags = sanitize_check(problems)  # cross-check against possible page bugs
    for f in flags: print(f)
    missing_diag = check_missing_diagram(problems)  # diagram-shaped topics with no diagram
    for f in missing_diag: print(f)
    flagged = {n: f"References {l}={v}, not shown on the page." for n, l, v, _ in flags}
    for n, topic in missing_diag:
        flagged[n] = f"Topic '{topic}' usually needs a diagram by real-test convention, but this has none."

    notes = {
      6: dict(kind='gap', title='Real gap -- ...', body='...'),
      12: dict(kind='careless', title='Not a gap -- ...', body='...'),
      # one entry per wrong problem number; omit one and the review marks it
      # NEEDS DIAGNOSIS instead of silently leaving it out
    }

    build_review_html(problems, grading, notes, title='Speed Set 4',
                       out_path='/Users/kxieztt/Documents/HannahISEEMath/reviews/speed-set-4-review-2026-XX-XX.html',
                       flagged=flagged)
    update_tracker_and_log('qr', 4, problems, grading, notes)
"""
import json, re, csv, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..')
LOG_PATH = os.path.join(HERE, '..', 'practice-log.json')
TRACKER_PATH = os.path.join(HERE, '..', 'student-tracker.json')

SLUG = {'qr': 'speed-set-{}', 'ma': 'ma-set-{}'}


# ---------- 1. Pull the exact as-published snapshot ----------

def _set_entry(kind, set_no):
    log = json.load(open(LOG_PATH))
    key = 'sets' if kind == 'qr' else 'ma_sets'
    entries = log.get(key, [])
    target = next((e for e in entries if e.get('set_no') == set_no), None)
    if target is None:
        raise SystemExit(f"No entry with set_no={set_no} in '{key}' of practice-log.json.")
    if 'published_commit' not in target:
        raise SystemExit(
            f"No published_commit recorded for {kind} set {set_no}. "
            f"Run mark_published.py at publish time, before she takes it. "
            f"(If this set predates that convention, find the right commit by hand via "
            f"`git log --oneline -- worksheets/{SLUG[kind].format(set_no)}-answer-key.html` "
            f"and set it manually in practice-log.json.)"
        )
    return log, key, target

def load_published_problems(kind, set_no):
    """Returns {problem_num: {q, diag, choices, ans, why, tier, topic}} from the
    EXACT commit that was live when the set was published -- not current HEAD."""
    _, _, target = _set_entry(kind, set_no)
    commit = target['published_commit']
    slug = SLUG[kind].format(set_no)
    path = f'worksheets/{slug}-answer-key.html'
    html = subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=REPO).decode()
    return _parse_answer_key(html)

_DIV_TAG_RE = re.compile(r'<div\b[^>]*>|</div>')

def _balanced_div_content(html, start_idx):
    """start_idx is right after the opening '<div ...>' tag's '>'. Returns
    (content, end_idx) where end_idx is right after the matching closing
    '</div>', counting nested <div>s so a question like #22's (two equation
    lines, each wrapped in its own inner <div>) doesn't get cut off at the
    first </div) the naive non-greedy regex would have stopped at -- that
    bug truncated #22's question to just the first equation line and lost
    the second equation and the actual question text (caught 2026-10-27)."""
    depth = 1
    i = start_idx
    while True:
        m = _DIV_TAG_RE.search(html, i)
        if not m:
            return html[start_idx:], len(html)
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return html[start_idx:m.start()], m.end()
        else:
            depth += 1
        i = m.end()

def _parse_answer_key(html):
    # split on the opening card tag, tolerating an optional data-n="N" attribute
    # (added once MA sets moved to the paginated one-problem-per-page harness, which
    # stamps every card with data-n for its prev/next nav -- plain QR cards have none)
    cards_raw = re.split(r'<div class="card"(?: data-n="\d+")?>', html)[1:]
    problems = {}
    for chunk in cards_raw:
        m_num = re.search(r'<div class="num">(\d+)\. ', chunk)
        if not m_num:
            continue
        n = int(m_num.group(1))
        m_qopen = re.search(r'<div class="q">', chunk)
        if m_qopen:
            q, q_end = _balanced_div_content(chunk, m_qopen.end())
            after_q = chunk[q_end:]
        else:
            q, after_q = '', chunk
        diag = ''
        idx_choices = after_q.find('<div class="choices">')
        if idx_choices > 0:
            between = after_q[:idx_choices].strip()
            if between.startswith('<div class="diag">'):
                diag = between
        m_choices = re.search(r'<div class="choices">(.*?)</div><div class="key">', chunk, re.S)
        choices_html = m_choices.group(1) if m_choices else ''
        parts = re.split(r'</span><span><b>', choices_html)
        ch = []
        for i, part in enumerate(parts):
            piece = part
            if i == 0:
                piece = re.sub(r'^<span><b>', '', piece)
            if i == len(parts) - 1:
                piece = re.sub(r'</span>\s*$', '', piece)
            mm = re.match(r'([A-D])</b>&nbsp; (.*)', piece, re.S)
            if mm:
                ch.append((mm.group(1), mm.group(2)))
        m_key = re.search(r'<div class="key"><b>Answer: ([A-D])\.</b> (.*?)</div>', chunk, re.S)
        ans, why = (m_key.group(1), m_key.group(2)) if m_key else (None, '')
        # accept either the literal middle-dot or its HTML entity as the separator
        m_ref = re.search(r'Tier: (\w+) (?:·|&middot;) Topic: ([^<·]+?)(?:&middot;| ·|<)', chunk)
        tier, topic = (m_ref.group(1), m_ref.group(2).strip().replace('&amp;', '&')) if m_ref else ('', '')
        problems[n] = dict(q=q, diag=diag, choices=ch, ans=ans, why=why, tier=tier, topic=topic)
    return problems


# ---------- 2. Grade against the downloaded times CSV ----------

def grade(problems, times_csv_path):
    """A row's 'seconds' may be empty -- used for a problem she answered on
    paper after the digital timer ran out (no per-problem timing exists for
    those, since she wasn't clicking through the UI). Those rows still count
    for correctness/topic tallies but are excluded from total_minutes and the
    slowest/fastest lists, so they don't fake a 0-second (or any) pacing
    number. Added 2026-10-18 for QR5, the first set she didn't finish
    digitally -- matches her documented real-test pattern of not finishing
    QR under time pressure, so expect this to recur."""
    rows = {int(r['problem']): r for r in csv.DictReader(open(times_csv_path))}
    n_total = len(problems)
    wrong, blank = [], []
    wrong_to_right, wrong_to_wrong, right_to_wrong = [], [], []
    for n in range(1, n_total + 1):
        r = rows.get(n)
        if r is None:
            blank.append(n)
            continue
        ans = problems[n]['ans']
        first_ok = r['first_answer'] == ans
        final_ok = r['final_answer'] == ans
        if not final_ok:
            wrong.append(n)
        if r['first_answer'] != r['final_answer']:
            if not first_ok and final_ok:
                wrong_to_right.append(n)
            elif not first_ok and not final_ok:
                wrong_to_wrong.append(n)
            elif first_ok and not final_ok:
                right_to_wrong.append(n)
    timed_rows = {n: r for n, r in rows.items() if r.get('seconds', '').strip() != ''}
    total_sec = sum(float(r['seconds']) for r in timed_rows.values())
    by_time = sorted(((n, float(r['seconds'])) for n, r in timed_rows.items()), key=lambda x: -x[1])
    return dict(
        rows=rows, n_total=n_total, n_correct=n_total - len(wrong) - len(blank),
        wrong=wrong, blank=blank,
        total_minutes=round(total_sec / 60, 2),
        wrong_to_right=wrong_to_right, wrong_to_wrong=wrong_to_wrong, right_to_wrong=right_to_wrong,
        slowest=by_time[:8], fastest=by_time[-8:],
    )


# ---------- 2b. Indecision from the click log (richer than times.csv) ----------

def changes_from_click_log(click_log_path, problems):
    """times.csv (and grade()'s wrong_to_right/wrong_to_wrong/right_to_wrong)
    only compares first_answer vs final_answer -- it's BLIND to a problem she
    changed and then changed BACK, since first == final looks "unchanged."
    Found on QR5 #2 (2026-10-18): she picked D, changed to C (the actual
    correct answer), then changed back to D (wrong) -- invisible to the times
    CSV, which just shows first=D final=D. The click log has every intermediate
    pick, so use it when available for the true indecision picture.

    Returns {problem: dict(picks=[letters chosen in order, 'cleared' events
    excluded], n_changes=int, first=letter, final=letter, self_corrected=bool
    (final is right, first wasn't), had_correct_then_left=bool (the right
    answer was picked at some point but NOT kept))} for every problem with 2+
    picks (i.e. she changed her answer at least once, however it netted out).
    Problems answered only once, or answered on paper (not in the click log
    at all), are simply absent from the result."""
    rows_by_problem = {}
    for row in csv.DictReader(open(click_log_path)):
        rows_by_problem.setdefault(int(row['problem']), []).append(row)
    out = {}
    for n, rows in rows_by_problem.items():
        picks = [r['letter'] for r in rows if r['action'] in ('chose', 'changed') and r['letter']]
        if len(picks) < 2:
            continue
        ans = problems.get(n, {}).get('ans')
        final = picks[-1]
        first = picks[0]
        out[n] = dict(
            picks=picks, n_changes=len(picks) - 1, first=first, final=final,
            self_corrected=(ans is not None and final == ans and first != ans),
            had_correct_then_left=(ans is not None and ans in picks[:-1] and final != ans),
        )
    return out


# ---------- 3. Flag possible unsolvable-diagram bugs (same heuristic as sanitize_diagrams.py) ----------

GIVEN_RE = re.compile(r'(?<!to )\b([A-Z])\s*(?:=|is)\s*(-?\d[\d,]*(?:\.\d+)?)\b(?!\s*(?:units?|ticks?|marks?|×|\*))')
NUM_TOKEN_RE = re.compile(r'-?\d[\d,]*(?:\.\d+)?')

def sanitize_check(problems):
    """Returns [(n, letter, number, why_text)] for explanations that state a
    specific point value not found anywhere in that problem's own question/diagram.
    Heuristic -- review each by hand, same caveats as sanitize_diagrams.py."""
    flags = []
    for n, p in problems.items():
        if not p['diag']:
            continue
        pool = set()
        for blob in (p['q'], p['diag']):
            for m in NUM_TOKEN_RE.finditer(re.sub(r'<[^>]+>', ' ', blob)):
                pool.add(m.group(0).replace(',', ''))
        why_plain = re.sub(r'<[^>]+>', ' ', p['why'])
        for letter, num in GIVEN_RE.findall(why_plain):
            if num.replace(',', '') not in pool:
                flags.append((n, letter, num, why_plain.strip()[:160]))
    return flags

# Topics where the real test's own convention is to show a diagram and have
# her read values off it, never state them directly in the question text.
# Added 2026-10-11 after set 3 #23 (Split Line Segments / midpoint) shipped
# with values stated in plain text instead of a number-line diagram --
# sanitize_check() can't catch this class of bug because it only looks at
# problems that ALREADY have a diagram (`if not p['diag']: continue`); this
# one is the opposite case, a diagram-shaped topic missing its diagram.
DIAGRAM_EXPECTED_KEYWORDS = [
    'number line', 'line segment', 'midpoint', 'bar graph', 'shaded',
    'composite shape', 'pictograph', 'coordinate',
]

def check_missing_diagram(problems):
    """Returns [(n, topic)] for problems whose topic is one of the real test's
    diagram-convention topics (number line, shaded figure, bar graph, etc.)
    but which has no <div class="diag"> on the page. Heuristic by topic name,
    same caveats as sanitize_check() -- review each by hand, don't auto-fix."""
    flags = []
    for n, p in problems.items():
        if p['diag']:
            continue
        topic_lower = p['topic'].lower()
        if any(kw in topic_lower for kw in DIAGRAM_EXPECTED_KEYWORDS):
            flags.append((n, p['topic']))
    return flags


# ---------- 4. Render the review HTML ----------

_CSS = open(os.path.join(HERE, 'review_template.css')).read() if os.path.exists(os.path.join(HERE, 'review_template.css')) else None

def _choices_html(p, her_final):
    out = []
    for L, c in p['choices']:
        cls, tags = 'choice', ''
        if L == p['ans']:
            cls += ' correct'
            tags += '<span class="tag c">✓ correct</span>'
        if L == her_final:
            cls += ' herpick'
            tags += f'<span class="tag {"c" if L==p["ans"] else "h"}">← her answer</span>'
        out.append(f'<div class="{cls}"><b>{L}</b>&nbsp; {c}{tags}</div>')
    return ''.join(out)

def build_review_html(problems, grading, notes, title, out_path, flagged=None, slow_threshold_sec=90, changes=None):
    """notes: {problem_num: dict(kind='gap'|'careless'|'uncertain', title=.., body=..)}
    One entry expected per wrong problem. Missing ones render as NEEDS DIAGNOSIS,
    on purpose -- this is the safety net against shipping an unreviewed problem.
    Each wrong-problem card links to the NEXT wrong problem (wrapping around),
    not back to the top jumplist -- lets you review misses one after another.

    flagged: {problem_num: message} from sanitize_check()/check_missing_diagram()
    results -- build it like:
        flagged = {}
        for n, letter, num, why in sanitize_check(problems):
            flagged[n] = f"References {letter}={num}, which doesn't appear in the question or diagram."
        for n, topic in check_missing_diagram(problems):
            flagged[n] = f"Topic '{topic}' usually needs a diagram by real-test convention, but this has none."
    A bare set/list of problem numbers also works (uses a generic message), for
    backward compatibility.

    slow_threshold_sec: any TIMED problem (has a numeric seconds value -- untimed
    paper-finished rows from grade()'s "answered after the digital timer" support
    don't count, there's nothing to threshold) at or above this is "took a long
    time," right or wrong. Separate from the wrong/gap tables on purpose -- a slow
    CORRECT answer is still a pacing signal worth seeing, not just a correctness
    one. Added 2026-10-18 at the parent's request for a second, independently
    clickable jumplist/table alongside the wrong-problem one.

    changes: optional result of changes_from_click_log(click_log_path, problems)
    -- {problem: dict(picks, n_changes, first, final, self_corrected,
    had_correct_then_left)}. When given, adds a third table + jumplist for
    every problem she picked more than once (whatever it netted out to), and
    replaces the per-card "first picked/changed to" line with the full pick
    sequence. Without it, cards fall back to the simpler first-vs-final
    comparison from the times CSV, which is blind to a change that nets out
    unchanged (e.g. picked right, then changed back to wrong). Added
    2026-10-18 at the parent's request, after QR5 #2 showed exactly that
    blind spot."""
    flagged = flagged or {}
    changes = changes or {}
    if not isinstance(flagged, dict):
        flagged = {n: 'The explanation references a specific value not found in the question or diagram text.' for n in flagged}
    wrong = grading['wrong']
    rows_data = grading['rows']
    n_total = grading['n_total']

    missing_notes = [n for n in wrong if n not in notes]

    gap_rows, careless_rows, uncertain_rows = '', '', ''
    for n in wrong:
        topic = problems[n]['topic']
        if n not in notes:
            row = f'<tr><td>#{n}</td><td>{topic}</td><td><b>⚠ NEEDS DIAGNOSIS</b> — not yet reviewed.</td></tr>'
            uncertain_rows += row
            continue
        note = notes[n]
        row = f'<tr><td>#{n}</td><td>{topic}</td><td>{note["body"]}</td></tr>'
        if note['kind'] == 'gap':
            gap_rows += row
        elif note['kind'] == 'careless':
            careless_rows += row
        else:
            uncertain_rows += row

    slow = sorted(
        ((n, float(r['seconds'])) for n, r in rows_data.items() if r.get('seconds', '').strip() != '' and float(r['seconds']) >= slow_threshold_sec),
        key=lambda x: -x[1])
    slow_nums = [n for n, _ in slow]
    slow_rows = ''
    for n, sec in slow:
        topic = problems[n]['topic']
        result = 'wrong' if n in wrong else 'right'
        slow_rows += f'<tr><td>#{n}</td><td>{topic}</td><td>{sec:.0f}s</td><td class="{result}">{result}</td></tr>'

    changed_nums = sorted(changes.keys())
    changed_rows = ''
    for n in changed_nums:
        c = changes[n]
        topic = problems[n]['topic']
        path = ' → '.join(c['picks'])
        result = 'wrong' if n in wrong else 'right'
        flag = ''
        if c['self_corrected']:
            flag = '<span class="pill self-corrected">self-corrected</span>'
        elif c['had_correct_then_left']:
            flag = '<span class="pill left-correct">had it right, changed away</span>'
        changed_rows += (f'<tr><td>#{n}</td><td>{topic}</td><td>{path}</td>'
                         f'<td>{c["n_changes"]}</td><td class="{result}">{result}</td><td>{flag}</td></tr>')

    tables = ''
    if gap_rows:
        tables += (f'<h2><span class="pill gap">Real gaps</span> — worth a closer look</h2>'
                   f'<table class="gaptable"><tr><th>#</th><th>Topic</th><th>What\'s going on</th></tr>{gap_rows}</table>')
    if careless_rows:
        tables += (f'<h2><span class="pill careless">Not a gap</span></h2>'
                   f'<table class="gaptable"><tr><th>#</th><th>Topic</th><th>What\'s going on</th></tr>{careless_rows}</table>')
    if uncertain_rows:
        tables += (f'<h2>Uncertain / needs follow-up</h2>'
                   f'<table class="gaptable"><tr><th>#</th><th>Topic</th><th>What\'s going on</th></tr>{uncertain_rows}</table>')
    if slow_rows:
        tables += (f'<h2><span class="pill slow">Took a long time</span> — {slow_threshold_sec}s or more, right or wrong</h2>'
                   f'<table class="gaptable"><tr><th>#</th><th>Topic</th><th>Time</th><th>Result</th></tr>{slow_rows}</table>')
    if changed_rows:
        tables += (f'<h2><span class="pill changed">Changed her answer</span> — picked more than once, whatever it netted out to</h2>'
                   f'<table class="gaptable"><tr><th>#</th><th>Topic</th><th>Picks</th><th>×changed</th><th>Result</th><th></th></tr>{changed_rows}</table>')

    jumplist_links = ' '.join(f'<a href="#q{n}">#{n}</a>' for n in wrong)
    slow_jumplist_links = ' '.join(f'<a href="#q{n}">#{n}</a>' for n in slow_nums)
    changed_jumplist_links = ' '.join(f'<a href="#q{n}">#{n}</a>' for n in changed_nums)

    cards = []
    for n in range(1, n_total + 1):
        p = problems[n]
        r = rows_data.get(n)
        is_wrong = n in wrong
        is_blank = n in grading['blank']
        badge = 'blank' if is_blank else ('wrong' if is_wrong else 'right')
        card_cls = f'card {badge}'
        change_badge = ''
        if is_blank:
            meta = 'Left blank'
            final = None
        else:
            untimed = r.get('seconds', '').strip() == ''
            meta = 'Answered on paper after the digital timer — not individually timed' if untimed else f'{float(r["seconds"]):.1f}s on this problem'
            c = changes.get(n)
            if c:
                meta += f' · picked {" → ".join(c["picks"])} ({c["n_changes"]}×changed)'
                if c['had_correct_then_left']:
                    change_badge = '<span class="chg chg-bad">had it right, changed away</span>'
                elif c['self_corrected']:
                    change_badge = '<span class="chg chg-good">self-corrected</span>'
                elif n in grading['wrong_to_wrong']:
                    change_badge = '<span class="chg chg-neutral">still wrong</span>'
            elif r['first_answer'] != r['final_answer']:
                meta += f' · first picked {r["first_answer"]}, changed to {r["final_answer"]}'
                if n in grading['wrong_to_right']:
                    change_badge = '<span class="chg chg-good">self-corrected</span>'
                elif n in grading['right_to_wrong']:
                    change_badge = '<span class="chg chg-bad">flipped to wrong</span>'
                elif n in grading['wrong_to_wrong']:
                    change_badge = '<span class="chg chg-neutral">still wrong</span>'
            final = r['final_answer']
        backlinks = []
        if is_wrong:
            next_wrong = wrong[(wrong.index(n) + 1) % len(wrong)]
            backlinks.append(f'<a class="backlink" href="#q{next_wrong}">next missed →</a>')
        if n in slow_nums:
            next_slow = slow_nums[(slow_nums.index(n) + 1) % len(slow_nums)]
            backlinks.append(f'<a class="backlink slow" href="#q{next_slow}">next slow →</a>')
        if n in changed_nums:
            next_changed = changed_nums[(changed_nums.index(n) + 1) % len(changed_nums)]
            backlinks.append(f'<a class="backlink changed" href="#q{next_changed}">next changed →</a>')
        backlink = ''.join(backlinks)
        slow_badge = '<span class="badge slow">⏱ Slow</span>' if n in slow_nums else ''
        changed_badge = '<span class="badge changed">⟲ Changed</span>' if n in changes else ''
        card = (f'<div class="{card_cls}" id="q{n}">'
                f'<div class="row1"><span class="num">#{n} · {p["topic"]} · {p["tier"]}</span>'
                f'<span class="row1-right">{backlink}{slow_badge}{changed_badge}<span class="badge {badge}">{badge.capitalize()}</span></span></div>'
                f'<div class="meta">{meta}{" " + change_badge if change_badge else ""}</div>'
                f'<div class="q">{p["q"]}</div>{p["diag"]}'
                f'<div class="choices">{_choices_html(p, final)}</div>'
                f'<div class="why"><b>Why {p["ans"]} is correct:</b> {p["why"]}</div>')
        if n in flagged:
            card += (f'<div class="note gap"><b>⚠ Automated check flagged this problem</b>'
                     f'{flagged[n]} Review by hand before trusting this card.</div>')
        if is_wrong and n in notes:
            note = notes[n]
            card += f'<div class="note {note["kind"] if note["kind"]!="uncertain" else "careless"}"><b>Parent\'s note — {note["title"]}</b>{note["body"]}</div>'
        elif is_wrong:
            card += '<div class="note careless"><b>⚠ NEEDS DIAGNOSIS</b>This wrong answer has not been reviewed yet.</div>'
        card += '</div>'
        cards.append(card)

    summary = (f'<h1>{title} — What Hannah Got Wrong</h1>'
               f'<p class="lede">{n_total} problems, graded against the exact worksheet she took '
               f'(pulled from its published commit, not the live file). {grading["total_minutes"]} minutes elapsed.</p>'
               f'<div class="summary">'
               f'<div class="stat right"><b>{grading["n_correct"]}</b><span>Correct</span></div>'
               f'<div class="stat wrong"><b>{len(wrong)}</b><span>Wrong</span></div>'
               f'<div class="stat blank"><b>{len(grading["blank"])}</b><span>Blank</span></div>'
               f'<div class="stat slow"><b>{len(slow_nums)}</b><span>Took long ({slow_threshold_sec}s+)</span></div>'
               f'<div class="stat changed"><b>{len(changed_nums)}</b><span>Changed answer</span></div>'
               f'<div class="stat"><b>{grading["n_correct"]}/{n_total}</b><span>Score</span></div>'
               f'</div>')
    if missing_notes:
        summary += (f'<p class="lede" style="color:var(--wrong);font-weight:600;">'
                    f'⚠ {len(missing_notes)} wrong problem(s) have no diagnosis yet: {missing_notes}. '
                    f'This review is incomplete.</p>')

    jumplists = f'<div class="jumplist" id="wronglist">Jump to a missed problem: {jumplist_links}</div>' if jumplist_links else ''
    jumplists += f'<div class="jumplist slow" id="slowlist">Jump to a slow problem: {slow_jumplist_links}</div>' if slow_jumplist_links else ''
    jumplists += f'<div class="jumplist changed" id="changedlist">Jump to a changed-answer problem: {changed_jumplist_links}</div>' if changed_jumplist_links else ''

    body = summary + tables + jumplists + ''.join(cards)

    css = _CSS or _DEFAULT_CSS
    full = f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Review</title><style>{css}</style></head><body><div class="wrap">{body}</div></body></html>'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, 'w').write(full)
    return out_path, missing_notes


_DEFAULT_CSS = '''
:root{--bg:#F3F1EC;--surface:#FFFFFF;--surface-alt:#EDEAE2;--ink:#2A2521;--ink-muted:#6B6358;--border:#DAD4C8;
--accent:#8A5A3B;--accent-ink:#6B4428;--accent-soft:#F1E3D6;--right:#2E7D5B;--right-soft:#E3F1EA;--wrong:#B5452E;--wrong-soft:#FBE7E1;--blank:#9A6B1F;--blank-soft:#FBF0DD;
--gap:#7A3B8C;--gap-soft:#F1E3F5;--careless:#2E6B8C;--careless-soft:#E3EEF5;--slow:#1E7A8C;--slow-soft:#E1F1F5;--changed:#9B5A1E;--changed-soft:#F5E8D8;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1C1815;--surface:#262220;--surface-alt:#2E2925;--ink:#EDE7DF;--ink-muted:#AFA596;--border:#3B352F;
--accent:#D79A6E;--accent-ink:#E8B98F;--accent-soft:rgba(215,154,110,0.14);--right:#6FCBA0;--right-soft:rgba(111,203,160,0.12);--wrong:#E58A74;--wrong-soft:rgba(229,138,116,0.14);--blank:#E0B45A;--blank-soft:rgba(224,180,90,0.14);
--gap:#C98FDA;--gap-soft:rgba(201,143,218,0.14);--careless:#7FB8E0;--careless-soft:rgba(127,184,224,0.14);--slow:#5EC8DD;--slow-soft:rgba(94,200,221,0.14);--changed:#E0A95E;--changed-soft:rgba(224,169,94,0.14);color-scheme:dark;}}
:root[data-theme="dark"]{--bg:#1C1815;--surface:#262220;--surface-alt:#2E2925;--ink:#EDE7DF;--ink-muted:#AFA596;--border:#3B352F;
--accent:#D79A6E;--accent-ink:#E8B98F;--accent-soft:rgba(215,154,110,0.14);--right:#6FCBA0;--right-soft:rgba(111,203,160,0.12);--wrong:#E58A74;--wrong-soft:rgba(229,138,116,0.14);--blank:#E0B45A;--blank-soft:rgba(224,180,90,0.14);
--gap:#C98FDA;--gap-soft:rgba(201,143,218,0.14);--careless:#7FB8E0;--careless-soft:rgba(127,184,224,0.14);--slow:#5EC8DD;--slow-soft:rgba(94,200,221,0.14);--changed:#E0A95E;--changed-soft:rgba(224,169,94,0.14);color-scheme:dark;}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Iowan Old Style","Palatino",Georgia,serif;line-height:1.5;}
.wrap{max-width:860px;margin:0 auto;padding:28px 18px 64px;}
h1{font-size:1.7rem;margin:0 0 4px;}
h2{font-size:1.2rem;margin:28px 0 10px;font-family:system-ui,sans-serif;}
.lede{color:var(--ink-muted);margin:0 0 20px;font-family:system-ui,sans-serif;font-size:0.95rem;}
.summary{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:22px;font-family:system-ui,sans-serif;}
.stat{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 16px;min-width:110px;}
.stat b{display:block;font-size:1.5rem;font-variant-numeric:tabular-nums;}
.stat.right b{color:var(--right);} .stat.wrong b{color:var(--wrong);} .stat.blank b{color:var(--blank);} .stat.slow b{color:var(--slow);} .stat.changed b{color:var(--changed);}
.stat span{font-size:0.78rem;color:var(--ink-muted);text-transform:uppercase;letter-spacing:0.04em;}
.jumplist{font-family:system-ui,sans-serif;font-size:0.9rem;margin-bottom:10px;color:var(--ink-muted);}
.jumplist a{color:var(--wrong);text-decoration:none;font-weight:600;margin-right:4px;}
.jumplist.slow a{color:var(--slow);}
.jumplist.changed a{color:var(--changed);}
.gaptable{width:100%;border-collapse:collapse;font-family:system-ui,sans-serif;font-size:0.88rem;margin-bottom:10px;}
.gaptable th,.gaptable td{border:1px solid var(--border);padding:7px 10px;text-align:left;vertical-align:top;}
.gaptable th{background:var(--surface-alt);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.03em;color:var(--ink-muted);}
.gaptable td.wrong{color:var(--wrong);font-weight:700;text-transform:capitalize;}
.gaptable td.right{color:var(--right);font-weight:700;text-transform:capitalize;}
.pill{display:inline-block;font-size:0.72rem;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap;}
.pill.gap{background:var(--gap-soft);color:var(--gap);}
.pill.careless{background:var(--careless-soft);color:var(--careless);}
.pill.slow{background:var(--slow-soft);color:var(--slow);}
.pill.changed{background:var(--changed-soft);color:var(--changed);}
.pill.self-corrected{background:var(--right-soft);color:var(--right);}
.pill.left-correct{background:var(--wrong-soft);color:var(--wrong);}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin:0 0 14px;scroll-margin-top:12px;}
.card.wrong{border-color:var(--wrong);box-shadow:inset 3px 0 0 var(--wrong);}
.card.blank{border-color:var(--blank);box-shadow:inset 3px 0 0 var(--blank);}
.card.right{box-shadow:inset 3px 0 0 var(--right);}
.row1{display:flex;justify-content:space-between;align-items:baseline;gap:10px;font-family:system-ui,sans-serif;}
.num{font-weight:700;color:var(--ink-muted);}
.badge{font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;padding:2px 9px;border-radius:999px;}
.badge.right{background:var(--right-soft);color:var(--right);}
.badge.wrong{background:var(--wrong-soft);color:var(--wrong);}
.badge.blank{background:var(--blank-soft);color:var(--blank);}
.badge.slow{background:var(--slow-soft);color:var(--slow);}
.badge.changed{background:var(--changed-soft);color:var(--changed);}
.meta{font-family:system-ui,sans-serif;font-size:0.78rem;color:var(--ink-muted);}
.chg{font-size:0.78rem;margin-left:4px;}
.chg::before{content:"· ";}
.chg-good{color:var(--right);}
.chg-bad{color:var(--wrong);}
.chg-neutral{color:var(--ink-muted);}
.row1-right{display:flex;align-items:baseline;gap:10px;}
.backlink{font-size:0.75rem;color:var(--ink-muted);text-decoration:none;margin-left:10px;}
.backlink:first-child{margin-left:0;}
.backlink:hover{text-decoration:underline;}
.backlink.slow{color:var(--slow);}
.backlink.changed{color:var(--changed);}
.q{margin:8px 0 10px;font-size:1.05rem;}
.diag{margin:8px 0 12px;}
table.data{border-collapse:collapse;font-size:0.85rem;font-family:system-ui,sans-serif;}
table.data th,table.data td{border:1px solid var(--border);padding:3px 8px;text-align:left;}
.choices{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin-bottom:8px;font-family:system-ui,sans-serif;font-size:0.95rem;}
.choice{padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface-alt);}
.choice.correct{border-color:var(--right);background:var(--right-soft);font-weight:700;}
.choice.herpick{outline:2px solid var(--wrong);outline-offset:-1px;}
.choice .tag{font-size:0.7rem;font-weight:700;margin-left:6px;}
.choice .tag.c{color:var(--right);} .choice .tag.h{color:var(--wrong);}
.why{font-family:system-ui,sans-serif;font-size:0.85rem;color:var(--ink-muted);border-left:3px solid var(--accent);padding:4px 10px;margin-top:4px;}
.note{font-family:system-ui,sans-serif;font-size:0.85rem;margin-top:8px;padding:8px 10px;border-radius:8px;}
.note.gap{background:var(--gap-soft);border-left:3px solid var(--gap);}
.note.careless{background:var(--careless-soft);border-left:3px solid var(--careless);}
.note b{display:block;margin-bottom:2px;}
.frac{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1;font-size:0.82em;margin:0 1px;}
.frac .n{border-bottom:2px solid currentColor;padding:0 3px 2px;}
.frac .d{padding:2px 3px 0;}
.colsum{display:inline-block;text-align:right;font-variant-numeric:tabular-nums;font-family:system-ui,sans-serif;}
.colsum div{padding:1px 4px;}
.colsum .total{border-top:2px solid currentColor;margin-top:2px;}
@media (max-width:480px){.choices{grid-template-columns:1fr;}}
'''


# ---------- 5. Update practice-log.json and student-tracker.json ----------

def update_tracker_and_log(kind, set_no, problems, grading, notes, date_str):
    log, key, target = _set_entry(kind, set_no)
    gkey = f'graded_{date_str}'
    target[gkey] = dict(
        score=f'{grading["n_correct"]}/{grading["n_total"]}',
        wrong=grading['wrong'], blank=grading['blank'],
        total_elapsed_minutes=grading['total_minutes'],
        first_then_changed=dict(
            wrong_to_right=grading['wrong_to_right'],
            wrong_to_wrong=grading['wrong_to_wrong'],
            right_to_wrong=grading['right_to_wrong'],
        ),
        notes_summary={str(n): notes[n]['title'] for n in grading['wrong'] if n in notes},
    )
    json.dump(log, open(LOG_PATH, 'w'), indent=1)

    tracker = json.load(open(TRACKER_PATH))
    by_topic = {}
    for n in range(1, grading['n_total'] + 1):
        if n in grading['blank']:
            continue
        topic = problems[n]['topic']
        by_topic.setdefault(topic, dict(wrong=0, graded=0, tier=problems[n]['tier'], sec_total=0.0, sec_n=0))
        by_topic[topic]['graded'] += 1
        if n in grading['wrong']:
            by_topic[topic]['wrong'] += 1
        r = grading['rows'].get(n)
        if r is not None and r.get('seconds', '').strip() != '':
            by_topic[topic]['sec_total'] += float(r['seconds'])
            by_topic[topic]['sec_n'] += 1
    existing = {x['topic']: x for x in tracker['topics']}
    for topic, d in by_topic.items():
        if topic in existing:
            e = existing[topic]
            e['wrong'] = (e.get('wrong') or 0) + d['wrong']
            e['graded'] = (e.get('graded') or 0) + d['graded']
            # avg_seconds is a running average across every graded set, tracked via
            # hidden accumulator fields (_sec_total/_sec_n) so a slow or fast set
            # doesn't overwrite history -- see plan_set.py's SLOW_SECONDS bonus.
            e['_sec_total'] = (e.get('_sec_total') or 0.0) + d['sec_total']
            e['_sec_n'] = (e.get('_sec_n') or 0) + d['sec_n']
            if e['_sec_n']:
                e['avg_seconds'] = round(e['_sec_total'] / e['_sec_n'], 1)
        else:
            entry = dict(
                topic=topic, tier=d['tier'], wrong=d['wrong'], graded=d['graded'],
                habits=[], priority='unknown',
                real_tests_note=f'not yet cross-checked against official-test tagging as of {date_str}',
            )
            if d['sec_n']:
                entry['_sec_total'] = d['sec_total']
                entry['_sec_n'] = d['sec_n']
                entry['avg_seconds'] = round(d['sec_total'] / d['sec_n'], 1)
            tracker['topics'].append(entry)
    tracker['updated'] = date_str
    json.dump(tracker, open(TRACKER_PATH, 'w'), indent=1)
