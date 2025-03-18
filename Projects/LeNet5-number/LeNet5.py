import torch
import torchvision.transforms
from torch import nn

class LeNet_5(nn.Module):
    def __init__(self):
        super(LeNet_5, self).__init__()
        self.model = nn.Sequential(
            # 修改输入通道数为 1（如果是单通道图像）
            nn.Conv2d(1, 6, kernel_size=3, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),

            nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),

            # 调整全连接层输入维度
            nn.Flatten(),
            nn.Linear(16 * 6 * 6, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 10)
        )

    def forward(self, input):
        output = self.model(input)
        return output

if __name__ == '__main__':
    tudui = LeNet_5()
    # 修改输入张量形状为 (批量大小, 通道数, 高度, 宽度)
    input = torch.ones(64, 1, 32, 32)
    output = tudui(input)
    print(output.shape)