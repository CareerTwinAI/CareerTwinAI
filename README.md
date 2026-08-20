# CareerTwin AI (Streamlit)

This version represents the Minimum Viable Product (MVP) that covers and processes all platform operations from onboarding to final evaluation. A career exploration platform that puts you inside a **virtual workday** in the job you're considering:
You face three interconnected situations, make decisions, see their realistic consequences, and then receive an **initial compatibility index specific to the selected job** along with a complete skills report.

- **10 career fields × 3 unique jobs** = 30 jobs, all fully **available to experience**.
- **Immersive UI:** A modern, comfortable, futuristic design with attractive visual effects and an immersive experience (Time-tunnel Effect).
- Arabic-first with full RTL layout, and an instant switch to English.
- **Demo Mode** works fully offline without an API key.
- **Live AI Mode** is optional via OpenAI or Azure OpenAI, with a silent automatic fallback to the local engine upon any failure — the experience never stops.

---

## Quick start

```bash
# 1) Inside the project folder
cd career_twin2

# 2) (Optional) Virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3) Install requirements
pip install -r requirements.txt

# 4) Run
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`. No additional setup is needed — Demo mode is ready immediately, and evaluators can complete the full experience offline.

## Automatic Mode Selection

There is no visible key or setting for the user: when valid API settings are available, Live AI Mode works automatically and a small "Smart simulation enabled" badge appears; when they are absent or the connection fails, the local Demo Mode works automatically and the experience completes without any interruption. For testing only, there is a hidden manual control inside the sidebar folded under "Demo settings".

## AI Activation

Copy `.env.example` to `.env` then fill in one of the options:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI Key (First option) |
| `OPENAI_MODEL` | Model name (default is `gpt-4o-mini`) |
| `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_DEPLOYMENT` | Microsoft Foundry / Azure OpenAI platform keys and settings (used automatically when available) |

Keys are never placed inside the code, and the platform is configured to connect directly to Azure and Foundry keys. When the model connection fails for any reason, the decision is evaluated by the local engine and a small note appears — without a blank page and without preventing the user from finishing the simulation.

## Project Structure

```text
career_twin/
├── app.py                 # Interface, navigation, game hosting (Tornado), and state management
├── requirements.txt
├── README.md
├── .env.example
├── components/            # Student Dashboard, Onboarding, and Education Stages
├── data/
│   └── careers.json       # Fields, jobs, situations, and evaluation weights data
├── static/                # Exported simulation game files (e.g. Godot)
├── services/
│   ├── ai_service.py      # Live AI Mode + Response validation
│   ├── scoring.py         # Performance Review and final report generation
│   └── demo_engine.py     # Local presentation engine and quick evaluation
├── utils/
│   ├── game_server.py     # Local server to host games with SharedArrayBuffer support
│   └── styles.py          # Visual identity and design
└── assets/                # Logos and UI images
```

## How the Simulation Works

1. **Dashboard & Onboarding**: Completing the student's profile (including Education Stage) and moving to a personalized dashboard that tracks progress in the career journey.
2. **Quick Profile**: Five questions that produce a recommendation for the three most suitable career fields for you (can be skipped).
3. **Game Integration**: Experiencing a game built with an external engine (like Godot) for some jobs to explore the work environment before starting the evaluation.
4. **A workday of three interconnected situations**: The decision of the first situation determines the path of the next (contained/escalated), and the decision of the second determines the last (calm/under pressure). There is no right/wrong answer — but **realistic consequences**.
5. **Performance Review**: A comprehensive report evaluating performance in the situations, showing a compatibility index with the job, in addition to an analysis of top skills, skills to develop, work style, and a suggested learning path supported by a career coach's message.

> **Disclaimer:** This result is guiding and does not represent a final decision regarding the user's academic or professional future.

## Error Handling

- Missing or corrupted data file → Clear Arabic message instead of crashing.
- Field/job ID not found → Message + safe return button.
- Empty answer → "Write your decision or choose one of the suggestions to continue" alert.
- Duplicate submission for the same situation → Protected (decision is evaluated only once).
- AI call failure → Automatic return to the local engine.
- Any unexpected error during presentation → Safe recovery to the fields list.

## CareerTwin AI Team

- **Salama Alhajeri** — Team Lead & Project Coordinator
  Team leadership, task distribution, following up on schedule and deliverables, and coordinating between all parts of the project.

- **Alanoud Almazrouei** — AI & Product Development Lead
  Platform and prototype development, AI integration, CareerTwin features and simulation experience design, and ensuring the technical and functional coherence of the solution.

- **Shamma Almansoori** — Research, Data & Impact Lead
  Problem and root cause analysis, data and evidence collection and documentation, target audience and competitor study, and defining impact measurement indicators.

- **Maryam Almansoori** — UX, Business & Presentation Lead
  User journey and experience, business model and sustainability plan, roadmap, and organizing the final presentation and pitch.

**Our Goal:** Developing a smart experience that helps youth experience the job before choosing it and making a more conscious career decision.

---
---

# توأمك المهني — CareerTwin AI (Streamlit)

تمثل هذه النسخة نموذج العمل الأولي (MVP) الذي يشمل ويُعالج كافة عمليات المنصة من التهيئة إلى التقييم النهائي. منصّة استكشاف مهني تضعك داخل **يوم عمل افتراضي** في الوظيفة التي تفكّر بها:
تواجه ثلاثة مواقف مترابطة، تتخذ قرارات، ترى نتائجها الواقعية، ثم تحصل على
**مؤشر توافق مبدئي خاص بالوظيفة المحددة** مع تقرير مهارات كامل.

- **10 مجالات مهنية × 3 وظائف فريدة** = 30 وظيفة، كلها **متاحة للتجربة** بالكامل.
- **واجهة مستخدم تفاعلية (Immersive UI):** تصميم عصري مريح يحاكي المستقبل مع تأثيرات بصرية جذابة وتجربة غامرة (Time-tunnel Effect).
- عربي أولاً مع تخطيط RTL كامل، وتبديل فوري إلى الإنجليزية.
- **وضع العرض (Demo Mode)** يعمل بالكامل بدون إنترنت وبدون مفتاح API.
- **وضع الذكاء الاصطناعي (Live AI Mode)** اختياري عبر OpenAI أو Azure OpenAI،
  مع عودة تلقائية صامتة إلى المحرّك المحلي عند أي فشل — التجربة لا تتوقف أبداً.

---

## التشغيل السريع / Quick start

```bash
# 1) داخل مجلد المشروع
cd career_twin

# 2) (اختياري) بيئة افتراضية
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3) تثبيت المتطلبات
pip install -r requirements.txt

# 4) التشغيل
python -m streamlit run app.py
```

يفتح التطبيق على `http://localhost:8501`. لا يحتاج أي إعداد إضافي —
وضع العرض جاهز فوراً ويمكن للمحكّمين إكمال التجربة كاملة دون اتصال.

## اختيار الوضع تلقائي

لا يوجد أي مفتاح أو إعداد ظاهر للمستخدم: عند توفر إعدادات API صالحة يعمل
وضع الذكاء الاصطناعي تلقائياً وتظهر شارة صغيرة «المحاكاة الذكية مفعّلة»؛
وعند غيابها أو فشل الاتصال يعمل وضع العرض المحلي تلقائياً وتكتمل التجربة
كاملة دون أي انقطاع. للاختبار فقط، يوجد تحكم يدوي مخفي داخل الشريط الجانبي
المطوي تحت «إعدادات العرض التجريبي».

## تفعيل الذكاء الاصطناعي

انسخ `.env.example` إلى `.env` ثم عبّئ أحد الخيارين:

```bash
cp .env.example .env
```

| المتغير | الوصف |
|---|---|
| `OPENAI_API_KEY` | مفتاح OpenAI (الخيار الأول) |
| `OPENAI_MODEL` | اسم النموذج (افتراضياً `gpt-4o-mini`) |
| `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_DEPLOYMENT` | مفاتيح وإعدادات منصة Microsoft Foundry / Azure OpenAI (تُستخدم تلقائياً عند توفرها) |

لا تُوضع المفاتيح داخل الكود إطلاقاً، والمنصة مهيأة للاتصال المباشر بمفاتيح Azure و Foundry. عند فشل الاتصال بالنموذج لأي سبب،
يُقيَّم القرار بالمحرّك المحلي وتظهر ملاحظة صغيرة — دون صفحة فارغة
ودون منع المستخدم من إنهاء المحاكاة.

## بنية المشروع

```text
career_twin/
├── app.py                 # الواجهة، التنقّل، استضافة الألعاب (Tornado) وإدارة الحالة
├── requirements.txt
├── README.md
├── .env.example
├── components/            # لوحة تحكم الطالب (Dashboard)، التهيئة (Onboarding)، والمراحل الدراسية
├── data/
│   └── careers.json       # بيانات المجالات، الوظائف، المواقف، وأوزان التقييم
├── static/                # ملفات ألعاب المحاكاة المصدّرة (مثل Godot)
├── services/
│   ├── ai_service.py      # وضع الذكاء الاصطناعي + التحقق من صحة الرد
│   ├── scoring.py         # مراجعة الأداء (Performance Review) وإصدار التقرير النهائي
│   └── demo_engine.py     # محرّك العرض المحلي والتقييم السريع
├── utils/
│   ├── game_server.py     # خادم محلي لاستضافة الألعاب مع دعم SharedArrayBuffer
│   └── styles.py          # الهوية البصرية والتصميم
└── assets/                # شعارات وصور واجهة المستخدم
```

## كيف تعمل المحاكاة

1. **التهيئة ولوحة التحكم (Dashboard & Onboarding)**: استكمال الملف التعريفي للطالب (بما في ذلك المرحلة الدراسية - Education Stage) والانتقال إلى لوحة تحكم مخصصة تتابع التقدم في الرحلة المهنية.
2. **ملف سريع**: خمسة أسئلة تُنتج ترشيحاً لثلاثة مجالات مهنية الأنسب لك (يمكن تجاوزها).
3. **لعبة محاكاة تفاعلية (Game Integration)**: تجربة اللعبة المبنية بمحرك خارجي (مثل Godot) لبعض الوظائف لاستكشاف بيئة العمل قبل بدء التقييم.
4. **يوم عمل من ثلاثة مواقف مترابطة**: قرار الموقف الأول يحدد مسار الموقف التالي (محتوى/متصاعد)، وقرار الثاني يحدد الأخير (هادئ/تحت ضغط). لا توجد إجابة صحيحة/خاطئة — بل **عواقب واقعية**.
5. **مراجعة الأداء والتقرير النهائي (Performance Review)**: تقرير شامل يقيّم الأداء في المواقف، ويعرض مؤشر التوافق مع الوظيفة، بالإضافة إلى تحليل أقوى المهارات، مهارات التطوير، أسلوب العمل، ومسار تعلّم مقترح مدعوم برسالة موجّه مهني.

> **تنويه:** هذه النتيجة إرشادية ولا تمثل قراراً نهائياً بشأن مستقبل
> المستخدم الأكاديمي أو المهني.

## معالجة الأخطاء

- ملف بيانات مفقود أو تالف → رسالة عربية واضحة بدل الانهيار.
- معرّف مجال/وظيفة غير موجود → رسالة + زر عودة آمن.
- إجابة فارغة → تنبيه «اكتب قرارك أو اختر أحد الاقتراحات للمتابعة».
- إرسال مكرر لنفس الموقف → محمي (يُقيَّم القرار مرة واحدة فقط).
- فشل استدعاء الذكاء الاصطناعي → عودة تلقائية للمحرّك المحلي.
- أي خطأ غير متوقع أثناء العرض → استرجاع آمن إلى قائمة المجالات.

## فريق توأمك المهني | CareerTwin AI

- **سلامة الهاجري** — Team Lead & Project Coordinator
  قيادة الفريق، توزيع المهام، متابعة الجدول والتسليمات، والتنسيق بين جميع أجزاء المشروع.

- **العنود المزروعي** — AI & Product Development Lead
  تطوير المنصة والنموذج الأولي، تكامل الذكاء الاصطناعي، تصميم خصائص CareerTwin وتجربة المحاكاة، وضمان ترابط الحل تقنياً ووظيفياً.

- **شما المنصوري** — Research, Data & Impact Lead
  تحليل المشكلة والأسباب الجذرية، جمع وتوثيق البيانات والأدلة، دراسة الفئة المستهدفة والمنافسين، وتحديد مؤشرات قياس الأثر.

- **مريم المنصوري** — UX, Business & Presentation Lead
  رحلة وتجربة المستخدم، نموذج العمل وخطة الاستدامة، خارطة الطريق، وتنظيم العرض النهائي والـPitch.

**هدفنا:** تطوير تجربة ذكية تساعد الشباب على تجربة الوظيفة قبل اختيارها واتخاذ قرار مهني أكثر وعياً.

