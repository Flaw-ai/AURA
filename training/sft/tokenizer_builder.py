from transformers import AutoTokenizer

class TokenizerBuilder:
    def __init__(self, model_name):
        self.model_name = model_name
        
    def build_tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_name)
        
    def load_tokenizer(self, save_path):
        return AutoTokenizer.from_pretrained(save_path)

    def add_special_tokens(self, tokenizer, special_tokens):
        tokenizer.add_special_tokens(special_tokens)

    def save_tokenizer(self, tokenizer, save_path):
        tokenizer.save_pretrained(save_path)
        
    def special_tokens_dict(self):
        return {
            "additional_special_tokens": [
                "<|user|>",
                "<|assistant|>"
            ]
        }