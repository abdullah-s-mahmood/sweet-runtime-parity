class LanguageAdapter:
    language="unknown"
    def capabilities(self): return {}
class EnglishAdapter(LanguageAdapter):
    language="en"
    def capabilities(self): return {"word_count":True,"sentence_units":True,"morphology":False,"syntax":False,"voice":False,"detector_protocol":False}
class NonLinguisticStubAdapter(LanguageAdapter):
    language="stub-x"
    def capabilities(self): return {"word_count":False,"unit_count":"characters","sentence_units":False}
