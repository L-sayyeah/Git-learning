# Sequential可以打包多层，顺序执行每一层

import torch
import torchvision
from torch import nn
from torch.nn import Conv2d
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset = torchvision.datasets.CIFAR10('./datasets/CIFAR10', train=False, transform=torchvision.transforms.ToTensor(), download=True)
dataloader = DataLoader(dataset, batch_size=64)

class Tudui(nn.Module):

    def __init__(self):
        super(Tudui, self).__init__()
        # self.conv1 = Conv2d(3, 32, 5, padding=2)
        # self.maxpool1 = nn.MaxPool2d(2)
        # self.conv2 = Conv2d(32, 32, 5, padding=2)
        # self.maxpool2 = nn.MaxPool2d(2)
        # self.conv3 = Conv2d(32, 64,  5, padding=2)
        # self.maxpool3 = nn.MaxPool2d(2)
        # self.flatten = nn.Flatten()
        # self.liner1 = nn.Linear(1024, 64)
        # self.liner2 = nn.Linear(64, 10)

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


tudui = Tudui()
optim = torch.optim.SGD(tudui.parameters(), lr=0.01)
loss = nn.CrossEntropyLoss()
for epoch in range(20):
    running_loss = 0.0
    for data in dataloader:
        imgs, targets = data
        outputs = tudui(imgs)
        res_loss = loss(outputs, targets)
        optim.zero_grad()
        res_loss.backward()
        optim.step()
        running_loss += res_loss
    print("epoch:{}".format(epoch),running_loss)




