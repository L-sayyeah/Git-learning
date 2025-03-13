import torch
import torchvision
from torch import nn
from torch.nn import Linear
from torch.utils.data import DataLoader

dataset = torchvision.datasets.CIFAR10('./datasets/CIFAR10', train=False, transform=torchvision.transforms.ToTensor(),
                                       download=True)

dataloader = DataLoader(dataset, batch_size=64, drop_last=True)


class Tudui(nn.Module):
    def __init__(self):
        super(Tudui, self).__init__()
        self.liner = Linear(196608, 10)

    def forward(self, input):
        output = self.liner(input)
        return output


tudui = Tudui()

for data in dataloader:
    imgs, targets = data

    # output = torch.reshape(imgs, (1, 1, 1, -1))
    output = torch.flatten(imgs)
    # 使用flatten可以变换为一行

    print((output.shape))
    output = tudui(output)
    print((output.shape))