from __future__ import annotations
import re

def nrm(s:str)->str:
    s=s.lower().replace("–","-").replace("—","-")
    return re.sub(r"\s+"," ",s).strip()

def units(text:str):
    t=nrm(text)
    out=[]
    for s in [x.strip() for x in re.split(r"(?<=[.!?;])\s+|;\s*",t) if x.strip()]:
        out.append(s)
        out.extend(x.strip() for x in re.split(r",\s+|\bbut\b|\bwhile\b|\bwhereas\b",s) if x.strip())
    seen=set(); uniq=[]
    for x in out:
        if x not in seen: seen.add(x); uniq.append(x)
    return uniq

def any_re(text,pats): return any(re.search(p,text,re.I) for p in pats)
def all_re(text,pats): return all(re.search(p,text,re.I) for p in pats)
def F(code,severity,msg): return {"code":code,"severity":severity,"message":msg}

def validate(case_id:str, source:str, candidate:str)->dict:
    t=nrm(candidate); us=units(candidate); findings=[]
    def hard(c,m): findings.append(F(c,"HARD",m))
    def review(c,m): findings.append(F(c,"REVIEW",m))
    def req(cond,c,m,sev="HARD"):
        if not cond: (hard if sev=="HARD" else review)(c,m)
    def forbid(pats,c,m):
        if any_re(t,pats): hard(c,m)
    def pair(must,wrong,c):
        req(any_re(t,must),c,"required assertion binding missing")
        forbid(wrong,c+"_CONTRADICTION","contradictory assertion binding present")
    def polarity(pos=None,neg=None,pos_forbid=None,neg_forbid=None,c="POL"):
        if pos: req(any_re(t,pos),c,"required positive proposition missing")
        if neg: req(any_re(t,neg),c,"required negative proposition missing")
        if pos_forbid: forbid(pos_forbid,c+"_POS_CONTRADICTION","positive contradiction present")
        if neg_forbid: forbid(neg_forbid,c+"_NEG_CONTRADICTION","negative contradiction present")

    if case_id=="EN01":
        req(all_re(t,[r"(platforms?|sensing).{0,80}(monitor|track).{0,80}traffic",r"real[- ]?time"]),"EN01_MONITOR","real-time traffic monitoring missing")
        req(all_re(t,[r"roadside",r"(collect|observation)"]),"EN01_ROADSIDE","roadside observation collection missing")
        rel=[u for u in us if re.search(r"(support|facilitat|identif).{0,80}congestion|congestion.{0,80}(support|facilitat|identif)",u,re.I)]
        req(bool(rel),"EN01_SUPPORT","congestion-identification relation missing")
        req(bool(rel) and any(re.search(r"\b(can|may|could|potentially)\b",u,re.I) for u in rel),"EN01_MODAL","modal limitation removed")
        req(all_re(t,[r"arterial roads?",r"weekday peak"]),"EN01_SCOPE","scope anchors missing")
        scope=[u for u in us if all_re(u,[r"arterial roads?",r"weekday peak"])]
        req(bool(scope) and any(any_re(u,[r"\bonly\b",r"\blimit(?:ed)?\b",r"\brestrict(?:ed)?\b",r"\bexclusive(?:ly)?\b"]) for u in scope),"EN01_EXCLUSIVE","exclusive evaluation scope missing")
        forbid([r"not only.{0,80}but also",r"local roads?",r"off[- ]peak",r"weekends?",r"highways?"],"EN01_SCOPE_EXPANSION","scope expansion detected")

    elif case_id=="EN02":
        pair([r"(fill estimates?|controller).{0,100}15\s*(?:minutes?|min\b)",r"15\s*(?:minutes?|min\b).{0,100}(fill estimates?|controller)"],
             [r"(fill estimates?|controller).{0,100}(30|60)\s*(?:minutes?|min\b)"],"EN02_INTERVAL")
        veh=[u for u in us if re.search(r"collection vehicles?",u,re.I)]
        req(bool(veh) and any(any_re(u,[r"\btwo\b",r"\b2\b"]) for u in veh),"EN02_VEHICLES","two-vehicle binding missing")
        req(not any(any_re(u,[r"\bone\b",r"\b1\b",r"\bthree\b",r"\b3\b",r"\bfour\b",r"\b4\b"]) for u in veh),"EN02_VEHICLE_CONTRADICTION","alternate vehicle count present")
        req("synthetic district" in t,"EN02_DISTRICT","synthetic district missing")
        req("travel distance" in t and bool(re.search(r"missed[- ]overflow",t)),"EN02_METRICS","metrics missing")

    elif case_id=="EN03":
        pair([r"study a.{0,100}(lower|reduc\w*) latency"],[r"study a.{0,120}(higher|increase\w*) latency"],"EN03_A")
        req(bool(re.search(r"study b.{0,140}(no|not|did not).{0,60}latency.{0,40}(reduc|improv)",t)) and "sparse traffic" in t,"EN03_B","Study B relation missing")
        mc=re.search(r"study c",t); md=re.search(r"study d",t)
        seg=t[mc.start():md.start()] if mc and md and md.start()>mc.start() else ""
        req(bool(seg) and bool(re.search(r"12\s*%",seg)) and bool(re.search(r"energy",seg)) and bool(re.search(r"decrease|lower|reduc",seg)),"EN03_C","Study C 12% energy-decrease relation missing")
        req(not bool(seg and re.search(r"12\s*%",seg) and re.search(r"energy",seg) and re.search(r"increase|higher|rise|rose",seg)),"EN03_C_DIRECTION","opposite Study C direction present")
        pair([r"study d.{0,140}batch.{0,80}(increase\w*|higher).{0,50}delay"],[r"study d.{0,140}batch.{0,80}(decrease\w*|lower).{0,50}delay"],"EN03_D")
        forbid([r"(studies? a.{0,80}(?:b|c|d)|studies? a, b, c,? and d).{0,160}impact of edge aggregation.{0,120}energy consumption"],"EN03_MECHANISM","mechanism conflation detected")
        req(any_re(t,[r"not (?:uniformly )?consistent",r"different operating conditions",r"vary across"]),"EN03_CONTRAST","non-uniformity statement missing","REVIEW")

    elif case_id=="EN04":
        claim1=[u for u in us if all_re(u,[r"queue length",r"(reduc|lower)"])]
        claim2=[u for u in us if all_re(u,[r"packet loss",r"(increase|higher)",r"(density|roadside|rsu)"])]
        req(bool(claim1) and any("cit_syn_01" in u for u in claim1),"EN04_CIT1","CIT_SYN_01 not bound to queue claim")
        req(not any("cit_syn_02" in u for u in claim1),"EN04_CIT1_SWAP","wrong citation bound to queue claim")
        req(bool(claim2) and any("cit_syn_02" in u for u in claim2),"EN04_CIT2","CIT_SYN_02 not bound to packet-loss claim")
        req(not any("cit_syn_01" in u for u in claim2),"EN04_CIT2_SWAP","wrong citation bound to packet-loss claim")
        req(any_re(t,[r"different subsystems?",r"distinct subsystems?"]),"EN04_DISTINCT","different-subsystem distinction missing","REVIEW")
        forbid([r"should be treated as evidence for the same mechanism",r"same mechanism.{0,30}(?:is|was|explains|evidence)"],"EN04_MECHANISM_CONTRADICTION","same-mechanism contradiction present")
        forbid([r"adaptive signal timing.{0,80}(?:associated with|association)"],"EN04_STRENGTH","source reduction claim weakened to association")

    elif case_id=="EN05":
        req("evening" in t,"EN05_POP","evening-window population missing")
        pair([r"higher beacon density.{0,90}(associat|correlat).{0,80}shorter discovery|shorter discovery.{0,90}(associat|correlat).{0,80}higher beacon density"],
             [r"higher beacon density.{0,90}(associat|correlat).{0,80}longer discovery|longer discovery.{0,90}(associat|correlat).{0,80}higher beacon density"],"EN05_ASSOC")
        req(any_re(t,[r"\bmay\b.{0,100}(awareness|neighbor)|(awareness|neighbor).{0,100}\bmay\b"]),"EN05_HEDGE","uncertainty qualifier missing")
        polarity(neg=[r"(does not|cannot|did not).{0,100}(establish|demonstrate|prove).{0,80}caus",r"not.{0,50}causal"],
                 pos_forbid=[r"\b(establishes?|demonstrates?|proves?)\b.{0,100}(causal|caus(?:e|es|ed|ing))",r"causal relationship.{0,40}(?:is|was)?\s*(?:established|demonstrated|proven)"],c="EN05_CAUSAL")
        req(any_re(t,[r"not (?:evaluated|assessed|tested) outside",r"outside the evening window.{0,50}not"]),"EN05_OUTSIDE","outside-window restriction missing")

    elif case_id=="EN06":
        pairs=[
          ("0800A",[r"08:00.{0,80}group a.{0,40}42\.0",r"08:00.{0,100}42\.0.{0,20}(?:for|to)\s+group a"],[r"08:00.{0,80}group a.{0,35}51\.5",r"08:00.{0,100}51\.5.{0,20}(?:for|to)\s+group a"]),
          ("0800B",[r"08:00.{0,120}group b.{0,40}51\.5",r"08:00.{0,120}51\.5.{0,20}(?:for|to)\s+group b"],[r"08:00.{0,120}group b.{0,35}42\.0",r"08:00.{0,120}42\.0.{0,20}(?:for|to)\s+group b"]),
          ("1400A",[r"14:00.{0,80}group a.{0,40}46\.2",r"14:00.{0,100}46\.2.{0,20}(?:for|to)\s+group a"],[r"14:00.{0,100}group a.{0,35}49\.8",r"14:00.{0,100}49\.8.{0,20}(?:for|to)\s+group a"]),
          ("1400B",[r"14:00.{0,120}group b.{0,40}49\.8",r"14:00.{0,120}49\.8.{0,20}(?:for|to)\s+group b"],[r"14:00.{0,120}group b.{0,35}46\.2",r"14:00.{0,120}46\.2.{0,20}(?:for|to)\s+group b"])]
        for cid,m,w in pairs: pair(m,w,"EN06_"+cid)
        delta=[u for u in us if "4.2" in u and "group a" in u]
        req(bool(delta) and any_re(" ".join(delta),[r"increase|increased|rose"]),"EN06_DELTA","4.2-second increase missing")
        req(not any_re(" ".join(delta),[r"decrease|decreased|fell|reduced"]),"EN06_DELTA_DIRECTION","opposite delta direction present")
        req("baseline" in t and "08:00" in t,"EN06_BASELINE","baseline relation missing","REVIEW")

    elif case_id=="EN07":
        req(any_re(t,[r"(discard|reject|remove)\w*.{0,80}(older than|over) 60\s*(?:s|seconds?)",r"60\s*(?:s|seconds?).{0,80}(discard|reject|remove)"]),"EN07_DISCARD","stale-reading discard missing")
        req(any_re(t,[r"normaliz\w*.{0,100}fixed (?:before|prior to) (?:evaluation|the evaluation|run|the run)"]),"EN07_NORMALIZE","pre-fixed normalization missing")
        m1=re.search(r"(discard|reject|remove)\w*.{0,80}(older than|over) 60",t); m2=re.search(r"normaliz",t)
        req(bool(m1 and m2 and m1.start()<m2.start()),"EN07_ORDER","discard/normalize order changed")
        polarity(pos=[r"exclud\w*.{0,80}(missing|lacking) position|(missing|lacking) position.{0,80}exclud"],
                 neg_forbid=[r"not exclud\w*.{0,80}(missing|lacking) position|(missing|lacking) position.{0,80}not exclud"],c="EN07_EXCLUDE")
        req("200" in t and bool(re.search(r"seed\s*17",t)),"EN07_REPRO","200 iterations / seed 17 missing")
        forbid([r"seed\s*(?!17\b)\d+"],"EN07_SEED_CHANGE","alternate seed present")
        req(any_re(t,[r"without (?:further|additional) tuning",r"no (?:further|additional) tuning",r"not.{0,60}(?:further|additional) tun"]),"EN07_NOTUNE","no-further-tuning condition missing")

    elif case_id=="EN08":
        pair([r"lower channel occupancy.{0,100}(associat|correlat).{0,100}higher delivery ratio|higher delivery ratio.{0,100}(associat|correlat).{0,100}lower channel occupancy"],
             [r"higher channel occupancy.{0,100}(associat|correlat).{0,100}higher delivery ratio",r"lower channel occupancy.{0,100}(associat|correlat).{0,100}lower delivery ratio"],"EN08_ASSOC")
        req(any_re(t,[r"(strongest|most pronounced).{0,80}medium[- ]density",r"medium[- ]density.{0,80}(strongest|most pronounced)"]),"EN08_MEDIUM","medium-density qualifier missing")
        req(any_re(t,[r"(not|did not).{0,80}(manipulat|control)\w*.{0,50}occupancy",r"occupancy.{0,80}(not|did not).{0,50}(manipulat|control)"]),"EN08_MANIP","non-manipulation condition missing")
        polarity(neg=[r"(does not|cannot|did not).{0,100}(demonstrate|establish|prove).{0,100}(cause|causal|reducing occupancy)",r"not.{0,60}causal"],
                 pos_forbid=[r"\b(demonstrates?|establishes?|proves?)\b.{0,120}(cause|causal|reducing occupancy)",r"reducing occupancy.{0,100}\b(causes?|will cause)\b"],c="EN08_CAUSAL")

    elif case_id=="EN09":
        compact=re.sub(r"\s+","",t)
        req("p_i=w_1u_i+w_2d_i" in compact,"EN09_EQUATION","equation identity/operator changed")
        pair([r"u_i\s*,?\s*(?:is|represents?|denotes?)\s+utilization",r"utilization\s*\(\s*u_i\s*\)"],
             [r"u_i\s*,?\s*(?:is|represents?|denotes?)\s+normalized deadline pressure"],"EN09_U")
        pair([r"d_i\s*,?\s*(?:is|represents?|denotes?)\s+normalized deadline pressure",r"normalized deadline pressure\s*\(\s*d_i\s*\)"],
             [r"d_i\s*,?\s*(?:is|represents?|denotes?)\s+utilization"],"EN09_D")
        req(bool(re.search(r"weights?.{0,100}fixed (?:before|prior to) (?:the )?run",t)),"EN09_WEIGHTS","fixed-before-run weights missing")
        req(any_re(t,[r"(larger|greater) priority.{0,120}(weighted combination).{0,80}(larger|greater)",r"(weighted combination).{0,80}(larger|greater).{0,120}(larger|greater) priority"]),"EN09_PRIORITY","priority-direction explanation missing")
        forbid([r"(larger|greater) priority.{0,120}(weighted combination).{0,80}(smaller|lower)",r"(weighted combination).{0,80}(smaller|lower).{0,120}(larger|greater) priority"],"EN09_PRIORITY_DIRECTION","priority direction reversed")
        req(any_re(t,[r"equation.{0,80}(unchanged|not changed|not modified)",r"(?:unchanged|not changed|not modified).{0,80}equation"]),"EN09_UNCHANGED","equation unchanged during adaptation missing")

    elif case_id=="EN10":
        pair([r"(measurement|collect).{0,100}every 30\s*(?:s|seconds?)",r"every 30\s*(?:s|seconds?).{0,100}(measurement|collect)"],
             [r"(measurement|collect).{0,100}every (?:15|60)\s*(?:s|seconds?)"],"EN10_RATE")
        req("active node" in t and "timestamp" in t and "node identifier" in t,"EN10_META","active-node/timestamp/node-id content missing")
        req(bool(re.search(r"group\w*.{0,80}node",t)) and bool(re.search(r"(five|5)[- ]minute",t)),"EN10_GROUP","grouping rule missing")
        polarity(neg=[r"no imputation",r"not imputed",r"imputation is not",r"performs? no imputation"],
                 pos_forbid=[r"missing measurements? (?:are|is) imputed",r"\bimput(?:e|es|ed|ing)\b.{0,40}missing measurements?"],c="EN10_IMPUTE")

    elif case_id=="EN11":
        req(bool(re.search(r"gateway.{0,100}receiv\w*.{0,60}report",t)) and "identifier" in t and "timestamp" in t,"EN11_GATEWAY","receive/check content missing")
        polarity(pos=[r"reject\w*.{0,60}duplicate"],neg_forbid=[r"(?:does not|do not|not)\s+reject\w*.{0,60}duplicate"],c="EN11_DUP")
        req(bool(re.search(r"forward\w*.{0,100}(accepted|valid).{0,80}storage",t)),"EN11_FORWARD","forward-to-storage relation missing")
        polarity(pos=[r"storage.{0,120}record\w*.{0,80}original timestamp"],neg_forbid=[r"storage.{0,120}(?:does not|do not|not)\s+record\w*.{0,80}original timestamp"],c="EN11_TS")

    elif case_id=="EN12":
        dens=[u for u in us if re.search(r"traffic densities?",u,re.I)]
        req(bool(dens) and any(any_re(u,[r"\bthree\b",r"\b3\b"]) for u in dens),"EN12_DENS","three-density scope missing")
        forbid([r"\b(two|2|four|4)\b.{0,30}traffic densities?"],"EN12_DENS_CHANGE","alternate density count present")
        req(any_re(t,[r"reliability.{0,80}(measur\w* as|=).{0,50}delivery ratio",r"delivery ratio.{0,80}reliability"]),"EN12_RELIABILITY","reliability=delivery ratio missing")
        polarity(pos=[r"delay.{0,40}(?:is|also)?\s*measur",r"measur\w*.{0,40}delay"],neg_forbid=[r"delay.{0,40}(?:is )?not measur",r"does not measur\w*.{0,40}delay"],c="EN12_DELAY")
        polarity(pos=[r"(same|fixed).{0,80}parameter.{0,100}(all|across).{0,30}densit",r"parameter.{0,80}(same|fixed).{0,100}densit"],
                 neg_forbid=[r"retun\w*.{0,80}(each|every).{0,30}densit",r"different parameter.{0,80}(each|every).{0,30}densit"],c="EN12_PARAMS")
        req(any_re(t,[r"(rather than|not).{0,100}retun",r"isolate.{0,100}retun",r"distinguish.{0,100}retun",r"rather than because of controller retuning"]),"EN12_PURPOSE","load-vs-retuning purpose missing","REVIEW")
    else:
        hard("UNKNOWN_CASE","unsupported case")

    hard_n=sum(x["severity"]=="HARD" for x in findings)
    review_n=sum(x["severity"]=="REVIEW" for x in findings)
    return {"case_id":case_id,"disposition":"REJECT" if hard_n else ("REVIEW" if review_n else "PASS_CANDIDATE"),"hard_findings":hard_n,"review_findings":review_n,"findings":findings}
