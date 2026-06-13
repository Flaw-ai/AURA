import json
import random
import hashlib

def python_variable():
    var_name = random.choice(["x", "count", "total", "score", "age", "name"])
    value = random.choice(["5", "3.14", "'hello'", "True", "[1,2,3]"])
    return f"What is a variable in Python? Give an example.", f"A variable is a named container. Example: {var_name} = {value}. Short answer: variable stores data."

def python_loop():
    n = random.randint(3, 10)
    return f"Write a Python for loop that prints numbers from 0 to {n-1}.", f"for i in range({n}): print(i). Short answer: for i in range({n}): print(i)"

def python_function():
    a, b = random.randint(1,20), random.randint(1,20)
    return f"Write a Python function that returns the sum of two numbers.", f"def add(x,y): return x+y. Example: add({a},{b}) = {a+b}. Short answer: def add(x,y): return x+y"

def python_list():
    ops = random.choice(["append", "remove", "sort"])
    if ops == "append":
        return f"How do you add an element to the end of a Python list?", f"Use the append() method. Example: my_list.append(5). Short answer: list.append(item)"
    elif ops == "remove":
        return f"How do you remove an element from a Python list by value?", f"Use the remove() method. Example: my_list.remove(3). Short answer: list.remove(value)"
    else:
        return f"How do you sort a Python list in ascending order?", f"Use the sort() method. Example: my_list.sort(). Short answer: list.sort()"

def cpp_variable():
    var_type = random.choice(["int", "float", "double", "char", "string"])
    var_name = random.choice(["x", "y", "value", "result"])
    return f"Declare a {var_type} variable in C++ named {var_name}.", f"{var_type} {var_name}; Short answer: {var_type} {var_name};"

def cpp_loop():
    n = random.randint(3, 10)
    return f"Write a C++ for loop that prints numbers 1 to {n}.", f"for(int i=1; i<={n}; i++) {{ cout << i; }} Short answer: for(int i=1; i<={n}; i++) {{ cout << i; }}"

def cpp_function():
    return f"Write a C++ function that returns the square of an integer.", f"int square(int x) {{ return x*x; }} Short answer: int square(int x) {{ return x*x; }}"

def ds_stack():
    ops = random.choice(["push", "pop", "LIFO"])
    if ops == "push":
        return f"In a stack, what operation adds an element?", f"Push. Short answer: push"
    elif ops == "pop":
        return f"In a stack, what operation removes the top element?", f"Pop. Short answer: pop"
    else:
        return f"What does LIFO stand for in stacks?", f"Last In First Out. Short answer: Last In First Out"

def ds_queue():
    ops = random.choice(["enqueue", "dequeue", "FIFO"])
    if ops == "enqueue":
        return f"In a queue, what operation adds an element?", f"Enqueue. Short answer: enqueue"
    elif ops == "dequeue":
        return f"In a queue, what operation removes the front element?", f"Dequeue. Short answer: dequeue"
    else:
        return f"What does FIFO stand for in queues?", f"First In First Out. Short answer: First In First Out"

def ds_linkedlist():
    return f"What is the advantage of a linked list over an array?", f"Dynamic size (no fixed capacity) and efficient insertions/deletions. Short answer: dynamic size."

def algo_binarysearch():
    arr = [random.randint(1,100) for _ in range(5)]
    arr.sort()
    target = random.choice(arr)
    return f"Explain binary search on sorted array. Example: find {target} in {arr}.", f"Binary search repeatedly divides the search interval in half. O(log n). Short answer: divide and conquer."

def algo_sort():
    sort_type = random.choice(["bubble", "selection", "insertion"])
    return f"Explain {sort_type} sort.", f"{sort_type.capitalize()} sort repeatedly places the next smallest/largest element. Short answer: comparison sort."

def web_html():
    tag = random.choice(["h1", "p", "a", "img"])
    if tag == "a":
        return f"Write HTML for a link to 'https://example.com'.", f"<a href='https://example.com'>Click here</a> Short answer: <a href='...'>text</a>"
    else:
        return f"Write HTML for a {tag} tag with sample content.", f"<{tag}>Sample content</{tag}> Short answer: <{tag}>...</{tag}>"

def web_css():
    prop = random.choice(["color", "font-size", "background-color"])
    val = random.choice(["red", "blue", "16px", "green"])
    return f"Write a CSS rule to set {prop}: {val}.", f"element {{ {prop}: {val}; }} Short answer: element {{ {prop}: {val}; }}"

def ai_definition():
    return f"What is Artificial Intelligence?", f"AI is the simulation of human intelligence by machines. Short answer: machines mimicking human intelligence."

def ai_ml():
    return f"What is the difference between AI and Machine Learning?", f"AI is the broad field; ML is a subset where systems learn from data. Short answer: ML is a subset of AI."

def ai_supervised():
    return f"Explain supervised learning with an example.", f"Supervised learning uses labeled data. Example: classifying emails as spam or not spam. Short answer: learning from labeled data."

cs_generators = [
    python_variable, python_loop, python_function, python_list,
    cpp_variable, cpp_loop, cpp_function,
    ds_stack, ds_queue, ds_linkedlist,
    algo_binarysearch, algo_sort,
    web_html, web_css,
    ai_definition, ai_ml, ai_supervised
]

def generate_cs():
    gen = random.choice(cs_generators)
    q, a = gen()
    return q, a

seen = set()
output_file = "cse.jsonl"

with open(output_file, "w") as f:
    count = 0
    while count < 20000:
        q, a = generate_cs()
        h = hashlib.md5((q + a).encode()).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        entry = {"messages": [{"role": "user", "content": q}, {"role": "assistant", "content": a}]}
        f.write(json.dumps(entry) + "\n")
        count += 1
        if count % 2000 == 0:
            print(f"Generated {count} CS examples...")
print(f"Done! {count} unique CS conversations saved.")