#!/usr/bin/env python3
"""Audit planning data against source evidence; does not prove in-game reachability."""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def audit(checklist):
    dex_text = (ROOT / 'include/constants/pokedex.h').read_text()
    expected = re.findall(r'NATIONAL_DEX_(\w+)', dex_text)[1:152]
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"\n]+)"\)',
                            (ROOT / 'src/data/text/species_names.h').read_text()))
    with checklist.open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    errors = []
    if len(rows) != 151 or [r['species'] for r in rows] != expected:
        errors.append('Checklist must contain exactly the National Dex #001–151, in order, once each.')
    if [r['number'] for r in rows] != [str(i) for i in range(1, 152)]:
        errors.append('National Dex numbering is missing, duplicated or out of order.')

    # Verify cited wild source evidence, including game version and encounter method.
    evidence = set()
    groups = json.loads((ROOT / 'src/data/wild_encounters.json').read_text())
    for group in groups['wild_encounter_groups']:
        for encounter in group.get('encounters', []):
            for method in ('land_mons', 'water_mons', 'fishing_mons', 'rock_smash_mons'):
                for mon in encounter.get(method, {}).get('mons', []):
                    evidence.add((mon['species'].removeprefix('SPECIES_'),
                                  encounter['base_label'] + ':' + method))
    evolution_pairs = set()
    source = (ROOT / 'src/data/pokemon/evolution.h').read_text()
    for parent, body in re.findall(r'\[SPECIES_(\w+)\]\s*=\s*(.*?)(?=\n\s*\[SPECIES_|\n};)', source, re.S):
        for child in re.findall(r'\{EVO_\w+,\s*\w+,\s*SPECIES_(\w+)\}', body):
            evolution_pairs.add((parent, child))
    by_species = {row['species']: row for row in rows}
    for row in rows:
        species = row['species']
        if names.get(species) != row['name']:
            errors.append(f'{species}: display name differs from source.')
        for field in ('planned_method_or_area', 'required_progression', 'choice_dependency', 'implementation', 'tested'):
            if not row[field].strip():
                errors.append(f'{species}: missing {field}.')
        if row['parent'] and (row['parent'], species) not in evolution_pairs:
            errors.append(f'{species}: evolution parent is not supported by source.')
        for citation in filter(None, row['baseline_wild_evidence'].split(';')):
            if (species, citation) not in evidence:
                errors.append(f'{species}: stale/wrong wild evidence: {citation}')
        visited = set()
        node = species
        while node:
            if node in visited:
                errors.append(f'{species}: cyclic acquisition dependency.')
                break
            visited.add(node)
            if node not in by_species:
                errors.append(f'{species}: parent {node} is outside the permitted 151-species roster.')
                break
            node = by_species[node]['parent']
    if errors:
        raise ValueError('\n'.join(errors))
    pending = sum(row['implementation'].startswith('PENDING') for row in rows)
    unrun = sum(row['tested'] == 'NOT RUN' for row in rows)
    print(f'PASS: {len(rows)} unique Kanto species; names, numbering, cited encounters and evolution dependencies checked.')
    print(f'Acquisition certification pending: {pending}; functional acquisition tests not run: {unrun}.')
    print('Planning audit only. Story flags, rewards, rates, stone budgets and finished-game roster restrictions are not validated.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checklist', type=Path, default=Path(__file__).with_name('pokedex.csv'))
    args = parser.parse_args()
    try:
        audit(args.checklist)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f'FAIL: {exc}\n')
