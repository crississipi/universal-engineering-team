#!/usr/bin/env python3
"""Report skill sizes; exact token counts require optional tiktoken."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]; files=sorted((ROOT/'skills').glob('*/SKILL.md'))
try:
 import tiktoken; enc=tiktoken.get_encoding('cl100k_base'); exact=True
except ImportError: enc=None; exact=False
print('Skill size report'); print('Method:', 'tiktoken cl100k_base' if exact else 'rough estimate (words + punctuation)'); print('-'*72)
total=0
for f in files:
 s=f.read_text(encoding='utf-8'); n=len(enc.encode(s)) if exact else len(re.findall(r'\w+|[^\w\s]',s)); total+=n; print(f'{f.parent.name:42} {n:6}')
print('-'*72); print(f'{"TOTAL":42} {total:6}')
if not exact: print('For a tokenizer-based estimate: python -m pip install tiktoken')
print('Counts are monitoring signals only; do not remove necessary instructions to reduce them.')
