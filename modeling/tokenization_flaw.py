from transformers import AutoTokenizer

class FlawTokenizer:
    def __init__(self, tokenizer_path):
        self.tokenizer = ( AutoTokenizer.from_pretrained(tokenizer_path))

    def encode(self, text):
        return self.tokenizer(text, return_tensors="pt")

    def decode(self, tokens):
        return self.tokenizer.decode(tokens, skip_special_tokens=True)