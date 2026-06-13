import hashlib
import json

seen = set()

kept = 0
removed = 0

with open("english.jsonl", "r", encoding="utf-8") as inp, \
     open("english_clean.jsonl", "w", encoding="utf-8") as out:

    for line in inp:
        try:
            obj = json.loads(line)

            text = json.dumps(
                obj,
                sort_keys=True,
                ensure_ascii=False
            ).strip()

            h = hashlib.md5(text.encode("utf-8")).hexdigest()

            if h not in seen:
                seen.add(h)
                out.write(line)
                kept += 1
            else:
                removed += 1

        except Exception:
            continue

print(f"Kept: {kept:,}")
print(f"Removed: {removed:,}")
print(f"Final: {kept:,}")