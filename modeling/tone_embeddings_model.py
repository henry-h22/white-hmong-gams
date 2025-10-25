import torch.nn as nn
import torch
torch.set_default_dtype(torch.float32)

class ToneFeedForward(nn.Module):
    def __init__(self, input_dim=50, output_dim=3072):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.Sigmoid(),
            nn.Linear(512, 2048),
            nn.Sigmoid(),
            nn.Linear(2048, output_dim)
        )
    
    def forward(self, x):
        return self.net(x)