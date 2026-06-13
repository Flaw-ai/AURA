import json
import random
import hashlib

subjects = [
    "the cat", "the dog", "a student", "my teacher", "the scientist",
    "the river", "the mountain", "the computer", "the phone", "the book",
    "the car", "the airplane", "the tree", "the flower", "the cloud",
    "the moon", "the sun", "the star", "the ocean", "the desert",
    "the man", "Alice", "Rudra", "Saee", "Mac"
]

verbs = [
    "runs", "jumps", "eats", "sleeps", "thinks", "writes", "reads",
    "paints", "sings", "dances", "drives", "flies", "grows", "shines", "glows", "flows", "melts", "freezes", "boils", "falls",
    "blows", "whispers", "screams", "laughs", "cries", "hugs", "kicks", "throws", "catches", "builds", "creates", "closes", 
    "opens", "starts", "stops", "wins", "loses", "finds", "loses", "gives", "takes", "loves", "hates", "breaks",
    "fixes", "teaches", "learns", "helps", "hurts", "saves", "wastes", "buys", "sells", "saves", "spends",
    "calls", "answers", "asks", "tells", "shows", "hides", "follows", "leads", "waits", "moves", "stays", "changes", "remains", "appears", "disappears", "arrives", "leaves", "enters", "exits", "travels", "stays", "works", "plays", "rests", "waits", "hurries", "slows", "speeds", "stops", "starts", "continues", "pauses", "resumes", "finishes", "begins", "ends", "sings", "dances", "laughs", "cries", "smiles", "frowns", "shouts", "whispers", "yells", "screams", "hugs", "kicks", "throws", "catches", "builds", "creates", "destroys", "fixes", "teaches", "learns", "helps", "hurts", "saves", "wastes", "buys", "sells", "saves", "spends", "calls", "answers", "asks", "tells", "shows", "hides", "follows", "leads", "waits", "moves", "stays", "changes", "remains", "appears", "disappears", "arrives", "leaves", "enters", "exits", "travels", "stays", "works", "plays", "rests", "waits", "hurries", "slows", "speeds", "stops", "starts", "continues", "pauses", "resumes", "finishes", "begins", "ends"
] 

adjectives = [
    "quick", "bright", "happy", "sad", "loud", "silent", "beautiful",
    "ugly", "strong", "weak", "ancient", "modern", "complex", "simple",
    "colorful", "dull", "hot", "cold", "fast", "slow", "tall", "short",
    "big", "small", "heavy", "light", "rich", "poor", "brave", "cowardly", "friendly", "hostile", "kind", "cruel", "generous", "selfish", "honest", "deceitful", "lonely", "social", "noisy", "quiet", "busy", "lazy", "strong", "weak", "healthy", "sick", "clean", "dirty", "new", "old", "young", "ancient", "modern", "famous", "unknown",
    "important", "trivial", "interesting", "boring", "funny", "serious", "dangerous", "safe", "expensive", "cheap", "valuable", "worthless"
]

objects = [
    "the ball", "the food", "the homework", "the song", "the picture",
    "the machine", "the formula", "the theory", "the experiment"
]

def generate_wrong_sentence():
    """Create a sentence with a deliberate grammar error."""
    s = random.choice(subjects)
    v = random.choice(verbs)
    o = random.choice(objects)
    error_type = random.choice(["sva", "tense", "double_negative", "word_order"])
    if error_type == "sva":
        if s in ["the cat","the dog","a student","my teacher","the scientist","the river","the mountain","the computer","the book","the tree","the flower","the cloud","the moon","the sun","the star","the ocean","the desert"]:
            wrong = f"{s} {v[:-1] if v.endswith('s') else v} {o}"
            correct = f"{s} {v} {o}"
        else:
            wrong = f"{s} {v}s {o}"
            correct = f"{s} {v} {o}"
    elif error_type == "tense":
        wrong = f"Yesterday, {s} {v} {o}"
        correct = f"Yesterday, {s} {v}ed {o}"
    elif error_type == "double_negative":
        wrong = f"{s} {v} not {o} nowhere"
        correct = f"{s} {v} not {o} anywhere"
    else:
        wrong = f"{v} {s} {o}?"
        correct = f"Does {s} {v} {o}?"
    return wrong, correct

def english_grammar_dynamic():
    wrong, correct = generate_wrong_sentence()
    explanation_parts = [
        f"The sentence '{wrong}' has an error. ",
        f"The correct version is '{correct}'. ",
        f"This is a common mistake with {random.choice(['subject-verb agreement','tense','negation','word order'])}. ",
        f"Remember: {random.choice(['verbs must match the subject','past actions need past tense','avoid double negatives','questions need auxiliary verbs'])}. ",
        f"Let's practice: try writing your own sentence correctly. ",
        f"If you need more help, just ask. "
    ]
    random.shuffle(explanation_parts)
    explanation = " ".join(explanation_parts[:random.randint(3,6)])
    return f"Correct this sentence: {wrong}", explanation + f" Short answer: {correct}"

vocab_list = []
for i in range(5000):
    word = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5,10)))
    meaning = f"a {random.choice(['type of','quality of','action of','state of'])} {random.choice(['being','doing','thinking','moving'])}"
    vocab_list.append((word, meaning))

def english_vocab_dynamic():
    word, meaning = random.choice(vocab_list)
    sentence_templates = [
        f"The {random.choice(adjectives)} {random.choice(subjects)} {random.choice(verbs)} {word}ly.",
        f"Her {word} {random.choice(verbs)} everyone.",
        f"The {word} of the situation was {random.choice(adjectives)}.",
    ]
    example = random.choice(sentence_templates)
    explanation = random_paragraph(
        f"The word '{word}' means {meaning}.",
        [f"It is derived from {random.choice(['Latin','Greek','Old English'])}.", f"Synonyms include {random.choice(['similar','related'])} terms."],
        example
    )
    return f"Define and use the word '{word}' in a sentence.", explanation + f" Short answer: {word} means {meaning}."

def random_paragraph(topic, key_points, example):
    starters = ["Let me explain. ", "Here's what you need to know: ", "This is important because "]
    para = random.choice(starters) + topic + " "
    if key_points:
        para += random.choice(key_points) + " "
    if example:
        para += f"For example, {example}. "
    para += "Keep practicing and you'll master it. "
    while len(para) < 200:
        para += "Let me know if you have any questions. "
    return para

essay_topics = [
    "climate change", "artificial intelligence", "importance of reading", 
    "online privacy", "mental health awareness", "sustainable living",
    "space exploration", "women empowerment", "digital divide"
] * 10

essay_tips = [
    "Start with a hook like a surprising fact.",
    "Use transition words: however, therefore, moreover.",
    "Each paragraph should have one main idea.",
    "Conclude by restating your thesis in new words."
]

def english_essay_dynamic():
    topic = random.choice(essay_topics)
    tip = random.choice(essay_tips)
    outline = ["Introduction", random.choice(["Causes","Examples","Benefits"]), 
               random.choice(["Effects","Counter‑arguments","Personal story"]), 
               "Conclusion"]
    para = random_paragraph(
        f"To write an essay on '{topic}', follow this structure: {' → '.join(outline)}. ",
        [f"Tip: {tip}.", "Always plan before writing."],
        f"For example, your introduction could ask: 'What if {topic} continues unchecked?'"
    )
    return f"Help me write an essay on '{topic}'.", para + " Short answer: Use the structure above."

generators = [english_grammar_dynamic, english_vocab_dynamic, english_essay_dynamic] * 20

seen_hashes = set()
out_file = "english_clean.jsonl"

with open(out_file, "w", encoding="utf-8") as f:
    count = 0
    while count < 500_000:
        gen = random.choice(generators)
        q, a = gen()
        if len(a) < 200 and "?" not in a[:50]:
            a += " " + random_paragraph("Remember", ["Practice is key"], "")
        h = hashlib.md5((q + a).encode()).hexdigest()
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry) + "\n")
        count += 1
        if count % 25000 == 0:
            print(f"Generated {count} unique English conversations...")

print(f"Done! {count} unique conversations saved to {out_file}")