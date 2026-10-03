from pathlib import Path
import sys,json,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from at0_core import EnglishAdapter, StubAdapter, cp_to_utf8_byte, cp_to_utf16_units
checks=[]
def c(name,cond,detail=''):
    checks.append({'check':name,'status':'PASS' if cond else 'FAIL','detail':detail})

core=(ROOT/'src/at0_core.py').read_text(encoding='utf-8')
c('language adapter exists','class LanguageAdapter' in core)
c('unknown capability is explicit',EnglishAdapter().capability('morphology')=='NOT_IMPLEMENTED')
c('nonlinguistic stub differs',StubAdapter().word_count('abc def') != EnglishAdapter().word_count('abc def'))
c('unicode utf8 mapping',cp_to_utf8_byte('A😀B',2)==5)
c('unicode utf16 mapping',cp_to_utf16_units('A😀B',2)==3)
c('core no Arabic import','camel_tools' not in core and 'arabic' not in core.lower())
c('English counting is adapter-level','def english_word_count' in core and 'EnglishAdapter' in core)
c('no silent English fallback',"language_code=\"unknown\"" in core)
c('direction not hard-coded','rtl' not in core.lower() and 'ltr' not in core.lower())
c('model/detector logic absent from core','turnitin' not in core.lower() and 'openai' not in core.lower() and 'anthropic' not in core.lower())
out={'total':len(checks),'passed':sum(x['status']=='PASS' for x in checks),'failed':sum(x['status']=='FAIL' for x in checks),'checks':checks}
p=ROOT/'results/offline-preflight/portability_audit.json'; p.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
raise SystemExit(1 if out['failed'] else 0)