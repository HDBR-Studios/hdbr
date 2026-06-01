#!/usr/bin/env python3
"""Popula contadores reais fixos no painel do github-profile-3d-contrib.
A API do GitHub não expõe commits/repos privados por tipo → fixamos manualmente.
Pós-step do workflow, idempotente. Mantém barras/total/streak dinâmicos."""
import sys, re

FIXED = {"Commits": "+12 000", "Repos": "+103"}  # estimativa commits + repos reais (contributedTo)

def populate(svg):
    for label, val in FIXED.items():
        # acha o <text>LABEL</text> e extrai o y; o valor é o <text x="330" y="MESMO_Y" ...>...</text>
        m = re.search(r'<text[^>]*y="([\d.]+)"[^>]*>' + re.escape(label) + r'</text>', svg)
        if not m:
            continue
        y = m.group(1)
        svg = re.sub(
            r'(<text[^>]*x="330"[^>]*y="' + re.escape(y) + r'"[^>]*>)[^<]*(</text>)',
            r'\g<1>' + val + r'\g<2>', svg)
    return svg

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    out = populate(s)
    open(path, 'w', encoding='utf-8').write(out)
    print(f"{path}: {'OK' if out != s else 'sem-mudança'}")
