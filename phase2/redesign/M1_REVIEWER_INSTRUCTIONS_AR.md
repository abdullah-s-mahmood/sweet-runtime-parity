# تعليمات المحكّم البشري — M1 Pilot

هذه الحزمة جزء من مرحلة معايرة تعريف الحكم في ACAD_PASS، وليست اختبارًا للنموذج أو للمحكّم.

## ما الذي ستراه؟

لكل حالة:
- النص الأصلي؛
- النص بعد تعديل واحد محدد؛
- موضع التعديل وسطحه.

لن ترى اسم النموذج أو ثقته أو الحكم السابق أو التصحيح المرجعي أثناء المرور الأول.

## المطلوب

احكم على كل محور بصورة مستقلة وفق ACAD_PASS Edit Contract v1:

1. necessity
2. local_correctness
3. contextual_correctness
4. edit_group_status
5. residual_relation
6. semantic_fidelity
7. scientific_fidelity
8. protected_invariants
9. document_integrity
10. ambiguity_author_intent
11. severity

ثم اكتب:
- brief_rationale: سبب مختصر ومحدد.
- evidence_span_or_relation: الكلمة/العلاقة التي اعتمدت عليها.

## قواعد مهمة

- لا تستخدم GitHub أو ملفات المشروع للبحث عن الحكم التاريخي قبل تسليم المرور الأول.
- لا تعتبر اختلاف المرشح عن المرجع خطأ تلقائيًا.
- لا تعتبر التطابق مع مرجع واحد دليلًا على اكتمال إصلاح الجملة.
- فرّق بين خطأ سببه التعديل وخطأ كان موجودًا أصلًا وبقي دون مساس.
- إذا كان قصد المؤلف أو القراءة غير محسومين، استخدم ambiguity بدل التخمين.
- في نصوص Nahw التجريبية يكون scientific_fidelity غالبًا NOT_APPLICABLE ما لم توجد دلالة علمية فعلية.
- protected_invariants = NOT_TESTED إذا لم تُعطَ لك قائمة حماية قابلة للفحص.
- document_integrity = NOT_APPLICABLE في هذا pilot النصي ما لم يظهر فساد سطحي خارج نطاق التعديل.

لا تغير النصوص. أعد فقط ملف الاستجابة بعد ملء الحقول.
