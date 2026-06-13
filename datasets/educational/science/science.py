import json
import random

step_phrases = [
    "Step 1: ", "First, ", "We begin by ", "Recall that ", "The key idea is ",
    "Always start with ", "Let's apply the formula: "
]
mistake_phrases = [
    "A common mistake is forgetting to square the units.",
    "Many students confuse mass with weight.",
    "Do not forget to convert units (e.g., cm to m).",
    "Be careful: the formula requires the radius, not diameter.",
    "A frequent error is using the wrong formula entirely.",
    "Remember: density is mass divided by volume, not the reverse.",
    "Watch out: Ohm's law uses resistance in ohms and voltage in volts.",
    "Don't mix up speed and velocity – speed has no direction."
]

def random_step(text):
    return random.choice(step_phrases) + text

def random_mistake():
    return random.choice(mistake_phrases)

def make_response(answer_text, short_answer, mistake=""):
    mistake_text = mistake if mistake else random_mistake()
    return f"{random_step(answer_text)} {mistake_text} Short answer: {short_answer}"

def physics_ohms_law():
    r = random.randint(2, 100)
    v = random.randint(5, 200)
    i = round(v / r, 2)
    q = f"A resistor of {r} Ω is connected to a {v} V battery. Calculate the current flowing through the resistor."
    step = f"Use Ohm's law: V = I × R → I = V / R = {v} / {r} = {i} A."
    return q, make_response(step, f"{i} A")

def physics_density():
    m = random.randint(50, 1000)
    v = random.randint(10, 500)
    d = round(m / v, 2)
    q = f"A solid block has mass {m} g and volume {v} cm³. Determine its density."
    step = f"Density = mass / volume = {m} / {v} = {d} g/cm³."
    return q, make_response(step, f"{d} g/cm³")

def physics_speed():
    d = random.randint(100, 800)
    t = random.randint(2, 12)
    s = round(d / t, 1)
    q = f"A car travels {d} km in {t} hours. Find its average speed."
    step = f"Average speed = total distance / total time = {d} / {t} = {s} km/h."
    return q, make_response(step, f"{s} km/h")

def physics_force():
    m = random.randint(2, 50)
    a = random.randint(2, 15)
    f = m * a
    q = f"A mass of {m} kg is accelerated at {a} m/s². Compute the force applied."
    step = f"Newton's second law: F = m × a = {m} × {a} = {f} N."
    return q, make_response(step, f"{f} N", "Common mistake: using weight (mg) instead of mass.")

def physics_pressure():
    force = random.randint(100, 1000)
    area = random.randint(1, 50)
    p = round(force / area, 1)
    q = f"A force of {force} N acts on an area of {area} m². Find the pressure."
    step = f"Pressure = Force / Area = {force} / {area} = {p} Pa."
    return q, make_response(step, f"{p} Pa")

def physics_work():
    f = random.randint(50, 500)
    d = random.randint(2, 20)
    w = f * d
    q = f"A force of {f} N moves an object {d} m in the direction of force. Calculate work done."
    step = f"Work = Force × displacement = {f} × {d} = {w} J."
    return q, make_response(step, f"{w} J")

def physics_kinetic_energy():
    m = random.randint(1, 20)
    v = random.randint(2, 10)
    ke = 0.5 * m * v**2
    q = f"An object of mass {m} kg moves with velocity {v} m/s. Find its kinetic energy."
    step = f"Kinetic energy = ½ × m × v² = 0.5 × {m} × {v}² = {ke} J."
    return q, make_response(step, f"{ke} J")

def chemistry_balance_hydrogen():
    q = "Write the balanced chemical equation for the reaction between hydrogen and oxygen to form water."
    step = "Hydrogen + Oxygen → Water. Unbalanced: H₂ + O₂ → H₂O. Balance: 2H₂ + O₂ → 2H₂O."
    return q, make_response(step, "2H₂ + O₂ → 2H₂O")

def chemistry_balance_methane():
    q = "Write the balanced equation for the complete combustion of methane (CH₄)."
    step = "Methane + Oxygen → Carbon dioxide + Water. CH₄ + 2O₂ → CO₂ + 2H₂O."
    return q, make_response(step, "CH₄ + 2O₂ → CO₂ + 2H₂O")

def chemistry_acid_base():
    acid = random.choice(["HCl", "H₂SO₄", "HNO₃"])
    base = random.choice(["NaOH", "KOH", "Ca(OH)₂"])
    if (acid, base) in [("HCl","NaOH"), ("H₂SO₄","NaOH")]:
        salt = "NaCl" if acid=="HCl" else "Na₂SO₄"
    else:
        salt = "KCl" if base=="KOH" else "CaCl₂"
    q = f"{acid} reacts with {base}. Write the balanced neutralisation equation."
    step = f"Acid + Base → Salt + Water. {acid} + {base} → {salt} + H₂O. Balance if needed."
    return q, make_response(step, f"{acid} + {base} → {salt} + H₂O")

def chemistry_ph():
    ph = random.randint(0, 14)
    if ph < 7:
        ans = "acidic"
    elif ph == 7:
        ans = "neutral"
    else:
        ans = "basic"
    q = f"A solution has a pH value of {ph}. Is it acidic, basic, or neutral?"
    step = f"pH < 7 is acidic, pH = 7 neutral, pH > 7 basic. Here pH = {ph}, so it is {ans}."
    return q, make_response(step, ans)

def chemistry_atomic_structure():
    element = random.choice([("sodium",11, (2,8,1)), ("carbon",6,(2,4)), ("oxygen",8,(2,6)), ("chlorine",17,(2,8,7))])
    name, num, config = element
    q = f"An atom of {name} has atomic number {num}. Write its electronic configuration and find the number of valence electrons."
    config_str = ",".join(map(str, config))
    valence = config[-1]
    step = f"Electronic configuration: K={config[0]}, L={config[1]}" + (f", M={config[2]}" if len(config)>2 else "") + f". Valence electrons = {valence}."
    return q, make_response(step, f"Configuration: {config_str}, Valence electrons: {valence}")

def biology_photosynthesis():
    q = "Write the balanced chemical equation for photosynthesis."
    step = "Carbon dioxide + Water → Glucose + Oxygen. Balanced: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂."
    return q, make_response(step, "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂")

def biology_heart():
    q = "Name the four chambers of the human heart."
    step = "The heart has two upper chambers (atria) and two lower chambers (ventricles)."
    return q, make_response(step, "Right atrium, right ventricle, left atrium, left ventricle")

def biology_digestion():
    food = random.choice(["starch", "protein", "fat"])
    if food == "starch":
        enzyme = "salivary amylase (ptyalin)"
        site = "mouth"
    elif food == "protein":
        enzyme = "pepsin"
        site = "stomach"
    else:
        enzyme = "lipase"
        site = "small intestine"
    q = f"Which enzyme breaks down {food} in the human digestive system, and where is it produced?"
    step = f"{food.capitalize()} is broken down by {enzyme} in the {site}."
    return q, make_response(step, f"{enzyme} in {site}")

def biology_xylem():
    q = "What is the function of xylem in plants?"
    step = "Xylem transports water and dissolved minerals from the roots to the leaves."
    return q, make_response(step, "Transports water and minerals upward")

def biology_respiration():
    q = random.choice([
        "Explain aerobic respiration.",
        "Explain anaerobic respiration in human muscles during exercise."
    ])
    if "aerobic" in q:
        step = "Aerobic respiration uses oxygen to produce ATP, carbon dioxide, and water. Equation: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP."
        short = "Uses oxygen, produces CO₂, H₂O, and much ATP"
    else:
        step = "Anaerobic respiration in muscles produces lactic acid without oxygen, causing cramps."
        short = "Produces lactic acid without oxygen"
    return q, make_response(step, short)

science_generators = [
    physics_ohms_law, physics_density, physics_speed, physics_force, physics_pressure,
    physics_work, physics_kinetic_energy,
    chemistry_balance_hydrogen, chemistry_balance_methane, chemistry_acid_base, chemistry_ph,
    chemistry_atomic_structure,
    biology_photosynthesis, biology_heart, biology_digestion, biology_xylem, biology_respiration
]

out_file = "science.jsonl"
with open(out_file, "w") as f:
    for i in range(30000):
        gen = random.choice(science_generators)
        q, a = gen()
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry) + "\n")
        if (i+1) % 5000 == 0:
            print(f"Generated {i+1} science conversations...")
print("Done. Saved to", out_file)