import torch
import torchvision
from torch import nn
from torch.nn import MaxPool2d, Conv2d
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

input = torchvision.datasets.CIFAR10("./datasets/CIFAR10", train=False, transform=torchvision.transforms.ToTensor(),
                                     download=True)
dataloader = DataLoader(dataset=input, batch_size=64, shuffle=True, num_workers=0)


class Tudui(nn.Module):
    def __init__(self):
        super(Tudui, self).__init__()
        self.conv2d = Conv2d(in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=0)
        self.max_pool = MaxPool2d(3, 1, ceil_mode=True)

    def forward(self, input):
        output = self.conv2d(input)
        output = self.max_pool(output)
        return output


tudui = Tudui()
writer = SummaryWriter('logs')
step = 0
for data in dataloader:
    imgs, targets = data
    output = tudui(imgs)
    writer.add_images('Pooling', output, step)
    step += 1

writer.close()
