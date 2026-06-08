class ParameterCounter:
    def __init__(self, model):
        self.model = model

    def count_total(self):
        return sum(p.numel() for p in self.model.parameters())

    def count_trainable(self):
        return sum(p.numel() for p in self.model.parameters() if p.requires_grad)

    def count_frozen(self):
        return sum(p.numel() for p in self.model.parameters() if not p.requires_grad)

    def summary(self):
        print(f"Total parameters: {self.count_total()}")
        print(f"Trainable parameters: {self.count_trainable()}")
        print(f"Frozen parameters: {self.count_frozen()}")