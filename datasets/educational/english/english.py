import json
import random
import hashlib

subjects = ["I", "You", "He", "She", "It", "We", "They", "The dog", "My friend", "The teacher", "Students"]
verbs_present = ["like", "play", "run", "eat", "sleep", "read", "write", "speak"]
verbs_past = ["liked", "played", "ran", "ate", "slept", "read", "wrote", "spoke"]
objects = ["cricket", "football", "books", "food", "fast", "loudly", "well"]

def generate_grammar():
    rule = random.choice(["sva", "tense", "pronoun", "preposition"])
    if rule == "sva":
        s = random.choice(subjects)
        v = random.choice(verbs_present)
        if s in ["He", "She", "It", "The dog", "My friend", "The teacher"]:
            wrong = f"{s} {v} {random.choice(objects)}."
            correct = f"{s} {v}s {random.choice(objects)}."
        else:
            wrong = f"{s} {v}s {random.choice(objects)}."
            correct = f"{s} {v} {random.choice(objects)}."
    elif rule == "tense":
        s = random.choice(subjects)
        v_past = random.choice(verbs_past)
        wrong = f"Yesterday, {s} {random.choice(verbs_present)} {random.choice(objects)}."
        correct = f"Yesterday, {s} {v_past} {random.choice(objects)}."
    elif rule == "pronoun":
        wrong = f"Me and {random.choice(subjects)} are going."
        correct = f"{random.choice(subjects)} and I are going."
    else:
        wrong = f"She is married with a {random.choice(['doctor','engineer','teacher'])}."
        correct = f"She is married to a {random.choice(['doctor','engineer','teacher'])}."
    return f"Correct: {wrong}", f"Correct sentence: {correct}. Short answer: {correct}"

vocab = [
    ("meticulous", "very careful and precise"), ("benevolent", "kind and helpful"),
    ("arduous", "difficult and tiring"), ("luminous", "bright and shining"),
    ("candid", "truthful and straightforward"), ("diligent", "hardworking"),
    ("ephemeral", "lasting a short time"), ("gregarious", "sociable"),
    ("hackneyed", "overused and clichéd"), ("juxtapose", "place side by side"),
    ("mellifluous", "sweet sounding"), ("nefarious", "wicked"),
    ("obfuscate", "to confuse"), ("prolific", "producing many works"),
    ("quintessential", "perfect example"), ("ubiquitous", "everywhere"),
    ("verbose", "wordy"), ("zealous", "enthusiastic"),
    ("serendipity", "finding something good without looking for it"), ("catharsis", "emotional release"),
    ("epiphany", "sudden realization"), ("labyrinth", "a complicated maze"),
    ("panacea", "a solution for all problems"), ("quagmire", "a difficult situation"),
    ("rendezvous", "a meeting at an agreed time and place"), ("sagacious", "wise"),
    ("taciturn", "reserved or uncommunicative"), ("vicarious", "experienced through another"),
    ("whimsical", "playfully quaint or fanciful"), ("xenophobia", "fear of foreigners"),
    ("yonder", "at some distance in the direction indicated"), ("zenith", "the highest point")
]
import string
for _ in range(200 - len(vocab)):
    fake_word = ''.join(random.choices(string.ascii_lowercase, k=8))
    vocab.append((fake_word, "a made‑up word for demonstration"))

def generate_vocab():
    word, meaning = random.choice(vocab)
    templates = [
        f"The {{adj}} student always completed her work on time.",
        f"His {{adj}} smile lit up the room.",
        f"The climb was {{adj}} but rewarding.",
        f"She gave a {{adj}} answer that everyone appreciated.",
        f"His {{adj}} behaviour surprised everyone.",
        f"The {{adj}} process took several hours."
    ]
    sentence = random.choice(templates).format(adj=word)
    return f"Use the word '{word}' in a sentence.", f"Example: {sentence} Meaning: {meaning}. Short answer: {sentence}"

essay_topics = [
    "Climate Change", "Impact of Social Media", "Importance of Education",
    "My Role Model", "Digital India", "Cleanliness Campaign", "Value of Time",
    "Pollution in Cities", "Women Empowerment", "Online Learning vs Classroom",
    "Save Water", "Plastic Ban", "Cyberbullying", "Artificial Intelligence",
    "Yoga and Health", "Swachh Bharat Mission", "Favourite Festival",
    "A Visit to a Historical Place", "Importance of Sports", "Global Warming",
    "Unity in Diversity", "The Power of Reading", "Honesty is the Best Policy",
    "My Dream Career", "The Influence of Cinema"
]
essay_types = ["argumentative", "descriptive", "narrative", "expository"]
essay_tips = [
    "Start with a hook", "Use transition words", "Provide examples",
    "Address counterarguments", "Conclude strongly", "Use a quote",
    "Tell a personal story", "Define key terms"
]

def generate_essay():
    topic = random.choice(essay_topics)
    etype = random.choice(essay_types)
    tip = random.choice(essay_tips)
    outline = {
        "argumentative": "Intro → Claim → Evidence → Counter‑argument → Rebuttal → Conclusion",
        "descriptive": "Sensory details → Physical description → Emotional impact → Reflection",
        "narrative": "Setting → Characters → Conflict → Climax → Resolution",
        "expository": "Introduction → Main idea 1 → Main idea 2 → Main idea 3 → Conclusion"
    }[etype]
    return f"Help me write an {etype} essay on '{topic}'.", f"Outline: {outline}. Tip: {tip}. Short answer: Follow the outline."

literature = [
    ("Macbeth", "Shakespeare", "ambition and guilt"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "the American Dream"),
    ("To Kill a Mockingbird", "Harper Lee", "racial injustice"),
    ("The Guide", "R.K. Narayan", "personal transformation"),
    ("Godan", "Premchand", "rural poverty"),
    ("The Diary of a Young Girl", "Anne Frank", "hope during war"),
    ("Oliver Twist", "Charles Dickens", "child labour"),
    ("The Story of My Experiments with Truth", "Gandhi", "non-violence"),
    ("1984", "George Orwell", "totalitarianism"),
    ("Pride and Prejudice", "Jane Austen", "social class and marriage"),
    ("The Alchemist", "Paulo Coelho", "following dreams"),
    ("The White Tiger", "Aravind Adiga", "class struggle"),
    ("Animal Farm", "George Orwell", "corruption of power"),
    ("The God of Small Things", "Arundhati Roy", "family and forbidden love"),
    ("The Namesake", "Jhumpa Lahiri", "identity and belonging"),
    ("The Inheritance of Loss", "Kiran Desai", "globalisation"),
    ("The Adventures of Huckleberry Finn", "Mark Twain", "race and freedom"),
    ("Wuthering Heights", "Emily Brontë", "obsession and revenge"),
    ("The Catcher in the Rye", "J.D. Salinger", "alienation"),
    ("Malgudi Days", "R.K. Narayan", "everyday life in India"),
    ("The Room on the Roof", "Ruskin Bond", "coming of age"),
    ("The Blue Umbrella", "Ruskin Bond", "greed and generosity"),
    ("The Hungry Tide", "Amitav Ghosh", "environment and politics"),
    ("The Lowland", "Jhumpa Lahiri", "family and revolution"),
    ("The Ministry of Utmost Happiness", "Arundhati Roy", "love and resistance"),
    ("The Guide", "R.K. Narayan", "personal transformation"),
    ("The Shadow Lines", "Amitav Ghosh", "memory and history"),
    ("The God of Small Things", "Arundhati Roy", "family and forbidden love"),
    ("The White Tiger", "Aravind Adiga", "class struggle"),
    ("The Inheritance of Loss", "Kiran Desai", "globalisation"),
    ("The Namesake", "Jhumpa Lahiri", "identity and belonging"),
]
while len(literature) < 50:
    literature.append((f"Book{len(literature)}", f"Author{len(literature)}", "a universal theme"))

lit_questions = [
    "What is the main theme of {book}?",
    "Who wrote {book}?",
    "Describe the character of {char} in {book}.",
    "What is the setting of {book}?",
    "Explain the title significance of {book}."
]

def generate_literature():
    book, author, theme = random.choice(literature)
    qtype = random.choice(lit_questions)
    if "character" in qtype:
        char = "the protagonist"
        q = qtype.format(char=char, book=book)
        a = f"In '{book}', {char} struggles with {theme}. Short answer: See explanation."
    elif "who wrote" in qtype:
        q = qtype.format(book=book)
        a = f"'{book}' was written by {author}. Short answer: {author}"
    elif "theme" in qtype:
        q = qtype.format(book=book)
        a = f"The main theme of '{book}' is {theme}. Short answer: {theme}"
    elif "setting" in qtype:
        q = qtype.format(book=book)
        a = f"The setting of '{book}' is {random.choice(['rural India','1920s America','Victorian England','a fictional town'])}. Short answer: setting varies."
    else:
        q = qtype.format(book=book)
        a = f"The title '{book}' is significant because it reflects {theme}. Short answer: reflects {theme}"
    return q, a

def random_name():
    first = random.choice(["Aarav", "Vihaan", "Ananya", "Diya", "Arjun", "Sanya", "Rohan", "Isha"])
    last = random.choice(["Sharma", "Verma", "Patel", "Kumar", "Singh", "Reddy"])
    return f"{first} {last}"

def random_place():
    return random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Jaipur", "Lucknow"])

def random_number():
    return str(random.randint(100, 999))

def generate_passage():
    template = random.choice([
        "{name} from {place} collected {num} plastic bottles in one week. This helped reduce waste by {num2} kilograms. The local council praised {name} for this effort.",
        "The {animal} population in {place} has increased by {num}% over five years. Scientists believe this is because of better protection laws.",
        "A new study shows that students who read for {num} minutes daily score {num2}% higher in exams. Reading improves vocabulary and concentration."
    ])
    name = random_name()
    place = random_place()
    num = random_number()
    num2 = random_number()
    animal = random.choice(["tiger", "elephant", "peacock", "dolphin"])
    passage = template.format(name=name, place=place, num=num, num2=num2, animal=animal)
    q_template = random.choice([
        f"What did {name} collect?",
        f"Where does {name} live?",
        f"How much did waste reduce?",
        f"Why did the animal population increase?",
        f"What benefit of reading is mentioned?"
    ])
    if "collect" in q_template:
        answer = "plastic bottles"
    elif "live" in q_template:
        answer = place
    elif "waste reduce" in q_template:
        answer = f"{num2} kilograms"
    elif "animal population" in q_template:
        answer = "better protection laws"
    else:
        answer = f"{num}% higher exam scores"
    full_q = f"Read the passage: '{passage}'\\n\\nQuestion: {q_template}"
    return full_q, f"From the passage: {answer}. Short answer: {answer}"

generators = [
    generate_grammar, generate_vocab, generate_essay,
    generate_literature, generate_passage
]

seen_hashes = set()
output_file = "english.jsonl"

with open(output_file, "w") as f:
    count = 0
    while count < 15000:
        gen = random.choice(generators)
        q, a = gen()
        h = hashlib.md5((q + a).encode()).hexdigest()
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry) + "\n")
        count += 1
        if count % 1000 == 0:
            print(f"Generated {count} unique examples...")

print(f"Done! Saved {count} unique conversations to {output_file}")