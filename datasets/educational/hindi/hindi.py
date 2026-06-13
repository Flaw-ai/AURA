import json
import random

step_phrases_hindi = [
    "पहला कदम: ", "सबसे पहले, ", "हम यहाँ से शुरू करते हैं: ",
    "ध्यान दीजिए: ", "सूत्र लगाते हैं: ", "आइए हल करें: ",
    "गणना करते हैं: ", "याद रखिए: "
]
mistake_phrases_hindi = [
    "एक आम गलती: इकाइयों को भूल जाना। ",
    "अक्सर छात्र सूत्र उल्टा लगा देते हैं। ",
    "सावधान: यहाँ भाग करना है, गुणा नहीं। ",
    "कई बार विद्यार्थी चिह्न (sign) की गलती करते हैं। ",
    "ध्यान रखें: माध्यम निकालने के लिए सभी संख्याओं को जोड़ना और भाग देना होता है। ",
    "एक सामान्य त्रुटि: दशमलव की स्थिति गलत रखना। "
]

def random_step(text):
    return random.choice(step_phrases_hindi) + text

def random_mistake():
    return random.choice(mistake_phrases_hindi)

def make_response(step_text, short_answer, custom_mistake=""):
    mistake = custom_mistake if custom_mistake else random_mistake()
    return f"{random_step(step_text)} {mistake} संक्षिप्त उत्तर: {short_answer}"

def math_linear():
    a = random.randint(1, 12)
    b = random.randint(-20, 20)
    c = random.randint(-30, 30)
    while (c - b) % a != 0:
        c = random.randint(-30, 30)
    x_val = (c - b) // a
    q = f"हल कीजिए: {a}x + {b} = {c}"
    step = f"दोनों तरफ { -b } जोड़ें: {a}x = {c - b}। फिर दोनों तरफ {a} से भाग दें: x = {x_val}।"
    return q, make_response(step, f"x = {x_val}")

def math_factor_simple():
    p = random.randint(-12, 12)
    q_val = random.randint(-12, 12)
    while p == 0 or q_val == 0:
        p, q_val = random.randint(1,10), random.randint(1,10)
    b = p + q_val
    c = p * q_val
    q_str = f"गुणनखंड कीजिए: x² + {b}x + {c}" if b>=0 else f"गुणनखंड कीजिए: x² - {abs(b)}x + {c}"
    if p < 0 and q_val < 0:
        fact = f"(x - {abs(p)})(x - {abs(q_val)})"
    elif p < 0:
        fact = f"(x - {abs(p)})(x + {q_val})"
    elif q_val < 0:
        fact = f"(x + {p})(x - {abs(q_val)})"
    else:
        fact = f"(x + {p})(x + {q_val})"
    step = f"दो संख्याएँ खोजें जिनका गुणनफल {c} और योग {b} हो। वे संख्याएँ {p} और {q_val} हैं। अतः {fact}।"
    return q_str, make_response(step, fact)

def math_pythagoras():
    legs = [(3,4),(5,12),(6,8),(8,15),(9,12),(7,24)]
    ab, bc = random.choice(legs)
    ac = int((ab**2+bc**2)**0.5)
    q = f"समकोण त्रिभुज ABC में, B पर समकोण है। AB = {ab} cm, BC = {bc} cm। AC ज्ञात कीजिए।"
    step = f"पाइथागोरस प्रमेय से: AC² = AB² + BC² = {ab}² + {bc}² = {ab**2} + {bc**2} = {ac**2}। अतः AC = √{ac**2} = {ac} cm।"
    return q, make_response(step, f"AC = {ac} cm")

def math_mean():
    n = random.randint(4, 10)
    numbers = [random.randint(1, 100) for _ in range(n)]
    total = sum(numbers)
    mean_val = total / n
    mean_val = int(mean_val) if mean_val == int(mean_val) else round(mean_val, 1)
    q = f"इन संख्याओं का माध्य ज्ञात कीजिए: {', '.join(map(str, numbers))}"
    step = f"योग = {total}, पदों की संख्या = {n}। माध्य = योग/पद = {total}/{n} = {mean_val}।"
    return q, make_response(step, str(mean_val))

def math_percent():
    obtained = random.randint(10, 90)
    total = random.randint(obtained+10, 120)
    perc = round((obtained/total)*100, 1)
    q = f"एक छात्र को {total} में से {obtained} अंक मिले। प्रतिशत ज्ञात कीजिए।"
    step = f"प्रतिशत = (प्राप्तांक/कुल अंक) × 100 = ({obtained}/{total}) × 100 = {perc}%।"
    return q, make_response(step, f"{perc}%")

def science_ohms_law():
    v = random.randint(5, 200)
    r = random.randint(2, 100)
    i = round(v / r, 2)
    q = f"{r} Ω का एक प्रतिरोधक {v} V की बैटरी से जोड़ा गया है। धारा ज्ञात कीजिए।"
    step = f"ओम के नियम से: V = I × R ⇒ I = V / R = {v} / {r} = {i} A।"
    return q, make_response(step, f"{i} A")

def science_density():
    m = random.randint(50, 1000)
    v = random.randint(10, 500)
    d = round(m / v, 2)
    q = f"एक ठोस का द्रव्यमान {m} g और आयतन {v} cm³ है। घनत्व ज्ञात कीजिए।"
    step = f"घनत्व = द्रव्यमान/आयतन = {m}/{v} = {d} g/cm³।"
    return q, make_response(step, f"{d} g/cm³")

def science_photosynthesis():
    q = "प्रकाश संश्लेषण की संतुलित रासायनिक समीकरण लिखिए।"
    step = "कार्बन डाइऑक्साइड + जल → ग्लूकोज + ऑक्सीजन। संतुलित: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂।"
    return q, make_response(step, "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂")

def science_human_heart():
    q = "मानव हृदय के चार कक्षों के नाम लिखिए।"
    step = "हृदय में दो ऊपरी कक्ष (अलिंद) और दो निचले कक्ष (निलय) होते हैं।"
    return q, make_response(step, "दायाँ अलिंद, दायाँ निलय, बायाँ अलिंद, बायाँ निलय")

def sst_gandhi():
    q = "महात्मा गांधी ने नमक सत्याग्रह (दांडी मार्च) किस वर्ष किया था?"
    step = "गांधी जी ने 1930 में ब्रिटिश नमक कर के विरोध में दांडी मार्च किया।"
    return q, make_response(step, "1930")

def sst_taj_mahal():
    q = "ताजमहल किसने बनवाया था?"
    step = "ताजमहल मुगल सम्राट शाहजहाँ ने अपनी पत्नी मुमताज महल की याद में बनवाया था।"
    return q, make_response(step, "शाहजहाँ")

def sst_green_revolution():
    q = "हरित क्रांति का भारत में क्या प्रभाव पड़ा?"
    step = "हरित क्रांति से गेहूँ और चावल की उत्पादकता बहुत बढ़ी। इसके प्रमुख नेता डॉ. एम.एस. स्वामीनाथन थे।"
    return q, make_response(step, "खाद्यान्न उत्पादन में वृद्धि")

def sst_fundamental_rights():
    rights = ["समानता का अधिकार", "स्वतंत्रता का अधिकार", "शोषण के विरुद्ध अधिकार"]
    q = "भारतीय संविधान द्वारा दिए गए दो मौलिक अधिकारों के नाम लिखिए।"
    r1, r2 = random.sample(rights, 2)
    step = f"दो मौलिक अधिकार हैं: {r1} और {r2}।"
    return q, make_response(step, f"{r1}, {r2}")

all_generators = [
    math_linear, math_factor_simple, math_pythagoras, math_mean, math_percent,
    science_ohms_law, science_density, science_photosynthesis, science_human_heart,
    sst_gandhi, sst_taj_mahal, sst_green_revolution, sst_fundamental_rights
]

out_file = "hindi_10k_high_quality.jsonl"
with open(out_file, "w", encoding="utf-8") as f:
    for i in range(10000):
        gen = random.choice(all_generators)
        q, a = gen()
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        if (i+1) % 2000 == 0:
            print(f"✅ {i+1} हिंदी संवाद बन चुके हैं...")
print(f"\n🎉 पूर्ण! फ़ाइल सहेजी गई: {out_file}")