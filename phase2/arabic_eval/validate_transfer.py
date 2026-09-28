import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
load=lambda n:json.loads((P/n).read_text())
ledger=[json.loads(x) for x in (P/'PROVENANCE_LEDGER.jsonl').read_text().splitlines()]
targets=[json.loads(x) for x in (P/'DEVELOPMENT_TARGETS.jsonl').read_text().splitlines()]
stress=[json.loads(x) for x in (P/'SCIENTIFIC_STRESS_CASES.jsonl').read_text().splitlines()]
original_stress=[json.loads(x) for x in (P/'SCIENTIFIC_STRESS_DEVELOPMENT.jsonl').read_text().splitlines()]
audit=load('SEALED_EXCLUSION_AUDIT.json');mapping=load('PASSAGE_TARGET_MAPPING.json');pins=load('INPUT_INTEGRITY.json')
assert len(ledger)==len(targets)==150 and len({x['case_id'] for x in targets})==150
assert len({x['target_id'] for x in targets})==150 and len({x['passage_id'] for x in targets})==len(mapping)==41
assert len(audit['excluded_passage_ids'])==audit['count']==59
assert not {x['passage_id'] for x in targets}&set(audit['excluded_passage_ids'])
assert len(stress)==len(original_stress)==12 and all(x['human_gold_status']=='NON_HUMAN_GOLD' for x in stress)
assert all('human_gold_status' not in x for x in original_stress)
assert all(x['passage_id'] and x['target_id'] and x['publication_source'] and x['source_url'] and x['license_or_usage_basis'] for x in targets)
for a,b in zip(ledger,targets):
 assert {k:v for k,v in b.items() if k!='target_id'}==a
 assert b['source'][b['target_start']:b['target_end']]==b['target_error']
 assert b['reference']==b['source'][:b['target_start']]+b['target_correction']+b['source'][b['target_end']:]
for x in mapping:
 actual=[r for r in targets if r['passage_id']==x['passage_id']]
 assert x['source']==actual[0]['source'] and set(x['target_ids'])=={r['target_id'] for r in actual}
for name,expected in pins.items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==expected
assert all(p.suffix not in ('.bin','.pt','.pth','.safetensors','.onnx') for p in P.rglob('*') if p.is_file())
assert all('sealed' not in p.name.lower() or p.name in ('SEALED_EXCLUSION_AUDIT.json','SEALED_RESULTS.json') for p in P.iterdir() if p.is_file())
print(json.dumps({'status':'PASS','targets':150,'unique_passages':41,'scientific_stress_cases':12,'sealed_ids_excluded':59,'weights_committed':False,'sealed_material_committed':False}))
