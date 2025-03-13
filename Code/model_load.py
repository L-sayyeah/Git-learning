import torch
from torch import nn

vgg161 = torch.load('./models/vgg161.pth')
# print(vgg161)

vgg162 = torch.load('./models/vgg162.pth')
# print(vgg162)

# 加上源码后就可以加载了
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv2d = nn.Conv2d(3, 3, 3, 1)


    def forward(self,input):
        output = self.conv2d(input)
        return output

# 直接load不行，需要源码
mymode = torch.load('./models/mymodel.pth')
print(mymode)