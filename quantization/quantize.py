import torch

class Quantizer:
    def __init__(self):
        pass

    def fp16(self, model):
        return model.half()

    def int8(self, model):
        return torch.quantization.quantize_dynamic(
            model,
            {torch.nn.Linear},
            dtype=torch.qint8
        )

    def summary(self, model):
        total = sum(
            p.numel()
            for p in model.parameters()
        )

        return {"parameters": total}

if __name__ == "__main__":
    print("Quantization module ready.")