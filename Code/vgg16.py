# this is for test and some edit in VGG16

import torch
import torchvision.models
from torch import nn

vgg16_test = torchvision.models.vgg16()
print(vgg16_test)
# 访问到某个Sequential的某一层
print(vgg16_test.features[30])
# 添加层
# vgg16_test.add_module('add_liner', nn.Linear(1000, 10))
# 在某一个Sequential添加层
# vgg16_test.features.add_module('add_liner', nn.Linear(1000, 10))
# 修改某层
# vgg16_test.classifier[6] = nn.Linear(in_features=4096, out_features=10)
