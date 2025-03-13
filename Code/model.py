import torch
from torch import nn
from torch.nn import Conv2d

class Tudui(nn.Module):

    def __init__(self):
        super(Tudui, self).__init__()

        self.model1 = nn.Sequential(
            Conv2d(3, 32, 5, padding=2),
            nn.MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            nn.MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        x = self.model1(x)
        return x


if __name__ == '__main__':
    tudui = Tudui()
    input = torch.ones(64, 3, 32, 32)
    output = tudui(input)
    print(output.shape)