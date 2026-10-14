"""Genera js/data/lang-zh-names.js: nombre del juego -> nombre oficial en chino tradicional.

  python tools/make_lang_zh_names.py ruta/a/pokemon_species_names.csv

El CSV es el de PokeAPI (data/v2/csv/pokemon_species_names.csv); idioma 4 = zh-Hant.
Se cruza por número de Pokédex con js/data/pokedex.js.
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
csv_path = Path(sys.argv[1])

zh = {}
with csv_path.open(encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['local_language_id'] == '4':
            zh[int(row['pokemon_species_id'])] = row['name']

dex_src = (ROOT / 'js/data/pokedex.js').read_text(encoding='utf-8')
out = {}
for m in re.finditer(r'\{"dex":(\d+),"name":"((?:[^"\\]|\\.)*)"', dex_src):
    d, name = int(m.group(1)), json.loads('"' + m.group(2) + '"')
    if d in zh and zh[d] != name:
        out[name] = zh[d]

body = ',\n'.join(f'  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}' for k, v in out.items())
(ROOT / 'js/data/lang-zh-names.js').write_text(
    '/* ============ lang-zh-names.js — GENERADO por tools/make_lang_zh_names.py ============\n'
    ' * Nombres de los Pokémon en chino tradicional (PokeAPI, idioma 4). */\n'
    "G.I18n.add({\n" + body + "\n}, 'zh');\n", encoding='utf-8')
print(f'ok: {len(out)} nombres')
