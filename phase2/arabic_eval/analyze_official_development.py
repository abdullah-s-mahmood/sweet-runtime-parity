"""Development-only targeted correction and collateral edit diagnostics.
Never treats one-target references as fully corrected paragraphs.
"""
import argparse,json,difflib,collections,random
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CATEGORIES=['SUPPORTED_CORRECTION','ACCEPTABLE_ALTERNATIVE','UNNECESSARY_EDIT','INCORRECT_EDIT','REVIEW_REQUIRED']
def score_target(row,output):
 source=row['source'];ref=row['reference'];a=row['target_start'];b=a+len(row['target_correction'])
 if source[a:row['target_end']]!=row['target_error'] or ref[a:b]!=row['target_correction']:raise ValueError(('bad target span',row['case_id']))
 equal=difflib.SequenceMatcher(None,ref,output,autojunk=False).get_matching_blocks()
 # Conservative alignment: require target and adjacent context to match in one block.
 left=min(3,a);right=min(3,len(ref)-b)
 if any(m.a<=a-left and m.a+m.size>=b+right for m in equal):return 'RECOVERED_ALIGNED'
 if output==source:return 'NOT_RECOVERED'
 return 'REVIEW_REQUIRED_ALIGNMENT'
def collateral(row,output):
 ref=row['reference'];a=row['target_start'];b=a+len(row['target_correction']);edits=[]
 for tag,i,j,k,l in difflib.SequenceMatcher(None,ref,output,autojunk=False).get_opcodes():
  if tag=='equal':continue
  outside=j<=a or i>=b
  edits.append({'reference_span':[i,j],'output_span':[k,l],'reference_text':ref[i:j],'output_text':output[k:l],'outside_published_target':outside,'category':'REVIEW_REQUIRED','permitted_categories':CATEGORIES})
 return edits

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=ROOT/'artifacts/OFFICIAL_DEVELOPMENT_RAW.jsonl');ap.add_argument('--output',type=Path,default=ROOT/'artifacts/TARGETED_AND_COLLATERAL_DIAGNOSTICS.json');ap.add_argument('--bootstrap',action='store_true');args=ap.parse_args()
 rows=[json.loads(x) for x in args.raw.read_text().splitlines() if x.strip()]
 assert len(rows)==150 and len({x['passage_id'] for x in rows})==41
 stages={'nopnx_iteration_1':lambda r:r['nopnx_iteration_1']['output'],'nopnx_iteration_2':lambda r:r['nopnx_iteration_2']['output'],'pnx_only':lambda r:r['pnx_only']['output'],'full':lambda r:r['full_pnx_iteration_1']['output']}
 results=[]
 for row in rows:
  item={'case_id':row['case_id'],'target_id':row['target_id'],'passage_id':row['passage_id'],'target_location':[row['target_start'],row['target_end']],'stages':{}}
  for name,get in stages.items():
   out=get(row);item['stages'][name]={'targeted_correction_recovery':score_target(row,out),'collateral_edits':collateral(row,out)}
  results.append(item)
 summary={}
 for name in stages:
  states=collections.Counter(x['stages'][name]['targeted_correction_recovery'] for x in results)
  # Passage-level output is repeated for multiple annotated targets. Do not count collateral instances as independent.
  distinct={(x['passage_id'],json.dumps(x['stages'][name]['collateral_edits'],ensure_ascii=False,sort_keys=True)) for x in results}
  summary[name]={'target_states':dict(states),'unique_passages':41,'collateral_annotation_required':True,'collateral_categories_not_automatically_assigned':True,'distinct_passage_target_contexts_with_collateral':sum('"outside_published_target": true' in d for _,d in distinct)}
 out={'status':'DEVELOPMENT_DIAGNOSTIC_NOT_HUMAN_ADJUDICATION','primary_metric':'TARGETED_CORRECTION_RECOVERY','cluster_unit':'passage_id','n_targets':150,'n_passages':41,'summary':summary,'cases':results,'collateral_category_contract':CATEGORIES}
 if args.bootstrap:
  groups=collections.defaultdict(list)
  for x in results:groups[x['passage_id']].append(x)
  ids=sorted(groups);rng=random.Random(20260928);vals=[]
  for _ in range(2000):
   sample=[x for pid in rng.choices(ids,k=len(ids)) for x in groups[pid]]
   vals.append(sum(x['stages']['full']['targeted_correction_recovery']=='RECOVERED_ALIGNED' for x in sample)/len(sample))
  vals.sort();out['full_cluster_bootstrap_95pct']=[vals[49],vals[1949]]
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'targets':150,'passages':41,'summary':summary},ensure_ascii=False))
if __name__=='__main__':main()
