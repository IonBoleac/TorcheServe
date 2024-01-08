import torch.nn as nn
import torch.nn.functional as F

class LogisticRegression(nn.Module):
    def __init__(self):
        super(LogisticRegression,self).__init__()
        self.f1 = nn.Linear(100, 1000)
        self.f2 = nn.Linear(1000, 2)

    def forward(self,x):
        x = self.f1(x)
        x = F.leaky_relu(x)
        x = F.dropout(x, p = 0.2)
        x = self.f2(x)
        return  F.sigmoid(x)
    
    