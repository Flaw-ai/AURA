import json
import random
import hashlib
import math
import re
from typing import List, Dict, Tuple, Optional, Any
from copy import deepcopy

TARGET_SAMPLES = 80000
RANDOM_SEED = 42
MAX_WORKERS = 8
GUARD_RAIL_TOPICS = ["math", "logic", "science", "coding", "analogy", "planning", "counterfactual"]
DIFFICULTIES = ["basic", "intermediate", "hard"]

random.seed(RANDOM_SEED)

def estimate_difficulty(steps: int, has_branching: bool = False, uses_tools: bool = False) -> str:
    if steps <= 3 and not has_branching and not uses_tools:
        return "basic"
    if steps <= 6 and not uses_tools:
        return "intermediate"
    return "hard"

def format_cot(steps: List[str], final_answer: Any) -> str:
    cot = "<|begin_of_thought|>\n"
    for i, step in enumerate(steps, 1):
        cot += f"Step {i}: {step}\n"
    cot += "<|end_of_thought|>\n\n"
    cot += "<|begin_of_solution|>\n"
    cot += str(final_answer) + "\n"
    cot += "<|end_of_solution|>"
    return cot

def deduplicate_key(question: str, cot: str) -> str:
    return hashlib.sha256((question + cot).encode()).hexdigest()

def generate_math_problem(difficulty: str) -> Tuple[str, List[str], Any]:
    if difficulty == "basic":
        a, b, c = random.randint(1, 20), random.randint(1, 20), random.randint(1, 10)
        question = f"A farmer has {a} apples. He sells {b} apples and then buys {c} more. How many apples does he have now?"
        steps = [
            f"Start with {a} apples.",
            f"Subtract sold apples: {a} - {b} = {a - b} apples.",
            f"Add bought apples: {a - b} + {c} = {a - b + c} apples."
        ]
        answer = a - b + c
    elif difficulty == "intermediate":
        p, r, t = random.randint(1000, 10000), random.uniform(3, 8), random.randint(2, 5)
        r = round(r, 1)
        interest = round(p * (r / 100) * t, 2)
        question = f"A sum of Rs {p} is invested at {r}% per annum simple interest for {t} years. Calculate the interest and total amount."
        steps = [
            f"Simple interest formula: I = P × R × T / 100",
            f"I = {p} × {r} × {t} / 100",
            f"I = {p * r * t / 100:.2f} → {interest:.2f}",
            f"Amount = Principal + Interest = {p} + {interest:.2f} = {p + interest:.2f}"
        ]
        answer = {"interest": interest, "amount": round(p + interest, 2)}
    else:
        a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(-20, 20)
        while b*b - 4*a*c < 0:
            a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(-20, 20)
        disc = b*b - 4*a*c
        root1 = (-b + math.sqrt(disc)) / (2*a)
        root2 = (-b - math.sqrt(disc)) / (2*a)
        question = f"Solve the quadratic equation: {a}x² + {b}x + {c} = 0"
        steps = [
            f"Quadratic formula: x = [-b ± √(b² - 4ac)] / (2a)",
            f"a = {a}, b = {b}, c = {c}",
            f"Discriminant = b² - 4ac = {b*b} - {4*a*c} = {disc}",
            f"x₁ = [-{b} + √{disc}] / {2*a} = {root1:.2f}",
            f"x₂ = [-{b} - √{disc}] / {2*a} = {root2:.2f}"
        ]
        answer = [round(root1, 2), round(root2, 2)]
    return question, steps, answer

def math_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_math_problem(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "math",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

def generate_logic_puzzle(difficulty: str) -> Tuple[str, List[str], Any]:
    a_type = random.choice(["Knight", "Knave"])
    b_type = random.choice(["Knight", "Knave"])
    statements = {
        ("Knight", "Knight"): ("I am a Knight.", "He is a Knight."),
        ("Knight", "Knave"): ("I am a Knight.", "He is a Knave."),
        ("Knave", "Knight"): ("I am a Knave.", "He is a Knight."),
        ("Knave", "Knave"): ("I am a Knave.", "He is a Knave.")
    }
    stmt_a, stmt_b = statements[(a_type, b_type)]
    question = f"On an island of Knights (always tell truth) and Knaves (always lie), you meet two people A and B. A says: '{stmt_a}'. B says: '{stmt_b}'. Determine the types of A and B."
    steps = [
        f"Case 1: Assume A is Knight → A tells truth → '{stmt_a}' is true → means A is Knight (consistent) → then analyze B's statement.",
        f"B says: '{stmt_b}' → if B is Knight then statement true → leads to consistency or contradiction.",
        f"Case 2: Assume A is Knave → statement false → means A is not Knight (A is Knave consistent) → analyze B.",
        f"After checking both cases, only consistent assignment is: A is {a_type}, B is {b_type}."
    ]
    answer = f"A is {a_type}, B is {b_type}"
    if difficulty == "basic":
        colors = ["red", "blue", "green"]
        random.shuffle(colors)
        persons = ["Alice", "Bob", "Charlie"]
        question = f"Three friends each have a different favorite color: red, blue, green. Alice's favorite color is not blue. Bob's favorite color is green. What is each person's favorite color?"
        steps = [
            f"Bob's favorite is green.",
            f"Alice cannot be blue → Alice is red (since green taken).",
            f"Remaining color blue must be Charlie's."
        ]
        answer = {"Alice": "red", "Bob": "green", "Charlie": "blue"}
    return question, steps, answer

def logic_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_logic_puzzle(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "logic",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

def generate_science_problem(difficulty: str) -> Tuple[str, List[str], Any]:
    subjects = ["physics", "chemistry"]
    subject = random.choice(subjects)
    if subject == "physics" and difficulty in ["basic", "intermediate"]:
        m, v = random.randint(5, 50), random.randint(2, 20)
        ke = 0.5 * m * v**2
        question = f"An object of mass {m} kg moves with velocity {v} m/s. Calculate its kinetic energy."
        steps = [
            f"Kinetic energy formula: KE = ½ × m × v²",
            f"KE = 0.5 × {m} × ({v})²",
            f"KE = 0.5 × {m} × {v*v}",
            f"KE = {ke} J"
        ]
        answer = ke
    elif subject == "chemistry" and difficulty == "hard":
        mass = random.randint(10, 100)
        compound = "NaCl"
        molar_mass = 58.44
        moles = mass / molar_mass
        question = f"Calculate the number of moles in {mass} grams of NaCl (molar mass = 58.44 g/mol)."
        steps = [
            f"Moles = given mass / molar mass",
            f"Moles = {mass} g / {molar_mass} g/mol",
            f"Moles = {moles:.2f} mol"
        ]
        answer = round(moles, 2)
    else:
        question = "Why does ice float in water? Explain the molecular reason."
        steps = [
            "Water molecules form a crystalline lattice when frozen.",
            "This lattice has more space between molecules than liquid water.",
            "Lower density → ice floats."
        ]
        answer = "Ice is less dense than liquid water due to hydrogen bonding creating an open hexagonal lattice."
    return question, steps, answer

def science_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_science_problem(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "science",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

def generate_coding_reasoning(difficulty: str) -> Tuple[str, List[str], Any]:
    tasks = ["debug", "complexity", "trace"]
    task = random.choice(tasks)
    if task == "debug" and difficulty != "hard":
        code = "def sum_list(lst):\n    total = 0\n    for i in range(len(lst)+1):\n        total += lst[i]\n    return total"
        bug = "off-by-one error: loop goes to len(lst) instead of len(lst)-1"
        question = f"Find and fix the bug in this Python function:\n```python\n{code}\n```\nThe function should return the sum of all elements in a list."
        steps = [
            "Understand function: supposed to sum elements of a list.",
            "Loop range: range(len(lst)+1) generates indices 0..len(lst).",
            "Last index len(lst) is out of bounds (list indices 0..len(lst)-1).",
            "Fix: change to range(len(lst)).",
            f"Corrected code: {code.replace('len(lst)+1', 'len(lst)')}"
        ]
        answer = "range(len(lst))"
    elif task == "complexity":
        question = "What is the time complexity of bubble sort in the worst case? Explain your reasoning."
        steps = [
            "Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if out of order.",
            "In worst case (reverse sorted), each pass moves one element to its correct position.",
            "Total comparisons = n + (n-1) + ... + 1 = n(n-1)/2.",
            "This is O(n²)."
        ]
        answer = "O(n²)"
    else:
        question = "Trace the execution of this recursive function for n=3:\n```python\ndef fact(n):\n    if n <= 1: return 1\n    return n * fact(n-1)\n```"
        steps = [
            "fact(3): 3 ≤ 1? no → return 3 * fact(2)",
            "fact(2): 2 ≤ 1? no → return 2 * fact(1)",
            "fact(1): 1 ≤ 1? yes → return 1",
            "Back substitute: fact(2) = 2 * 1 = 2",
            "fact(3) = 3 * 2 = 6"
        ]
        answer = 6
    return question, steps, answer

def coding_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_coding_reasoning(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "coding",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

analogy_templates = [
    ("atom", "solar system", "nucleus/sun, electrons/planets", "nucleus attracts electrons like sun attracts planets"),
    ("cell", "factory", "nucleus/office, mitochondria/power plant", "organelles as specialized departments"),
    ("internet", "nervous system", "routers/neurons, data/impulses", "information flow parallels neural signals")
]

def generate_analogy(difficulty: str) -> Tuple[str, List[str], Any]:
    template = random.choice(analogy_templates)
    domain1, domain2, mapping, explanation = template
    question = f"Explain how the {domain1} is analogous to the {domain2}. Provide at least two specific parallels."
    steps = [
        f"Identify core elements of {domain1}: {mapping.split(',')[0].split('/')[0]}",
        f"Match each to corresponding element in {domain2}: {mapping.split(',')[0].split('/')[1]}",
        f"Further matching: {mapping.split(',')[1]}",
        f"The relationship shows {explanation}"
    ]
    answer = explanation
    return question, steps, answer

def analogy_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_analogy(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "analogy",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

def generate_planning(difficulty: str) -> Tuple[str, List[str], Any]:
    if difficulty == "basic":
        question = "Plan a 3‑day itinerary for a trip to a historical city. Include one major landmark per day and one meal suggestion."
        steps = [
            "Day 1: Arrival, check-in, visit Red Fort (Delhi). Lunch at local chaat shop.",
            "Day 2: Visit Qutub Minar and Humayun's Tomb. Dinner at a traditional restaurant.",
            "Day 3: Explore Chandni Chowk market, depart after lunch."
        ]
        answer = "3‑day itinerary: Day1: Red Fort + chaat; Day2: Qutub Minar + Tomb; Day3: Chandni Chowk."
    else:
        question = "You are planning a wedding for 200 guests on a ₹10 lakh budget. Outline a step‑by‑step plan including venue, catering, decor, and entertainment."
        steps = [
            "Step 1: Allocate budget (~40% venue, 30% catering, 20% decor, 10% entertainment).",
            "Step 2: Book venue 6 months in advance.",
            "Step 3: Finalize caterer with menu tasting.",
            "Step 4: Hire decorator according to theme.",
            "Step 5: Book DJ or live band.",
            "Step 6: Create guest list and send invites."
        ]
        answer = "Budget‑conscious plan with early booking and prioritized spending."
    return question, steps, answer

def planning_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_planning(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "planning",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

def generate_counterfactual(difficulty: str) -> Tuple[str, List[str], Any]:
    scenarios = [
        ("What would happen if the Earth stopped rotating abruptly?", 
         "1. Everything on surface would continue moving east at high speed.",
         "2. Massive tsunamis and earthquakes due to momentum.",
         "3. One side would face constant heat, other eternal cold."),
        ("If antibiotics had never been discovered, how would medicine differ?",
         "1. High mortality from bacterial infections (pneumonia, sepsis).",
         "2. Surgery would remain extremely risky.",
         "3. Focus would be on sanitation and natural antimicrobials.")
    ]
    scenario = random.choice(scenarios)
    question = scenario[0]
    steps = list(scenario[1:4])
    answer = scenario[-1][:100] + "..."
    return question, steps, answer

def counterfactual_generator(count: int) -> List[Dict]:
    samples = []
    for _ in range(count):
        diff = random.choice(DIFFICULTIES)
        q, steps, ans = generate_counterfactual(diff)
        cot = format_cot(steps, ans)
        samples.append({
            "domain": "counterfactual",
            "question": q,
            "cot": cot,
            "answer": ans,
            "difficulty": diff,
            "steps": len(steps)
        })
    return samples

def generate_dataset() -> List[Dict]:
    generators = [
        (math_generator, 15000),
        (logic_generator, 12000),
        (science_generator, 12000),
        (coding_generator, 15000),
        (analogy_generator, 10000),
        (planning_generator, 8000),
        (counterfactual_generator, 8000)
    ]
    all_samples = []
    seen_keys = set()
    for gen_func, target in generators:
        print(f"Generating {target} samples from {gen_func.__name__}...")
        samples = gen_func(target)
        for sample in samples:
            key = deduplicate_key(sample["question"], sample["cot"])
            if key not in seen_keys:
                seen_keys.add(key)
                all_samples.append(sample)
        print(f"  -> Kept {len(samples)} after dedup (total {len(all_samples)} so far)")
        if len(all_samples) >= TARGET_SAMPLES:
            break
    if len(all_samples) > TARGET_SAMPLES:
        all_samples = random.sample(all_samples, TARGET_SAMPLES)
    return all_samples

def save_dataset(samples: List[Dict], filename: str = "reasoning_dataset_80k.jsonl"):
    with open(filename, 'w', encoding='utf-8') as f:
        for sample in samples:
            answer_str = json.dumps(sample["answer"], ensure_ascii=False) if isinstance(sample["answer"], (list, dict)) else str(sample["answer"])
            record = {
                "instruction": sample["question"],
                "output": sample["cot"],
                "domain": sample["domain"],
                "difficulty": sample["difficulty"],
                "num_reasoning_steps": sample["steps"]
            }
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(f"Saved {len(samples)} examples to {filename}")

def show_sample(samples: List[Dict], n: int = 3):
    for i in range(n):
        sample = samples[i]
        print(f"\n----- Example {i+1} ({sample['domain']}, {sample['difficulty']}) -----")
        print(f"Q: {sample['question']}")
        print(f"COT: {sample['cot'][:300]}...")
        print(f"Answer: {sample['answer']}")

if __name__ == "__main__":
    print("Generating DeepSeek‑style reasoning dataset...")
    dataset = generate_dataset()
    save_dataset(dataset)
    show_sample(dataset)
    print("\n✅ Done. Dataset ready for training.")