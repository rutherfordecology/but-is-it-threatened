"""
Build nzor_names.json — a local index of every name in NZOR.

For each of the ~170k names, stores the minimum needed for search + display:
  key  : lowercase normalised name  (JSON key)
  n    : display name (proper casing)
  id   : NZOR nameId (UUID)
  cls  : "v" if Vernacular Name, omitted for Scientific Name
  acc  : accepted/preferred scientific name (if this name is a synonym)
  sci  : linked scientific name (vernacular names only, from concepts.applications)
  sciId: nameId of the linked scientific name

Output: nzor_names.json  (same directory as this script)
"""

import urllib.request, json, time, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

BASE    = 'https://data.nzor.org.nz/v1'
OUT     = r'C:\Users\User\GBIF-Record-Finder\.claude\worktrees\objective-bose-704ec8\nzor_names.json'
PSIZE   = 1000   # max page size
DELAY   = 0.15   # seconds between requests (be polite)

def norm(s):
    if not s: return ''
    return re.sub(r'\s+', ' ', s.strip()).lower()

def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f'  retry {attempt+1} after error: {e}')
            time.sleep(2)

def linked_sci(name_obj):
    """Return (partialName, nameId) of first 'is vernacular for' application, or (None,None)."""
    for concept in name_obj.get('concepts') or []:
        for app in concept.get('applications') or []:
            if app.get('type') == 'is vernacular for':
                linked = app.get('concept', {}).get('name', {})
                if linked.get('partialName'):
                    return linked['partialName'], linked.get('nameId')
    return None, None

# ── Fetch first page to get total ────────────────────────────────────────────
print('Fetching page 1 to get total…')
first = fetch(f'{BASE}/names?pageSize={PSIZE}&page=1')
total = first['total']
pages = (total + PSIZE - 1) // PSIZE
print(f'Total names: {total:,}  |  Pages: {pages}')

lookup = {}   # norm(name) -> entry dict
seen   = set()

def process_page(names):
    for n in names:
        key = norm(n.get('partialName') or n.get('fullName') or '')
        if not key or key in seen:
            continue
        seen.add(key)

        is_vernac = n.get('class') == 'Vernacular Name'
        acc_name  = n.get('acceptedName') or {}
        is_syn    = acc_name.get('nameId') and acc_name['nameId'] != n['nameId']

        entry = {
            'n':  n.get('partialName') or n.get('fullName'),
            'id': n.get('nameId'),
        }
        if is_vernac:
            entry['cls'] = 'v'
            sci, sci_id = linked_sci(n)
            if sci:
                entry['sci']   = sci
                entry['sciId'] = sci_id
        elif is_syn:
            entry['acc']   = acc_name.get('partialName')
            entry['accId'] = acc_name.get('nameId')

        lookup[key] = entry

process_page(first.get('names', []))
print(f'  page 1/{pages} — {len(lookup):,} entries so far')

for page in range(2, pages + 1):
    time.sleep(DELAY)
    data = fetch(f'{BASE}/names?pageSize={PSIZE}&page={page}')
    process_page(data.get('names', []))
    if page % 10 == 0 or page == pages:
        print(f'  page {page}/{pages} — {len(lookup):,} entries so far')

print(f'\nTotal entries: {len(lookup):,}')
print(f'Writing {OUT}…')
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(lookup, f, ensure_ascii=False, separators=(',', ':'))

size_mb = os.path.getsize(OUT) / 1024 / 1024
print(f'Done. {size_mb:.1f} MB')
