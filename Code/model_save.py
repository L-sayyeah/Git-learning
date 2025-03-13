import torch
import torchvision.models
from torch import nn

vgg16_model = torchvision.models.vgg16()

# 方式一：保存模型及其参数
torch.save(vgg16_model, './models/vgg161.pth')

# 方式二：只保存模型参数不保存模型结构
torch.save(vgg16_model.state_dict(), './models/vgg162.pth')

# 注意：使用方式一，保存自定义结构时，需要显示声明对应结构才能使用，比如把定义的代码放到load.py文件中
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv2d = nn.Conv2d(3, 3, 3, 1)


    def forward(self,input):
        output = self.conv2d(input)
        return output


mymodel = MyModel()
torch.save(mymodel, './models/mymodel.pth')
