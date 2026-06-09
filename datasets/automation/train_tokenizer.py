from pathlib import Path

def train_tokenizer():
    tokenizer_file = Path("models/flaw/tokenizer.json")

    if tokenizer_file.exists():
        print("Tokenizer already exists.")
        return

    print("Tokenizer training not yet implemented.")
    print("Create training/scripts/train_tokenizer.py")

if __name__ == "__main__":
    train_tokenizer()