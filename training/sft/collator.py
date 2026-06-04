from transformers import DataCollatorForLanguageModeling

class SFTCollator(DataCollatorForLanguageModeling):
    def __init__(self, tokenizer, mlm=False, mlm_probability=0.15):
        super().__init__(
            tokenizer=tokenizer,
            mlm=mlm,
            mlm_probability=mlm_probability
        )
        
    def build_collator(self, tokenizer):
        return SFTCollator(
            tokenizer=tokenizer,
            mlm=self.mlm,
            mlm_probability=self.mlm_probability
        )