import torch
import torchvision
from torch import nn
from torch.nn import Conv2d
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

dataset = torchvision.datasets.CIFAR10("./datasets/CIFAR10", train=False, transform=torchvision.transforms.ToTensor(),
                                       download=True)

dataloader = DataLoader(dataset, 64)


class Tudui(nn.Module):

    def __init__(self):
        super(Tudui, self).__init__()
        self.cov1 = Conv2d(3, 3, kernel_size=3, stride=1, padding=0)

    def forward(self,x):
        x = self.cov1(x)
        return x


tudui = Tudui()

writer = SummaryWriter("logs")
step = 0
for data in dataloader:
    imgs, targets = data
    output = tudui(imgs)
    writer.add_images("test_conv2d", output, step)
    step += 1

writer.close()
