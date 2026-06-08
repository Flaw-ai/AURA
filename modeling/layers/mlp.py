import torch
import torch.nn as nn

class FlawMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.fc1 = nn.Linear(config.hidden_size, config.hidden_size * 4)
        self.fc2 = nn.Linear(config.hidden_size * 4, config.hidden_size)
        self.activation = nn.GELU()

    def gate_proj(self, x):
        return self.fc1(x)

    def up_proj(self, x):
        return self.fc1(x)

    def down_proj(self, x):
        return self.fc2(x)
    
    def SiLU(self, x):
        return x * torch.sigmoid(x)
    
    def gelu(self, x):
        return 0.5 * x * (1 + torch.tanh(torch.sqrt(2 / torch.pi) * (x + 0.044715 * torch.pow(x, 3))))
    
    def swish(self, x):
        return x * torch.sigmoid(x)
    
    def forward(self, x):
        x = self.up_proj(x)
        x = self.SiLU(x)
        x = self.down_proj(x)
        return x