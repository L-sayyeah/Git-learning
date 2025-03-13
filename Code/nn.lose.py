import torch
from torch import nn

inputs = torch.tensor([1, 2, 3], dtype=torch.float)

targets = torch.tensor([1, 2, 5], dtype=torch.float)

inputs = torch.reshape(inputs, (1, 1, 1, 3))
targets = torch.reshape(targets, (1, 1, 1, 3))

# reduction计算lose的方式，默认为mean
loss = nn.L1Loss(reduction='sum')
print(loss(inputs, targets))

loss = nn.MSELoss()
print(loss(inputs, targets))

# 分类问题的lose function ，参数为batch-size  ,  class
x = torch.tensor([0.1, 0.2, 0.3])
y = torch.tensor([1])
x = torch.reshape(x, (1, 3))
res_cross = nn.CrossEntropyLoss()
print(res_cross(x, y))
