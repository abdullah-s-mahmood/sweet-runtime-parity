import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
import unittest
from core import *
class CoreTests(unittest.TestCase):
    def test_canonical_identity(self): self.assertEqual(transaction_id({"a":1,"b":2}),transaction_id({"b":2,"a":1}))
    def test_rollback(self):
        s=Source("v1","abc");p=Proposal("v1",s.hash,"xyz");ok,_,st=apply_proposal(s,p);self.assertTrue(ok);self.assertEqual(rollback(s,st).text,"abc")
    def test_length(self):
        a=" ".join(["w"]*100);b=" ".join(["w"]*85);self.assertTrue(length_metrics(a,b)["within_15pct"])
if __name__=="__main__": unittest.main()
