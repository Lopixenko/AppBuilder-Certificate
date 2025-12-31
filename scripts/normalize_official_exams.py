import json
import re
from pathlib import Path

folder = Path(r"c:/Users/Alejandro López/Documents/AppBuilderTest/AppBuilder-Certificate/Official-Exams")
files = list(folder.glob('*.json'))

summary = []
for f in files:
    text = f.read_text(encoding='utf-8')
    data = json.loads(text)
    changed = 0
    for q in data:
        orig = q.get('explanation')
        if not isinstance(orig, str):
            continue
        new = re.sub(r"\[cite:.*?\]", "", orig)
        new = re.sub(r"\s+", " ", new).strip()
        if new and not new.endswith('.'):
            new = new + '.'
        if new != orig:
            q['explanation'] = new
            changed += 1
    if changed > 0:
        # create a simple backup
        bak = f.with_suffix('.json.bak')
        if not bak.exists():
            bak.write_text(text, encoding='utf-8')
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    summary.append({'file': str(f.name), 'changed': changed})

print('Processed', len(files), 'files')
for s in summary:
    print(s['file'], '- explanations changed:', s['changed'])

# quick leftover check
all_text = ''
for f in files:
    all_text += f.read_text(encoding='utf-8')
leftover = all_text.count('[cite:')
print('Leftover [cite: occurrences in Official-Exams:', leftover)