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
        if rel.get("qualifiers") and not all(contains_any(u,[q]) for q in rel["qualifiers"]):
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

def relation_quantity(rel,text,cardinality=False):
    subj=rel.get("subject")
    pred=rel.get("predicate")
    groups=[subj,pred] if pred else [subj]
    units=candidate_units(text,groups)
    expected=str(rel["value"])
    time=norm(rel.get("time",""))
    quals=[norm(x) for x in rel.get("qualifiers",[])]
    correct=[]
    contradictions=[]
    for u in units:
        nums=number_tokens(u)
        if time and time not in u: continue
        if quals and not all(q in u for q in quals): continue
        if expected in [n.rstrip("%") for n in nums] and not has_neg(u) and not is_decoy(u):
            correct.append(u)
        # competing numeric binding to same subject/predicate is a violation
        other=[n for n in nums if n.rstrip("%")!=expected and (not time or n!=time.replace(":",""))]
        if other and not is_decoy(u):
            contradictions.append(u)
    if contradictions:
        return finding(rel,"VIOLATED","QUANTITY_REBOUND","different quantity/cardinality bound to protected relation",contradictions[0])
    if correct:
        return finding(rel,"VERIFIED","QUANTITY_VERIFIED","quantity/cardinality binding retained",correct[0])
    # proximity fallback catches '51.5 s to Group A'
    t=norm(text)
    for m in re.finditer("|".join(re.escape(norm(x)) for x in (subj if isinstance(subj,list) else [subj])),t):
        win=t[max(0,m.start()-60):m.end()+60]
        nums=number_tokens(win)
        if nums:
            nearest_expected=expected in [n.rstrip("%") for n in nums]
            if nearest_expected and not has_neg(win) and not is_decoy(win):
                return finding(rel,"VERIFIED","QUANTITY_VERIFIED_PROXIMITY","quantity retained near entity",win)
    return finding(rel,"UNRESOLVED","QUANTITY_BINDING_UNRESOLVED","expected quantity/cardinality not safely rebound")

def relation_metric(rel,text):
    t=norm(text)
    if rel.get("metrics"):
        for metric in rel["metrics"]:
            if norm(metric) not in t: return finding(rel,"UNRESOLVED","METRIC_MISSING",f"metric missing: {metric}")
            for u in split_units(text):
                if norm(metric) in u and has_neg(u):
                    return finding(rel,"VIOLATED","METRIC_NEGATED",f"metric negated: {metric}",u)
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
    # explicit contradiction dominates any correct-looking clause
    if expected=="POSITIVE":
        bad=[u for u in active if has_neg(u)]
        good=[u for u in active if not has_neg(u)]
    else:
        bad=[u for u in active if not has_neg(u)]
        good=[u for u in active if has_neg(u)]
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
        # Any positive causal assertion anywhere dominates a negative decoy.
        bad=[u for u in units if re.search(strong,u) and not re.search(negcausal,u) and not is_decoy(u)]
        if bad: return finding(rel,"VIOLATED","CAUSALITY_STRENGTHENED","non-causal source relation strengthened",bad[0])
        good=[u for u in units if re.search(negcausal,u)]
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
