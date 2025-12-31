import json
from pathlib import Path

files = [Path('c:/Users/Alejandro López/Documents/AppBuilderTest/AppBuilder-Certificate/questions.json')]
files += list(Path('c:/Users/Alejandro López/Documents/AppBuilderTest/AppBuilder-Certificate/Official-Exams').glob('*.json'))

report = {}
for f in files:
    data = json.loads(f.read_text(encoding='utf-8'))
    total = len(data)
    empty = sum(1 for q in data if not q.get('explanation'))
    not_end_period = sum(1 for q in data if isinstance(q.get('explanation'), str) and not q.get('explanation').strip().endswith('.'))
    leftover_cite = sum(1 for q in data if isinstance(q.get('explanation'), str) and '[cite:' in q.get('explanation'))
    report[str(f.name)] = {'total': total, 'empty_explanations': empty, 'not_ending_period': not_end_period, 'leftover_cite': leftover_cite}

print('Validation report:')
for k,v in report.items():
    print(k, v)

# Exit with non-zero code if issues found
issues = any(v['empty_explanations']>0 or v['leftover_cite']>0 for v in report.values())
if issues:
    raise SystemExit(1)
else:
    print('All checks passed.')