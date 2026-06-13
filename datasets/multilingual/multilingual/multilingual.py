import json
import random

languages = [
    "es", "fr", "de", "zh", "ar", "ru", "ja", "pt", "it", "nl", "ko", "tr", "pl", "vi", "th", "sw", "ta", "te", "bn", "ur"
]


responses = {
    "es": {
        "math_linear": lambda a,b,c,x: (
            f"Resolver para x: {a}x + {b} = {c}. Paso 1: Reste {b} de ambos lados: {a}x = {c-b}. "
            f"Paso 2: Divida entre {a}: x = {x}. Siempre verifique. Respuesta corta: x = {x}"
        ),
        "greeting": "¡Hola! ¿Cómo puedo ayudarte hoy?"
    },
    "fr": {
        "math_linear": lambda a,b,c,x: (
            f"Résoudre pour x : {a}x + {b} = {c}. Étape 1 : Soustrayez {b} des deux côtés : {a}x = {c-b}. "
            f"Étape 2 : Divisez par {a} : x = {x}. Réponse courte : x = {x}"
        ),
        "greeting": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    },
    "de": {
        "math_linear": lambda a,b,c,x: (
            f"Löse nach x auf: {a}x + {b} = {c}. Schritt 1: Subtrahiere {b} von beiden Seiten: {a}x = {c-b}. "
            f"Schritt 2: Teile durch {a}: x = {x}. Kurze Antwort: x = {x}"
        ),
        "greeting": "Hallo! Wie kann ich Ihnen heute helfen?"
    },
    "zh": {
        "math_linear": lambda a,b,c,x: (
            f"解方程: {a}x + {b} = {c}。步骤1：两边减去{b}：{a}x = {c-b}。步骤2：除以{a}：x = {x}。简短回答：x = {x}"
        ),
        "greeting": "你好！今天我可以如何帮助你？"
    },
    "ja": {
        "math_linear": lambda a,b,c,x: (
            f"xを解く: {a}x + {b} = {c}。ステップ1：両辺から{b}を引く: {a}x = {c-b}。ステップ2：{a}で割る: x = {x}。短い答え: x = {x}"
        ),
        "greeting": "こんにちは！今日どのようにお手伝いできますか？"
    },
    "ru": {
        "math_linear": lambda a,b,c,x: (
            f"Решите для x: {a}x + {b} = {c}. Шаг 1: Вычтите {b} из обеих частей: {a}x = {c-b}. "
            f"Шаг 2: Разделите на {a}: x = {x}. Короткий ответ: x = {x}"
        ),
        "greeting": "Привет! Как я могу вам помочь сегодня?"
    },
    "ar": {
        "math_linear": lambda a,b,c,x: (
            f"حل لـ x: {a}x + {b} = {c}. الخطوة 1: اطرح {b} من كلا الجانبين: {a}x = {c-b}. "
            f"الخطوة 2: اقسم على {a}: x = {x}. إجابة قصيرة: x = {x}"
        ),
        "greeting": "مرحبًا! كيف يمكنني مساعدتك اليوم؟"
    },
    "pt": {
        "math_linear": lambda a,b,c,x: (
            f"Resolver para x: {a}x + {b} = {c}. Passo 1: Subtraia {b} de ambos os lados: {a}x = {c-b}. "
            f"Passo 2: Divida por {a}: x = {x}. Resposta curta: x = {x}"
        ),
        "greeting": "Olá! Como posso ajudá-lo hoje?"
    },
    "it": {
        "math_linear": lambda a,b,c,x: (
            f"Risolvi per x: {a}x + {b} = {c}. Passo 1: Sottrai {b} da entrambe le parti: {a}x = {c-b}. "
            f"Passo 2: Dividi per {a}: x = {x}. Risposta breve: x = {x}"
        ),
        "greeting": "Ciao! Come posso aiutarti oggi?"
    },
    "nl": {
        "math_linear": lambda a,b,c,x: (
            f"Los op voor x: {a}x + {b} = {c}. Stap 1: Trek {b} van beide zijden af: {a}x = {c-b}. "
            f"Stap 2: Deel door {a}: x = {x}. Korte antwoord: x = {x}"
        ),
        "greeting": "Hallo! Hoe kan ik u vandaag helpen?"
    },
    "ko": {
        "math_linear": lambda a,b,c,x: (
            f"x를 풀어라: {a}x + {b} = {c}. 단계 1: 양변에서 {b}를 뺀다: {a}x = {c-b}. "
            f"단계 2: {a}로 나눈다: x = {x}. 짧은 답변: x = {x}"
        ),
        "greeting": "안녕하세요! 오늘 어떻게 도와드릴까요?"
    },
    "tr": {
        "math_linear": lambda a,b,c,x: (
            f"x için çöz: {a}x + {b} = {c}. Adım 1: Her iki yandan da {b}'yi çıkarın: {a}x = {c-b}. "
            f"Adım 2: {a}'ya bölün: x = {x}. Kısa yanıt: x = {x}"
        ),
        "greeting": "Merhaba! Bugün size nasıl yardımcı olabilirim?"
    },
    "pl": {
        "math_linear": lambda a,b,c,x: (
            f"Rozwiąż dla x: {a}x + {b} = {c}. Krok 1: Odejmij {b} od obu stron: {a}x = {c-b}. "
            f"Krok 2: Podziel przez {a}: x = {x}. Krótka odpowiedź: x = {x}"
        ),
        "greeting": "Cześć! Jak mogę ci dziś pomóc?"
    },
    "vi": {
        "math_linear": lambda a,b,c,x: (
            f"Giải cho x: {a}x + {b} = {c}. Bước 1: Trừ {b} từ cả hai bên: {a}x = {c-b}. "
            f"Bước 2: Chia cho {a}: x = {x}. Câu trả lời ngắn: x = {x}"
        ),
        "greeting": "Xin chào! Tôi có thể giúp gì cho bạn hôm nay?"
    },
    "th": {
        "math_linear": lambda a,b,c,x: (
            f"แก้สมการสำหรับ x: {a}x + {b} = {c}. ขั้นตอนที่ 1: ลบ {b} จากทั้งสองข้าง: {a}x = {c-b}. "
            f"ขั้นตอนที่ 2: หารด้วย {a}: x = {x}. คำตอบสั้น: x = {x}"
        ),
        "greeting": "สวัสดี! วันนี้ฉันสามารถช่วยคุณได้อย่างไร?"
    },
    "sw": {
        "math_linear": lambda a,b,c,x: (
            f"Suluhisha kwa x: {a}x + {b} = {c}. Hatua ya 1: Toa {b} kutoka kila upande: {a}x = {c-b}. "
            f"Hatua ya 2: Gawa kwa {a}: x = {x}. Jibu fupi: x = {x}"
        ),
        "greeting": "Habari! Sasa ninaweza kukusaidia?"
    },
    "ta": {
        "math_linear": lambda a,b,c,x: (
            f"x க்கு தீர்வு காண்க: {a}x + {b} = {c}. படிமுறை 1: இருபக்கமும் இருந்து {b}ஐ கழிக்கவும்: {a}x = {c-b}. "
            f"படிமுறை 2: {a}ஆல் வகுக்கவும்: x = {x}. சிறிய பதில்: x = {x}"
        ),
        "greeting": "ஹலோ! இன்று நீங்கள் எனக்கு எப்படி உதவலாம்?"
    },
    "te": {
        "math_linear": lambda a,b,c,x: (
            f"x కొరకు పరిష్కరించండి: {a}x + {b} = {c}. అధ్యయనం 1: రెండు వైపులనూ నువ్వు తీసుకోవడంతో సరిగడతను చేర్చడంలోకి ఉనది. "
            f"వదలబడదగలదనగలదనగలదనగలదనగలదనగలదనగలదనగలదనగలద"
        ),
        "greeting": "హలో! ఇకడ మరికళ మళ్ళతరబడతరబడతరబడతరబడతరబడతరబడతరబడతరబడత"
    },
    "bn": {
        "math_linear": lambda a,b,c,x: (
            f"x এর জন্য সমাধান করুন: {a}x + {b} = {c}. পদক্ষেপ 1: উভয় দিকের থেকেও বিয়োগ করুন, যা হবেঃ{a}x =.{c-b}. "
            f"পদক্ষেপ 2:{a}-এর সাথে ভাগ করুন, x =.{x}.সংক্ষিপ্ত উত্তর:{x}"
        ),
        "greeting": "হ্যালো!আজকেআপনারজন্যকিরুপেসহায়তাৎসহায়তাৎসহায়তাৎসহায়তাৎসহায়তাৎসহায়তাৎসহায়তাৎসহায়তাৎ"
    },
    "ur": {
        "math_linear": lambda a,b,c,x: (
            f"x کے لیے حل کریں: {a}x + {b} = {c}. مرحلہ 1: دونوں طرف سے {b} کو طے کریں: {a}x = {c-b}. "
            f"مرحلہ 2: {a} سے تقسیم کریں: x = {x}. مختصر جواب: x = {x}"
        ),
        "greeting": "سلام! آج آپ کیسے مدد کر سکتا ہوں?"
    }
}

def generate_multilingual():
    lang = random.choice(languages)
    if lang not in responses:
        return f"Greetings in {lang}", f"Hello from {lang} (detailed response would be added)"
    if random.random() < 0.1:
        return f"Hi in {lang}", responses[lang]["greeting"]
    else:
        a = random.randint(1,10)
        b = random.randint(-20,20)
        c = random.randint(-30,30)
        while (c - b) % a != 0:
            c = random.randint(-30,30)
        x = (c - b) // a
        q = f"Solve: {a}x + {b} = {c} (in {lang})"
        a_text = responses[lang]["math_linear"](a,b,c,x)
        return q, a_text

out_file = "multilingual.jsonl"
with open(out_file, "w") as f:
    for i in range(200000):
        q, a = generate_multilingual()
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry) + "\n")
        if (i+1) % 20000 == 0:
            print(f"Generated {i+1} multilingual examples...")
print("Multilingual 200k done.")