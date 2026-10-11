"""
Stamps the current git commit hash into practice-log.json as the "as-published"
snapshot for a set -- run this the moment a set's worksheet files are finalized
and the link is handed to Hannah to take, before any further edits.

Why this exists: grading/review tooling must reconstruct exactly what she saw,
regardless of any bug fixes made to the live worksheet after she took it (like
speed-set-3 #37's diagram). Without a recorded commit, reconstructing "what was
actually live" means manually digging through git log by hand (error-prone --
this is exactly what had to be done after-the-fact for set 3).

Usage: python3 mark_published.py qr 3
       python3 mark_published.py ma 2
"""
import json, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(HERE, '..', 'practice-log.json')

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('qr', 'ma'):
        print(__doc__)
        sys.exit(1)
    kind, set_no = sys.argv[1], int(sys.argv[2])
    key = 'sets' if kind == 'qr' else 'ma_sets'

    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=HERE).decode().strip()
    status = subprocess.check_output(['git', 'status', '--porcelain'], cwd=HERE).decode()
    if status.strip():
        print("WARNING: working tree has uncommitted changes. Commit and push first,")
        print("so the recorded hash actually matches what's live on GitHub Pages.")
        sys.exit(1)

    log = json.load(open(LOG_PATH))
    entries = log.get(key, [])
    target = next((e for e in entries if e.get('set_no') == set_no), None)
    if target is None:
        print(f"No entry with set_no={set_no} in '{key}'. Add the set's topics/build entry first.")
        sys.exit(1)

    target['published_commit'] = commit
    json.dump(log, open(LOG_PATH, 'w'), indent=1)
    print(f"Stamped {key}[set_no={set_no}].published_commit = {commit}")

if __name__ == '__main__':
    main()
