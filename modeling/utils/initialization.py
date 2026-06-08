import torch.nn as nn
from .rmsnorm import RMSNorm

class InitializationUtils:
    @staticmethod
    def initialize_weights(module):
        if isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, RMSNorm):
            nn.init.ones_(module.weight)
        
    @staticmethod
    def initialize_embeddings(module):
        if isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
        
    @staticmethod
    def initialize_linear(module):
        if isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
            
    @staticmethod
    def initialize_rmsnorm(module):
        if isinstance(module, RMSNorm):
            nn.init.ones_(module.weight)
            