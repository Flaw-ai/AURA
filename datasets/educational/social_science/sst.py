import json
import random

def history_rowlatt():
    return "What was the Rowlatt Act (1919)?", "Allowed detention without trial. Short answer: detention without trial"

def history_jallianwala():
    return "What happened at Jallianwala Bagh?", "General Dyer fired on unarmed crowd. Short answer: massacre"

def history_salt_march():
    return "Who led the Salt March and why?", "Gandhi against salt tax. Short answer: Gandhi"

def history_french_rev():
    causes = ["inequality", "taxation", "Enlightenment", "financial crisis"]
    return "What was a cause of the French Revolution?", f"{random.choice(causes).capitalize()}. Short answer: {random.choice(causes)}"

def geography_tropic():
    return "Latitude of Tropic of Cancer?", "23.5° N. Short answer: 23.5° N"

def geography_desert():
    deserts = [("Sahara", "Africa"), ("Gobi", "Asia"), ("Thar", "India")]
    name, cont = random.choice(deserts)
    return f"Where is {name} desert?", f"{name} in {cont}. Short answer: {cont}"

def civics_fundamental_rights():
    rights = ["Right to Equality", "Right to Freedom", "Right against Exploitation"]
    return "Name a Fundamental Right.", f"{random.choice(rights)}. Short answer: {random.choice(rights)}"

def economics_gdp():
    return "What does GDP stand for?", "Gross Domestic Product. Short answer: GDP"

sst_generators = [
    history_rowlatt, history_jallianwala, history_salt_march, history_french_rev,
    geography_tropic, geography_desert, civics_fundamental_rights, economics_gdp
]

out_file = "sst.jsonl"
with open(out_file, "w") as f:
    for i in range(15000):
        gen = random.choice(sst_generators)
        q, a = gen()
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry) + "\n")
        if (i+1) % 3000 == 0:
            print(f"SST: {i+1} generated")
print("Done.")