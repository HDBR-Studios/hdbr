#!/usr/bin/env python3
"""Remove o radar chart + painel de números dos SVGs do github-profile-3d-contrib,
deixando só as barras 3D do calendário. Roda como pós-step do workflow (idempotente)."""
import sys, re

def remove_group_at(svg, start):
    """Remove o grupo <g...> que ABRE em `start`, balanceando <g>/</g> aninhados."""
    i = svg.index('>', start) + 1
    depth = 1
    while depth > 0 and i < len(svg):
        ng = svg.find('<g', i); ngc = svg.find('</g>', i)
        if ngc == -1: break
        if ng != -1 and ng < ngc:
            depth += 1; i = ng + 2
        else:
            depth -= 1; i = ngc + 4
    return svg[:start] + svg[i:]

def clean(svg):
    # 1) Radar: o <g ...> que envolve o <polygon class="radar"> (acha o polygon, anda pra trás até o <g de abertura do wrapper)
    pr = svg.find('class="radar"')
    if pr != -1:
        # wrapper = último '<g transform="translate(' antes do polygon que contém os 'class="axis"'
        gopen = svg.rfind('<g transform="translate(', 0, svg.rfind('class="axis"', 0, pr) if svg.rfind('class="axis"',0,pr)!=-1 else pr)
        if gopen != -1:
            svg = remove_group_at(svg, gopen)
    # 2) Painel de texto (totais + data): o <g> SEM atributos que contém '>contributions</text>'
    pc = svg.find('>contributions</text>')
    if pc != -1:
        gopen = svg.rfind('<g>', 0, pc)
        if gopen != -1:
            svg = remove_group_at(svg, gopen)
    return svg

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    out = clean(s)
    open(path, 'w', encoding='utf-8').write(out)
    print(f"{path}: {len(s)} -> {len(out)} bytes")
