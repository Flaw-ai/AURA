import json
import random
import re

step_phrases = [
    "Step 1: ", "First, ", "We begin by ", "Notice that ", "Always start with ",
    "The key idea: ", "Let's think: ", "According to the rule, ", "Recall that "
]
mistake_phrases = [
    "A common mistake is to forget the sign. ",
    "Many students incorrectly add instead of subtract. ",
    "Do not forget to take the square root. ",
    "Be careful: the units must match. ",
    "Often, students misapply the distributive property. ",
    "Remember: percent means per hundred. ",
    "A frequent error is to divide before subtracting. ",
    "Do not confuse median with mean. "
]

def random_step(text):
    return random.choice(step_phrases) + text

def random_mistake():
    return random.choice(mistake_phrases)

templates = []

for _ in range(100):
    templates.append({
        "generator": lambda: gen_linear(),
        "topic": "algebra"
    })

def gen_linear():
    a = random.randint(1, 12)
    b = random.randint(-20, 20)
    c = random.randint(-30, 30)
    while (c - b) % a != 0 or abs((c-b)//a) > 50:
        c = random.randint(-30, 30)
    x_val = (c - b) // a
    q = f"Solve: {a}x + {b} = {c}"
    step1 = f"Add { -b } to both sides: {a}x = {c - b}" if b < 0 else f"Subtract {b} from both sides: {a}x = {c - b}"
    step2 = f"Divide both sides by {a}: x = {x_val}"
    mistake = random_mistake()
    short = f"x = {x_val}"
    detailed = f"{random_step(step1)} {random_step(step2)} {mistake} Check: {a}*{x_val}+{b}={a*x_val+b} = {c}. Short answer: {short}"
    return q, detailed

def gen_factor_simple():
    p = random.randint(-12, 12)
    q = random.randint(-12, 12)
    if p == 0 or q == 0:
        p, q = random.randint(1,10), random.randint(1,10)
    b = p + q
    c = p * q
    q_str = f"Factorise: x² + {b}x + {c}" if b >= 0 else f"Factorise: x² - {abs(b)}x + {c}"
    if p < 0 and q < 0:
        fact = f"(x - {abs(p)})(x - {abs(q)})"
    elif p < 0:
        fact = f"(x - {abs(p)})(x + {q})"
    elif q < 0:
        fact = f"(x + {p})(x - {abs(q)})"
    else:
        fact = f"(x + {p})(x + {q})"
    step = f"Find two numbers whose product is {c} and sum is {b}. Those numbers are {p} and {q}. So {fact}."
    mistake = random_mistake()
    detailed = f"{random_step(step)} {mistake} Expand to verify: {fact} = {q_str[10:]}. Short: {fact}"
    return q_str, detailed

def gen_quad_lead():
    a = random.randint(2, 6)
    b = random.randint(-15, 15)
    c = random.randint(-15, 15)
    while b*b - 4*a*c < 0 or (b*b - 4*a*c)**0.5 != int((b*b - 4*a*c)**0.5):
        a, b, c = random.randint(2,6), random.randint(-15,15), random.randint(-15,15)
    disc = int((b*b - 4*a*c)**0.5)
    root1 = (-b + disc)/(2*a)
    root2 = (-b - disc)/(2*a)
    if root1 != int(root1) or root2 != int(root2):
        return gen_factor_simple()
    root1, root2 = int(root1), int(root2)
    q = f"Solve: {a}x² + {b}x + {c} = 0"
    fact = f"{a}(x - {root1})(x - {root2})" if root1==root2 else f"{a}(x - {root1})(x - {root2})"
    step = f"Using quadratic formula: x = [{-b} ± √({b}² - 4*{a}*{c})]/(2*{a}) = [{-b} ± {disc}]/{2*a}. So x = {root1} or {root2}."
    detailed = f"{random_step(step)} {random_mistake()} Short: x = {root1}, {root2}"
    return q, detailed

def gen_pythagoras():
    legs = [(3,4),(5,12),(6,8),(7,24),(8,15),(9,12),(12,16),(5,12),(8,6),(9,40)]
    leg = random.choice(legs)
    ab, bc = leg
    ac = int((ab**2+bc**2)**0.5)
    q = f"In right triangle ABC, right‑angled at B, AB = {ab} cm, BC = {bc} cm. Find AC."
    step = f"Pythagoras: AC² = AB² + BC² = {ab}² + {bc}² = {ab**2} + {bc**2} = {ac**2}. So AC = √{ac**2} = {ac} cm."
    detailed = f"{random_step(step)} {random_mistake()} Short: AC = {ac} cm"
    return q, detailed

def gen_mean():
    n = random.randint(4, 10)
    numbers = [random.randint(1, 100) for _ in range(n)]
    total = sum(numbers)
    mean_val = total / n
    if mean_val == int(mean_val):
        mean_val = int(mean_val)
    else:
        mean_val = round(mean_val, 1)
    q = f"Find the mean of: {', '.join(map(str, numbers))}"
    step = f"Sum = {total}, count = {n}. Mean = {total}/{n} = {mean_val}."
    detailed = f"{random_step(step)} {random_mistake()} Short: {mean_val}"
    return q, detailed

def gen_percent():
    obtained = random.randint(10, 90)
    total = random.randint(obtained+10, 120)
    perc = round((obtained/total)*100, 1)
    q = f"A student scores {obtained} out of {total}. What is the percentage?"
    step = f"Percentage = (obtained/total)×100 = ({obtained}/{total})×100 = {perc}%."
    detailed = f"{random_step(step)} {random_mistake()} Short: {perc}%"
    return q, detailed

def gen_triangle_angles():
    r1 = random.randint(1,5)
    r2 = random.randint(1,5)
    r3 = random.randint(1,5)
    total = r1+r2+r3
    factor = 180 / total
    a1, a2, a3 = int(r1*factor), int(r2*factor), int(r3*factor)
    q = f"Angles of a triangle are in the ratio {r1}:{r2}:{r3}. Find each angle."
    step = f"Let angles be {r1}x, {r2}x, {r3}x. Sum = {total}x = 180 → x = {180/total:.1f}. Angles: {a1}°, {a2}°, {a3}°."
    detailed = f"{random_step(step)} {random_mistake()} Short: {a1}°, {a2}°, {a3}°"
    return q, detailed

def gen_trig_sincos():
    sinvals = [(3,5),(5,13),(7,25),(8,17),(1,2)]
    num, den = random.choice(sinvals)
    cosval = (den**2 - num**2)**0.5 / den
    if cosval == int(cosval):
        cosval = int(cosval)
    cos_str = f"{int(cosval)}/{den}" if cosval==int(cosval) else f"√{den**2 - num**2}/{den}"
    q = f"If sin θ = {num}/{den} and θ is acute, find cos θ."
    step = f"sin²θ + cos²θ = 1 → cos²θ = 1 - ({num}/{den})² = 1 - {num**2}/{den**2} = {den**2 - num**2}/{den**2}. So cos θ = √({den**2 - num**2}/{den**2}) = {cos_str}."
    detailed = f"{random_step(step)} {random_mistake()} Short: {cos_str}"
    return q, detailed

def gen_loss_cp():
    sp = random.randint(200, 1000)
    loss_percent = random.randint(5, 25)
    cp = sp * 100 / (100 - loss_percent)
    cp = round(cp, 2)
    q = f"A shopkeeper sells an item for ₹{sp} at a loss of {loss_percent}%. Find the cost price."
    step = f"SP = CP × (100 - loss%)/100 → {sp} = CP × ({100-loss_percent}/100) → CP = {sp} × 100 / {100-loss_percent} = ₹{cp}."
    detailed = f"{random_step(step)} {random_mistake()} Short: ₹{cp}"
    return q, detailed

def gen_cube_vol():
    side = random.randint(2, 15)
    vol = side**3
    q = f"Find the volume of a cube with side {side} cm."
    step = f"Volume = side³ = {side}³ = {vol} cm³."
    detailed = f"{random_step(step)} {random_mistake()} Short: {vol} cm³"
    return q, detailed

def gen_sets():
    total = random.randint(50, 200)
    A = random.randint(20, total-20)
    B = random.randint(20, total-20)
    both = random.randint(5, min(A,B)-5)
    neither = total - (A + B - both)
    q = f"In a class of {total} students, {A} like cricket, {B} like football, and {both} like both. How many like neither?"
    step = f"n(C∪F) = {A} + {B} - {both} = {A+B-both}. Neither = total - {A+B-both} = {neither}."
    detailed = f"{random_step(step)} {random_mistake()} Short: {neither}"
    return q, detailed

generators = [
    gen_linear, gen_factor_simple, gen_quad_lead, gen_pythagoras,
    gen_mean, gen_percent, gen_triangle_angles, gen_trig_sincos,
    gen_loss_cp, gen_cube_vol, gen_sets
]

def generate_one():
    gen = random.choice(generators)
    q, detailed = gen()
    return {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": detailed}]}

def save_jsonl(n=30000, filename="math.jsonl"):
    with open(filename, "w") as f:
        for i in range(n):
            entry = generate_one()
            f.write(json.dumps(entry) + "\n")
            if (i+1) % 5000 == 0:
                print(f"Generated {i+1} examples...")
    print(f"Done! Saved {n} examples to {filename}")

if __name__ == "__main__":
    save_jsonl(30000)