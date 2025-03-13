# 第一种GPU训练方式
import torch.cuda
import torchvision
from torch import nn
import torch
from torch.nn import Conv2d
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from model import *
import time
# 准备数据集
train_data = torchvision.datasets.CIFAR10('./datasets/CIFAR10', train=True, transform=torchvision.transforms.ToTensor(),
                                          download=True)
test_data = torchvision.datasets.CIFAR10('./datasets/CIFAR10', train=False, transform=torchvision.transforms.ToTensor(),
                                         download=True)
train_data_size = len(train_data)
test_data_size = len(test_data)

print("训练集数据量为: {}\n".format(train_data_size))
print("测试集数据量为: {}\n".format(test_data_size))

# 用dataloader加载数据集
train_data_loader = DataLoader(train_data, batch_size=64)
test_data_loader = DataLoader(test_data, batch_size=64)


# 搭建神经网络
tudui = Tudui()
if torch.cuda.is_available():
    tudui = tudui.cuda()

# 损失函数
loss_fn = nn.CrossEntropyLoss()
if torch.cuda.is_available():
    loss_fn = loss_fn.cuda()
learning_rate = 0.01
optim = torch.optim.SGD(params=tudui.parameters(), lr=learning_rate)

# 训练设置网络的参数
# 记录训练次数
total_train_step = 0
# 记录测试次数
total_test_step = 0
# 训练轮数
epochs = 10

# 添加tensorboard
writer = SummaryWriter('train_log')


for epoch in range(epochs):
    start_time = time.time()
    # 训练阶段
    train_loader = tqdm(
        train_data_loader,
        desc=f"Epoch {epoch + 1}/{epochs} [Train]",
        leave=True  # 关闭进度条保留
    )
    tudui.train()# 非必须
    total_train_loss = 0
    for data in train_loader:
        imgs, targets = data
        if torch.cuda.is_available():
            imgs = imgs.cuda()
            targets = targets.cuda()
        optim.zero_grad()
        outputs = tudui(imgs)
        loss = loss_fn(outputs, targets)
        loss.backward()
        optim.step()

        total_train_loss += loss.item()
        train_loader.set_postfix(loss=loss.item())  # 实时更新损失
    end_time = time.time()
    total_time = end_time - start_time
    format_time = time.strftime("%H:%M:%S", time.gmtime(total_time))
    # 使用tqdm安全输出
    tqdm.write(f"\nEpoch {epoch + 1}/{epochs} - Train Loss: {total_train_loss:.4f}   Training time:{format_time}")

    # 测试阶段
    test_loader = tqdm(
        test_data_loader,
        desc=f"Epoch {epoch + 1}/{epochs} [Test]",
        leave=True
    )
    # 测试步骤开始
    tudui.eval()# 非必须
    total_test_loss = 0
    total_correct = 0
    with torch.no_grad():
        for data in test_loader:
            imgs, targets = data
            if torch.cuda.is_available():
                imgs = imgs.cuda()
                targets = targets.cuda()
            outputs = tudui(imgs)
            loss = loss_fn(outputs, targets)
            total_test_loss += loss.item()

            # 计算正确率
            preds = outputs.argmax(dim=1)
            correct = (preds == targets).sum().item()
            total_correct += correct

            test_loader.set_postfix(loss=loss.item())

    # 输出测试结果
    test_accuracy = total_correct / test_data_size
    tqdm.write(f"Epoch {epoch + 1}/{epochs} - Test Loss: {total_test_loss:.4f}")
    tqdm.write(f"Test Accuracy: {test_accuracy * 100:.2f}%\n")

    # 保存模型
    torch.save(tudui, f'./run/tudui_{epoch}.pth')

writer.close()
