#!/usr/bin/env python3
"""Validate Agent Skill metadata, role index targets, and local Markdown links."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]; SKILLS=ROOT/'skills'; errors=[]; warnings=[]
def parse(path):
 text=path.read_text(encoding='utf-8')
 if not text.startswith('---\n'): errors.append(f'{path.relative_to(ROOT)}: missing YAML frontmatter opener'); return None
 end=text.find('\n---',4)
 if end<0: errors.append(f'{path.relative_to(ROOT)}: missing YAML frontmatter closer'); return None
 fields={}
 for line in text[4:end].splitlines():
  if ':' in line and not line.lstrip().startswith('#'):
   k,v=line.split(':',1); fields[k.strip()]=v.strip().strip('"').strip("'")
 for k in ('name','description'):
  if not fields.get(k): errors.append(f'{path.relative_to(ROOT)}: missing required {k!r}')
 return fields
files=sorted(SKILLS.glob('*/SKILL.md'))
if not files: errors.append('No skills found under skills/*/SKILL.md')
names={}
for f in files:
 fields=parse(f)
 if not fields: continue
 n=fields.get('name','')
 if n!=f.parent.name: errors.append(f'{f.relative_to(ROOT)}: name {n!r} does not match folder {f.parent.name!r}')
 if n in names: errors.append(f'Duplicate skill name {n!r}: {names[n]} and {f}')
 names[n]=f
 wc=len(fields.get('description','').split())
 if wc>18: warnings.append(f'{f.relative_to(ROOT)}: description has {wc} words (target <= 18)')
idx=ROOT/'ROLE-INDEX.md'
if not idx.exists(): errors.append('Missing ROLE-INDEX.md')
else:
 links=set(re.findall(r'\]\((skills/[^)]+/SKILL\.md)\)',idx.read_text(encoding='utf-8')))
 expected={f.relative_to(ROOT).as_posix() for f in files}
 for x in sorted(expected-links): errors.append(f'ROLE-INDEX.md: missing skill link {x}')
 for x in sorted(links-expected): errors.append(f'ROLE-INDEX.md: invalid skill link {x}')
link_re=re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
for md in ROOT.rglob('*.md'):
 if any(x in {'.git','.venv','node_modules'} for x in md.parts): continue
 for raw in link_re.findall(md.read_text(encoding='utf-8',errors='replace')):
  target=raw.strip().split()[0].strip('<>')
  if not target or target.startswith(('http://','https://','mailto:','#','data:')): continue
  target=target.split('#',1)[0]
  if not target: continue
  cand=(md.parent/target).resolve()
  try: cand.relative_to(ROOT.resolve())
  except ValueError: errors.append(f'{md.relative_to(ROOT)}: link escapes repository: {raw}'); continue
  if not cand.exists(): errors.append(f'{md.relative_to(ROOT)}: broken local link: {raw}')
for x in warnings: print('WARNING:',x)
for x in errors: print('ERROR:',x)
if errors: print(f'\nValidation failed: {len(errors)} error(s), {len(warnings)} warning(s).'); sys.exit(1)
print(f'Validation passed: {len(files)} skills, unique metadata, role index and local Markdown links checked.')
if warnings: print(f'{len(warnings)} warning(s) require review.')
