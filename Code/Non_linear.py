# 非线性激活Relu为例子,sigmod

import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset = torchvision.datasets.CIFAR10('./datasets/CIFAR10', train=0, transform=torchvision.transforms.ToTensor(), download=True)

dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

class Tudui(nn.Module):
    def __init__(self):
        super(Tudui, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=0)
        self.max_pooling = nn.MaxPool2d(3, stride=1)
        self.relu = nn.ReLU()

    def forward(self, input):
        output = self.conv2d(input)
        output = self.relu(output)
        output = self.max_pooling(output)
        return output


tudui = Tudui()

writer = SummaryWriter('logs')
step = 0
for data in dataloader:
    imgs, targets = data
    output = tudui(imgs)
    writer.add_images("Relu", output, step)
    step += 1

writer.close()
