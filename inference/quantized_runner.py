import torch
from quantization.quantize import (Quantizer)

class QuantizedRunner:
    def __init__(self, model):
        self.model = model
        self.quantizer = (Quantizer())

    def load_int8(self):
        self.model = (self.quantizer.int8(self.model))
        return self.model

    def load_fp16(self):
        self.model = (self.quantizer.fp16(self.model))
        return self.model

    def summary(self):
        return self.quantizer.summary(self.model)

if __name__ == "__main__":
    print("Quantized runner ready.")