import json
import re
from pathlib import Path

fp = Path(r"c:\Users\Alejandro López\Documents\AppBuilderTest\AppBuilder-Certificate\questions.json")
text = fp.read_text(encoding='utf-8')

data = json.loads(text)

count = 0
changes = []

for q in data:
    orig = q.get('explanation')
    if not isinstance(orig, str):
        continue
    new = re.sub(r"\[cite:.*?\]", "", orig)
    new = re.sub(r"\s+", " ", new).strip()
    new = new.replace('are standardly used', 'are used')
    new = new.replace('are configured within the App Manager', 'are configured in the App Manager')
    new = new.replace('Prerequisites for Campaign Members include existing records and formatted CSV data.', 'Prerequisites for Campaign Members include existing records and properly formatted CSV data.')
    if new and not new.endswith('.'):
        new = new + '.'
    if new != orig:
        q['explanation'] = new
        count += 1
        changes.append({'id': q.get('id'), 'before': orig, 'after': new})

fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"Updated {count} explanations.")
if changes:
    for c in changes[:10]:
        print(f"id {c['id']}: \n  BEFORE: {c['before']}\n  AFTER:  {c['after']}\n")

# Quick leftover check
full = fp.read_text(encoding='utf-8')
leftover = full.count('[cite:')
print('Leftover [cite: occurrences:', leftover)