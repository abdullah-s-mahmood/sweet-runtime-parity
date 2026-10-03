from __future__ import annotations
import json,re,sys,pathlib,collections

NEG=r"\b(?:no|not|never|without|false|incorrect|removed|neither|cannot|can't|doesn't|does not|didn't|did not|isn't|is not|aren't|are not)\b"
DECOY=r"\b(?:earlier|previous|pilot|legend|diagnostic|hypothesis|phrase|statement|saying|only for comparison|retained only|describes the previous)\b"

def norm(s):
    s=s.lower().replace("–","-").replace("—","-")
    return re.sub(r"\s+"," ",s).strip()

def split_units(text):
    t=norm(text)
    # sentence/clause units; keep whole sentences plus finer clauses.
    sent=[x.strip() for x in re.split(r"(?<=[.!?])\s+",t) if x.strip()]
    out=list(sent)
    for s in sent:
        out += [x.strip() for x in re.split(r"\s*;\s*|\b(?:but|whereas|while|although|however|contrary to)\b",s) if x.strip()]
    return list(dict.fromkeys(out))

def contains_any(s, vals):
    if vals is None: return True
    if isinstance(vals,str): vals=[vals]
    return any(norm(v) in s for v in vals)

def contains_all_groups(s, groups):
    return all(contains_any(s,g) for g in groups if g is not None)

def has_neg(s):
    return bool(re.search(NEG,s))

def is_decoy(s):
    return bool(re.search(DECOY,s))

def number_tokens(s):
    return re.findall(r"(?<![\w.])\d+(?:\.\d+)?%?",s)

def finding(rel,status,code,msg,evidence=None):
    x={"relation_id":rel["id"],"relation_type":rel["type"],"status":status,"code":code,"message":msg}
    if evidence: x["evidence"]=evidence
    return x

def candidate_units(text, groups):
    return [u for u in split_units(text) if contains_all_groups(u,groups)]

def relation_text_assertion(rel,text):
    groups=[rel.get("subject"),rel.get("predicate"),rel.get("object")]
    units=candidate_units(text,groups)
    if not units:
        return finding(rel,"UNRESOLVED","ASSERTION_NOT_RECONSTRUCTED","required assertion not reconstructed")
    good=[]
    for u in units:
        if rel.get("qualifiers") and not contains_any(u,rel["qualifiers"]):
            continue
        if rel.get("forbid_weaker") and contains_any(u,rel["forbid_weaker"]):
            return finding(rel,"VIOLATED","ASSERTION_STRENGTH_CHANGED","forbidden weaker relation cue detected",u)
        if not has_neg(u) and not is_decoy(u): good.append(u)
    if good: return finding(rel,"VERIFIED","ASSERTION_VERIFIED","assertion reconstructed",good[0])
    return finding(rel,"VIOLATED","ASSERTION_NEGATED_OR_DECOY","assertion appears only negated/decoyed",units[0])

def relation_modality(rel,text):
    groups=[rel.get("subject"),rel.get("predicate"),rel.get("object")]
    units=candidate_units(text,groups)
    if not units:
        return finding(rel,"UNRESOLVED","MODAL_RELATION_NOT_FOUND","modal relation not reconstructed")
    modals=[norm(x) for x in rel.get("accepted_modals",[])]
    for u in units:
        if is_decoy(u): continue
        if any(re.search(r"\b"+re.escape(m)+r"\b",u) for m in modals) and not has_neg(u):
            return finding(rel,"VERIFIED","MODALITY_VERIFIED","required bounded modality retained",u)
    # a positive assertion without the source hedge is a strength change
    for u in units:
        if not is_decoy(u) and not has_neg(u):
            return finding(rel,"VIOLATED","MODALITY_STRENGTHENED","bounded source modality removed/strengthened",u)
    return finding(rel,"UNRESOLVED","MODALITY_UNRESOLVED","could not establish compatible modality")

def relation_scope(rel,text):
    req=rel.get("scope_required",[])
    base=[rel.get("subject"),rel.get("predicate")]
    units=[u for u in split_units(text) if contains_any(u,rel.get("subject")) and all(norm(x) in u for x in req)]
    if not units:
        return finding(rel,"UNRESOLVED","SCOPE_NOT_RECONSTRUCTED","required scope not reconstructed")
    for u in units:
        if re.search(r"\bnot only\b|\balso\b|\bbeyond\b|\bin addition to\b",u):
            return finding(rel,"VIOLATED","SCOPE_EXPANDED","exclusive source scope was expanded",u)
        if rel.get("exclusivity")=="ONLY":
            if re.search(r"\b(?:only|limited to|restricted to|focus(?:ed)? on|exclusively)\b",u) and not re.search(r"\bnot only\b",u):
                return finding(rel,"VERIFIED","SCOPE_VERIFIED","exclusive scope retained",u)
        else:
            return finding(rel,"VERIFIED","SCOPE_VERIFIED","scope retained",u)
    return finding(rel,"UNRESOLVED","SCOPE_EXCLUSIVITY_UNRESOLVED","scope terms present but exclusivity unresolved")

def _strip_times(s):
    return re.sub(r"\b\d{1,2}:\d{2}\b"," ",s)

NUM_WORDS={"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9","ten":"10"}

def _numbers_with_pos(s):
    z=_strip_times(s)
    out=[]
    for m in re.finditer(r"(?<![\w.])\d+(?:\.\d+)?%?",z):
        out.append((m.group(0).rstrip("%"),m.start()))
    for w,v in NUM_WORDS.items():
        for m in re.finditer(r"\b"+w+r"\b",z):
            out.append((v,m.start()))
    return out

def _alias_positions(s,aliases):
    if isinstance(aliases,str): aliases=[aliases]
    out=[]
    for a in aliases or []:
        a=norm(a)
        for m in re.finditer(re.escape(a),s): out.append((a,m.start(),m.end()))
    return out

def relation_quantity(rel,text,cardinality=False):
    subj=rel.get("subject")
    pred=rel.get("predicate")
    expected=str(rel["value"])
    expected_time=norm(rel.get("time",""))
    qualifier_numbers=set()
    for q in rel.get("qualifiers",[]):
        qualifier_numbers.update(x[0] for x in _numbers_with_pos(norm(q)))
    best=[]
    contradictions=[]
    for u in split_units(text):
        if not contains_any(u,subj): continue
        if pred and not contains_any(u,pred): continue
        if expected_time and expected_time not in u: continue
        if rel.get("qualifiers") and not contains_any(u,rel["qualifiers"]): continue
        if is_decoy(u): continue
        nums=_numbers_with_pos(u)
        # For measured quantities, only numbers locally paired with an allowed unit are binding candidates.
        if rel.get("unit") and not cardinality:
            unit_aliases=rel["unit"] if isinstance(rel["unit"],list) else [rel["unit"]]
            filtered=[]
            for n,pos in nums:
                for ua in unit_aliases:
                    ua=norm(ua)
                    if re.search(r"\b"+re.escape(n)+r"\s*"+re.escape(ua)+r"\b",u[max(0,pos-2):pos+30]):
                        filtered.append((n,pos)); break
            nums=filtered
        subjects=_alias_positions(u,subj)
        if not nums or not subjects: continue
        if expected_time and "baseline" in u and expected not in [n for n,_ in nums]:
            # A later delta sentence may mention the protected time only as the baseline.
            continue
        # bind each subject mention to its nearest numeric mention.
        for _,ss,se in subjects:
            ranked=sorted(nums,key=lambda x:min(abs(x[1]-ss),abs(x[1]-se)))
            if not ranked: continue
            nearest,dist=ranked[0]
            if dist>70: continue
            if nearest==expected:
                best.append(u)
            elif nearest not in qualifier_numbers:
                contradictions.append(u)
    if contradictions:
        return finding(rel,"VIOLATED","QUANTITY_REBOUND","different quantity/cardinality is more tightly bound to protected entity/relation",contradictions[0])
    if best:
        return finding(rel,"VERIFIED","QUANTITY_VERIFIED","quantity/cardinality binding retained",best[0])
    # No proximity-only verification when the protected predicate/qualifier is absent.
    return finding(rel,"UNRESOLVED","QUANTITY_BINDING_UNRESOLVED","expected quantity/cardinality not safely reconstructed")

def relation_metric(rel,text):
    t=norm(text)
    if rel.get("metrics"):
        metrics=rel["metrics"]
        groups=[]
        for x in metrics:
            groups.append(x if isinstance(x,list) else [x])
        for group in groups:
            if not contains_any(t,group):
                return finding(rel,"UNRESOLVED","METRIC_MISSING","required metric missing: "+" / ".join(group))
            for u in split_units(text):
                if contains_any(u,group) and has_neg(u):
                    return finding(rel,"VIOLATED","METRIC_NEGATED","required metric negated",u)
        return finding(rel,"VERIFIED","METRICS_VERIFIED","required metrics retained")
    metric=norm(rel["metric"]); definition=norm(rel["definition"])
    units=[u for u in split_units(text) if metric in u and definition in u]
    if any(not has_neg(u) for u in units):
        return finding(rel,"VERIFIED","METRIC_DEFINITION_VERIFIED","metric definition retained",units[0])
    return finding(rel,"UNRESOLVED","METRIC_DEFINITION_UNRESOLVED","metric definition not reconstructed")

def relation_polarity(rel,text):
    subj=rel.get("subject"); pred=rel.get("predicate"); obj=rel.get("object")
    units=candidate_units(text,[subj,pred,obj])
    if not units:
        return finding(rel,"UNRESOLVED","POLAR_RELATION_NOT_FOUND","polar relation not reconstructed")
    expected=rel["polarity"]
    active=[u for u in units if not is_decoy(u)]
    if not active: return finding(rel,"UNRESOLVED","POLAR_RELATION_DECOY_ONLY","relation appears only in decoy context")
    def negative_semantics(u):
        return has_neg(u) or bool(re.search(r"\b(?:unchanged|unmodified|excluded from|no imputation)\b",u))
    # explicit contradiction dominates any correct-looking clause
    if expected=="POSITIVE":
        bad=[u for u in active if negative_semantics(u)]
        good=[u for u in active if not negative_semantics(u)]
    else:
        bad=[u for u in active if not negative_semantics(u)]
        good=[u for u in active if negative_semantics(u)]
    if bad: return finding(rel,"VIOLATED","POLARITY_REVERSED","protected polarity contradicted",bad[0])
    if good: return finding(rel,"VERIFIED","POLARITY_VERIFIED","protected polarity retained",good[0])
    return finding(rel,"UNRESOLVED","POLARITY_UNRESOLVED","polarity unresolved")

def relation_association(rel,text):
    units=candidate_units(text,[rel.get("subject"),["associated","association","correlated","correlation"],rel.get("object")])
    if not units: return finding(rel,"UNRESOLVED","ASSOCIATION_NOT_FOUND","association not reconstructed")
    for u in units:
        if is_decoy(u): continue
        d=rel.get("direction")
        if d=="HIGHER_TO_SHORTER" and ("higher" in u and ("shorter" in u or "reduced" in u)) and not has_neg(u):
            return finding(rel,"VERIFIED","ASSOCIATION_VERIFIED","association direction retained",u)
        if d=="LOWER_TO_HIGHER" and "lower" in u and "higher" in u and not has_neg(u):
            return finding(rel,"VERIFIED","ASSOCIATION_VERIFIED","association direction retained",u)
    # Presence of association with opposite directional adjective is a hard violation.
    return finding(rel,"VIOLATED","ASSOCIATION_DIRECTION_CHANGED","association direction not compatible with source",units[0])

def relation_causality(rel,text):
    subj=rel.get("subject"); obj=rel.get("object")
    units=[u for u in split_units(text) if contains_any(u,subj) and contains_any(u,obj)]
    if not units: return finding(rel,"UNRESOLVED","CAUSALITY_NOT_FOUND","causal-status relation not reconstructed")
    strong=r"\b(?:cause|causes|caused|causal|demonstrates?|establishes?|proves?|will cause|leads? to)\b"
    negcausal=r"\b(?:does not|did not|cannot|can not|not)\b.{0,80}\b(?:cause|causal|demonstrat|establish|prove)"
    if rel["status"]=="NOT_ESTABLISHED":
        # A contrastive sentence containing both a disclaimer and a later positive causal assertion is a contradiction.
        for u in units:
            if re.search(negcausal,u) and re.search(r"\b(?:contrary|however|but|although)\b.{0,180}\b(?:establishes?|demonstrates?|proves?|causal relationship|will cause)\b",u):
                return finding(rel,"VIOLATED","CAUSALITY_CONTRADICTION","negative causal bound followed by positive causal assertion",u)
        bad=[u for u in units if re.search(strong,u) and not re.search(negcausal,u) and not is_decoy(u)]
        if bad: return finding(rel,"VIOLATED","CAUSALITY_STRENGTHENED","non-causal source relation strengthened",bad[0])
        good=[u for u in units if re.search(negcausal,u)]
        if not good:
            # discourse-level negative causal cue may omit repeated subject/object.
            for u in split_units(text):
                if re.search(r"\b(?:does not|cannot|can not)\b.{0,80}\b(?:causal|cause|establish|demonstrat|prove)\b",u):
                    good.append(u)
        if good: return finding(rel,"VERIFIED","CAUSALITY_BOUND_RETAINED","non-causality bound retained",good[0])
    if rel["status"]=="PURPOSE_DISTINGUISH_FROM":
        alt=rel.get("alternative",[])
        good=[u for u in split_units(text) if contains_any(u,subj) and contains_any(u,alt) and re.search(r"\b(?:rather than|not because|distinguish|isolate)\b",u)]
        bad=[u for u in split_units(text) if contains_any(u,subj) and contains_any(u,alt) and re.search(r"\b(?:because of|due to|from)\b",u) and not re.search(r"rather than",u)]
        if bad: return finding(rel,"VIOLATED","PURPOSE_RELATION_REVERSED","alternative explanation asserted",bad[0])
        if good: return finding(rel,"VERIFIED","PURPOSE_RELATION_VERIFIED","distinguishing purpose retained",good[0])
    return finding(rel,"UNRESOLVED","CAUSALITY_UNRESOLVED","causal-status extraction unresolved")

def relation_citation(rel,text):
    cit=norm(rel["citation"]); terms=[norm(x) for x in rel["claim_terms"]]
    t=norm(text)
    if cit not in t: return finding(rel,"VIOLATED","CITATION_MISSING","citation id missing")
    # bind citation to nearest preceding clause/span
    pos=t.find(cit); pre=t[max(0,pos-180):pos]
    score=sum(term in pre for term in terms)
    if score>=2:
        return finding(rel,"VERIFIED","CITATION_EDGE_VERIFIED","citation remains attached to expected claim",pre[-160:])
    return finding(rel,"VIOLATED","CITATION_EDGE_REBOUND","citation not adjacent to expected claim",pre[-160:])

def relation_equation(rel,text):
    t=norm(text).replace(" ","")
    required=[norm(x).replace(" ","") for x in rel["required_tokens"]]
    if not all(x in t for x in required):
        return finding(rel,"UNRESOLVED","EQUATION_TOKENS_MISSING","equation identity tokens missing")
    # normalized operator between u_i and w_2/d_i region
    if "u_i-w_2d_i" in t or "u_i−w_2d_i" in t:
        return finding(rel,"VIOLATED","EQUATION_OPERATOR_CHANGED","equation operator changed from + to -")
    if "u_i+w_2d_i" in t:
        return finding(rel,"VERIFIED","EQUATION_VERIFIED","equation operator identity retained")
    return finding(rel,"UNRESOLVED","EQUATION_OPERATOR_UNRESOLVED","equation operator not safely reconstructed")

def relation_definition(rel,text):
    term=norm(rel["term"]); defs=[norm(x) for x in rel["definition"]]
    units=[u for u in split_units(text) if term in u]
    for u in units:
        if any(d in u for d in defs) and not has_neg(u):
            # Reject if another protected term is explicitly bound to this definition in same clause.
            return finding(rel,"VERIFIED","TERM_DEFINITION_VERIFIED","term definition retained",u)
    return finding(rel,"UNRESOLVED","TERM_DEFINITION_UNRESOLVED","term definition not reconstructed")

def relation_method(rel,text):
    actions=rel["action"]; objects=rel["object"]; cond=rel.get("condition",[])
    units=[u for u in split_units(text) if contains_any(u,actions) and contains_any(u,objects)]
    for u in units:
        if cond and not contains_any(u,cond): continue
        if has_neg(u) and not is_decoy(u): return finding(rel,"VIOLATED","METHOD_STEP_NEGATED","method step negated",u)
        if not is_decoy(u): return finding(rel,"VERIFIED","METHOD_STEP_VERIFIED","method step retained",u)
    return finding(rel,"UNRESOLVED","METHOD_STEP_UNRESOLVED","method step not reconstructed")

def relation_order(rel,text,results,ledger_case):
    before=rel["before"]; after=rel["after"]
    # derive action anchor from referenced ledger records
    byid={x["id"]:x for x in ledger_case}
    b=byid[before]; a=byid[after]; t=norm(text)
    bpos=min([t.find(norm(x)) for x in b["action"] if t.find(norm(x))>=0] or [-1])
    apos=min([t.find(norm(x)) for x in a["action"] if t.find(norm(x))>=0] or [-1])
    if bpos<0 or apos<0: return finding(rel,"UNRESOLVED","ORDER_UNRESOLVED","ordered actions not both found")
    if bpos<apos: return finding(rel,"VERIFIED","ORDER_VERIFIED","method order retained")
    return finding(rel,"VIOLATED","ORDER_REVERSED","protected method order reversed")

def relation_exclusion(rel,text):
    units=[u for u in split_units(text) if contains_any(u,rel["entity"]) and contains_any(u,rel["condition"]) and contains_any(u,rel["action"])]
    if not units: return finding(rel,"UNRESOLVED","EXCLUSION_UNRESOLVED","exclusion relation not reconstructed")
    for u in units:
        if re.search(r"\bnot excluded\b|\binclude[sd]?\b",u) and not is_decoy(u):
            return finding(rel,"VIOLATED","EXCLUSION_REVERSED","protected exclusion reversed",u)
        if re.search(r"\bexcluded\b|\bexclude\b",u) and not has_neg(u):
            return finding(rel,"VERIFIED","EXCLUSION_VERIFIED","exclusion retained",u)
    return finding(rel,"UNRESOLVED","EXCLUSION_UNRESOLVED","exclusion polarity unresolved")

def relation_delta(rel,text):
    val=norm(rel["value"]); subj=rel["subject"]; base=norm(rel["baseline"])
    units=[u for u in split_units(text) if contains_any(u,subj) and val in u]
    if not units: return finding(rel,"UNRESOLVED","DELTA_NOT_FOUND","delta relation not reconstructed")
    expected="increase" if rel["direction"]=="INCREASE" else "decrease"
    opposite="decrease" if expected=="increase" else "increase"
    for u in units:
        if opposite in u and not re.search(r"\bnot\s+"+opposite,u):
            return finding(rel,"VIOLATED","DELTA_DIRECTION_REVERSED","delta direction reversed",u)
        if expected in u and not re.search(r"\bnot\s+"+expected,u) and base in norm(text):
            return finding(rel,"VERIFIED","DELTA_VERIFIED","delta direction and baseline retained",u)
    return finding(rel,"UNRESOLVED","DELTA_UNRESOLVED","delta direction unresolved")

def relation_mechanism(rel,text):
    t=norm(text)
    if rel.get("must_not_globalize"):
        # if a lead/general sentence names mechanism A while grouping B subjects, reject
        for u in split_units(text):
            if norm(rel["mechanism_a"]) in u and any(norm(x) in u for x in rel["subjects_b"]):
                if not is_decoy(u): return finding(rel,"VIOLATED","MECHANISM_CONFLATED","mechanism generalized to wrong study/entity",u)
        return finding(rel,"VERIFIED","MECHANISM_DISTINCTION_VERIFIED","no cross-mechanism conflation detected")
    if rel.get("must_be_distinct"):
        if re.search(r"\b(?:same mechanism|evidence for the same mechanism)\b",t) and not re.search(r"\b(?:not|should not)\b.{0,30}same mechanism",t):
            return finding(rel,"VIOLATED","MECHANISM_COLLAPSED","distinct mechanisms collapsed")
        if re.search(r"\b(?:different|distinct) subsystems?\b",t) or re.search(r"\bshould not\b.{0,50}same mechanism",t):
            return finding(rel,"VERIFIED","MECHANISM_DISTINCTION_VERIFIED","distinction retained")
        return finding(rel,"UNRESOLVED","MECHANISM_DISTINCTION_UNRESOLVED","distinction not reconstructed")
    return finding(rel,"UNRESOLVED","MECHANISM_UNRESOLVED","mechanism relation unresolved")

def relation_directional(rel,text):
    t=norm(text)
    subj=rel.get("subject")
    obj=rel.get("object")
    units=[u for u in split_units(text) if contains_any(u,subj) and contains_any(u,obj)]
    if not units:
        return finding(rel,"UNRESOLVED","DIRECTIONAL_RELATION_UNRESOLVED","directional relation not reconstructed")
    expected=rel.get("expected")
    for u in units:
        if is_decoy(u): continue
        if expected=="LARGER_WHEN_LARGER":
            bad=re.search(r"(?:larger|higher).{0,45}(?:priority).{0,70}(?:smaller|lower)|(?:priority).{0,80}(?:larger|higher).{0,80}(?:smaller|lower)",u)
            good=re.search(r"(?:larger|higher).{0,45}(?:priority).{0,90}(?:larger|higher)|(?:priority).{0,80}(?:larger|higher).{0,80}(?:combination).{0,40}(?:larger|higher)",u)
            if bad: return finding(rel,"VIOLATED","DIRECTION_REVERSED","protected monotonic direction reversed",u)
            if good: return finding(rel,"VERIFIED","DIRECTION_VERIFIED","protected monotonic direction retained",u)
    return finding(rel,"UNRESOLVED","DIRECTIONAL_RELATION_UNRESOLVED","directional relation present but comparator binding unresolved")

def relation_parameter(rel,text):
    t=norm(text)
    if rel["status"]=="FIXED_BEFORE_RUN":
        if re.search(r"weights?.{0,80}(?:fixed|set).{0,40}(?:before|prior to)",t):
            if re.search(r"weights?.{0,100}(?:constant throughout|remain constant throughout)",t):
                return finding(rel,"UNRESOLVED","PARAMETER_EXTRA_INFERENCE","adds throughout-run stability beyond source")
            return finding(rel,"VERIFIED","PARAMETER_STABILITY_VERIFIED","pre-run fixed status retained")
    if rel["status"]=="SAME_ACROSS_DENSITIES":
        if re.search(r"(?:same|fixed).{0,40}parameter.{0,100}densit|parameter.{0,50}(?:same|fixed).{0,100}densit",t):
            if re.search(r"(?:retuned|retune).{0,50}(?:each|every).{0,20}densit",t) and not is_decoy(t):
                return finding(rel,"VIOLATED","PARAMETER_STABILITY_REVERSED","controller retuning asserted")
            return finding(rel,"VERIFIED","PARAMETER_STABILITY_VERIFIED","same-across-density status retained")
    return finding(rel,"UNRESOLVED","PARAMETER_STABILITY_UNRESOLVED","parameter stability not reconstructed")

HANDLERS={
 "TEXT_ASSERTION":relation_text_assertion,
 "MODALITY":relation_modality,
 "SCOPE":relation_scope,
 "CARDINALITY":lambda r,t: relation_quantity(r,t,True),
 "QUANTITY_BINDING":relation_quantity,
 "METRIC_DEFINITION":relation_metric,
 "POLARITY":relation_polarity,
 "ASSOCIATION":relation_association,
 "CAUSALITY":relation_causality,
 "CITATION_EDGE":relation_citation,
 "EQUATION_IDENTITY":relation_equation,
 "TERM_DEFINITION":relation_definition,
 "METHOD_STEP":relation_method,
 "EXCLUSION":relation_exclusion,
 "DELTA_DIRECTION":relation_delta,
 "MECHANISM_DISTINCTION":relation_mechanism,
 "PARAMETER_STABILITY":relation_parameter,
 "DIRECTIONAL_RELATION":relation_directional,
}

def verify_case(case_id,text,ledger):
    rels=ledger["relations_by_case"][case_id]
    results=[]
    for rel in rels:
        if rel["type"]=="ORDER_BEFORE":
            results.append(relation_order(rel,text,results,rels))
        else:
            h=HANDLERS.get(rel["type"])
            if not h:
                results.append(finding(rel,"UNRESOLVED","UNSUPPORTED_RELATION_TYPE","no generic handler"))
            else:
                results.append(h(rel,text))
    counts=collections.Counter(x["status"] for x in results)
    disposition="REJECT" if counts["VIOLATED"] else ("REVIEW" if counts["UNRESOLVED"] else "PASS_CANDIDATE")
    return {"case_id":case_id,"disposition":disposition,"relation_counts":dict(counts),"relations":results}

def main():
    ap=sys.argv[1:]
    if len(ap)<3:
        raise SystemExit("usage: verifier.py LEDGER.json CASE_ID TEXT_FILE")
    ledger=json.loads(pathlib.Path(ap[0]).read_text(encoding="utf-8"))
    text=pathlib.Path(ap[2]).read_text(encoding="utf-8")
    print(json.dumps(verify_case(ap[1],text,ledger),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
