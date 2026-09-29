"""Final fine-tuned Arabic CAD feasibility model. External QALB14 only."""
from __future__ import annotations
import hashlib,json,math,random
from pathlib import Path
import numpy as np, torch
from torch.utils.data import DataLoader,Dataset
from transformers import AutoTokenizer,AutoModelForSequenceClassification,get_linear_schedule_with_warmup
from sklearn.metrics import roc_auc_score
from phase2.generalization.cad_qalb14_data_common import examples_for_split,select_train,select_dev,rows_hash

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"upstream/arabic-gec/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
TRAIN_SRC=BASE/"train/QALB-2014-L1-Train.sent.no_ids"; TRAIN_GOLD=BASE/"train/QALB-2014-L1-Train.cor.no_ids"
DEV_SRC=BASE/"dev/QALB-2014-L1-Dev.sent.no_ids"; DEV_GOLD=BASE/"dev/QALB-2014-L1-Dev.cor.no_ids"
OUT=ROOT/"PHASE2_CAD_FINETUNED_TRAINING_SUMMARY.json"; MODEL_DIR=ROOT/"CAD_FINETUNED_MODEL"
MODEL_ID="CAMeL-Lab/bert-base-arabic-camelbert-msa"; REV="9c0a8968fc47b06469302963b68caa5ce5e943af"
MAX_LENGTH=96; BATCH=16; EPOCHS=3; LR=1e-5; WD=0.01; SEED=0

def set_seed(s):
    random.seed(s);np.random.seed(s);torch.manual_seed(s)

class PairDS(Dataset):
    def __init__(self,rows,tok,with_labels=True):
        self.rows=rows;self.tok=tok;self.with_labels=with_labels
    def __len__(self):return len(self.rows)
    def __getitem__(self,i):
        r=self.rows[i]
        enc=self.tok(r["source"],r["candidate"],truncation=True,max_length=MAX_LENGTH,padding="max_length",return_tensors="pt")
        item={k:v.squeeze(0) for k,v in enc.items()}
        if self.with_labels:item["labels"]=torch.tensor(int(r["label"]),dtype=torch.long)
        return item

def sha_dir(path):
    h=hashlib.sha256()
    for p in sorted(path.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(path)).encode())
            with p.open("rb") as f:
                for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def probs(model,loader):
    model.eval();out=[]
    with torch.no_grad():
        for b in loader:
            labels=b.pop("labels",None)
            logits=model(**b).logits
            out.extend(torch.softmax(logits,dim=-1)[:,1].cpu().numpy().tolist())
    return np.asarray(out,dtype=np.float64)

def main():
    set_seed(SEED);torch.set_num_threads(max(1,min(8,torch.get_num_threads())))
    tr=select_train(examples_for_split(TRAIN_SRC,TRAIN_GOLD,"train"))
    dv=select_dev(examples_for_split(DEV_SRC,DEV_GOLD,"dev"))
    tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REV,use_fast=True)
    model=AutoModelForSequenceClassification.from_pretrained(MODEL_ID,revision=REV,num_labels=2).cpu()
    g=torch.Generator();g.manual_seed(SEED)
    train_loader=DataLoader(PairDS(tr,tok),batch_size=BATCH,shuffle=True,generator=g)
    dev_loader=DataLoader(PairDS(dv,tok),batch_size=BATCH,shuffle=False)
    opt=torch.optim.AdamW(model.parameters(),lr=LR,weight_decay=WD)
    steps=len(train_loader)*EPOCHS; warm=int(0.1*steps)
    sched=get_linear_schedule_with_warmup(opt,warm,steps)
    trace=[]
    for ep in range(EPOCHS):
        model.train();tot=0.0
        for i,b in enumerate(train_loader,1):
            opt.zero_grad(set_to_none=True)
            loss=model(**b).loss;loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
            opt.step();sched.step();tot+=float(loss.item())
            if i%100==0:print(f"[epoch {ep+1}/{EPOCHS}] step {i}/{len(train_loader)} loss={tot/i:.6f}",flush=True)
        trace.append({"epoch":ep+1,"mean_loss":tot/len(train_loader)})
    p=probs(model,dev_loader);y=np.asarray([x["label"] for x in dv],dtype=np.int64)
    max_neg=float(np.max(p[y==0]));thr=float(np.nextafter(np.float64(max_neg),np.float64(2.0)))
    pred=p>=thr;neg_false=int(np.sum(pred&(y==0)));pos_pass=int(np.sum(pred&(y==1)));pos_total=int(np.sum(y==1))
    auc=float(roc_auc_score(y,p));ret=pos_pass/pos_total
    feasible=neg_false==0 and pos_pass>=300 and ret>=0.25
    MODEL_DIR.mkdir(exist_ok=True);model.save_pretrained(MODEL_DIR);tok.save_pretrained(MODEL_DIR)
    summary={
      "status":"PHASE2_CAD_FINETUNED_EXTERNAL_MODEL_TRAINED","training_source":"QALB14_EXTERNAL_ONLY",
      "current_phase_labels_read":False,"qalb15_corrected_read":False,"qalb15_test_read":False,"qalb_text_persisted":False,
      "model_id":MODEL_ID,"model_revision":REV,"architecture":"AutoModelForSequenceClassification_num_labels_2",
      "max_length":MAX_LENGTH,"batch_size":BATCH,"epochs":EPOCHS,"learning_rate":LR,"weight_decay":WD,"seed":SEED,
      "training_examples":len(tr),"dev_examples":len(dv),"train_selection_ids_sha256":rows_hash(tr),"dev_selection_ids_sha256":rows_hash(dv),
      "training_trace":trace,"dev_auc":auc,"max_dev_negative_probability":max_neg,"acceptance_threshold":thr,
      "dev_negative_false_accepts":neg_false,"dev_positive_pass":pos_pass,"dev_positive_total":pos_total,"dev_positive_retention":ret,
      "external_feasibility_criterion_met":feasible,"model_dir_sha256":sha_dir(MODEL_DIR),
      "next_action":"SCORE_CONSUMED_QALB15" if feasible else "STOP_PHASE2_ARABIC_AUTO_ACCEPT_REVIEW_FIRST",
    }
    OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in OUT.read_text(encoding="utf-8"))
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":main()
