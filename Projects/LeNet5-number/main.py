import time
import torch
from torch.utils.tensorboard import SummaryWriter
from torch import optim, nn
from torch.utils.data import DataLoader
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pre_process import load_images
from LeNet5 import LeNet_5

# 初始化最佳指标跟踪变量
best_accuracy = 0.0
best_class_acc = None
best_epoch = 0
device1 = torch.device("cpu")
device2 = torch.device("cuda:0")
# DataLoader加载数据
train_data, test_data = load_images()

test_data_size = len(test_data)
train_data_size = len(train_data)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64)

# 建立模型

model = LeNet_5()
if torch.cuda.is_available():
    model = model.to(device2)

# 定义损失函数
loss_fn = nn.CrossEntropyLoss()
if torch.cuda.is_available():
    loss_fn = loss_fn.to(device2)
learning_rate = 0.001
optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

epochs = 200
writer = SummaryWriter('logs')
num_classes = 10  # 根据你的数据集修改类别数量

for epoch in range(epochs):
    start_time = time.time()

    # ==================== 训练阶段 ====================
    model.train()
    total_train_loss = 0
    train_loader_tqdm = tqdm(
        train_loader,
        desc=f"Epoch {epoch + 1}/{epochs} [Train]",
        leave=False
    )

    for data in train_loader_tqdm:
        imgs, targets = data
        if torch.cuda.is_available():
            imgs = imgs.to(device2)
            targets = targets.to(device2)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = loss_fn(outputs, targets)
        loss.backward()
        optimizer.step()
        total_train_loss += loss.item()

    avg_train_loss = total_train_loss / len(train_loader)
    writer.add_scalar('Loss/Train', avg_train_loss, epoch)

    # ==================== 测试阶段 ====================
    model.eval()
    total_test_loss = 0
    total_correct = 0
    class_correct = torch.zeros(num_classes)
    class_total = torch.zeros(num_classes)

    test_loader_tqdm = tqdm(
        test_loader,
        desc=f"Epoch {epoch + 1}/{epochs} [Test]",
        leave=False
    )

    with torch.no_grad():
        for data in test_loader_tqdm:
            imgs, targets = data
            if torch.cuda.is_available():
                imgs = imgs.to(device2)
                targets = targets.to(device2)
            outputs = model(imgs)
            loss = loss_fn(outputs, targets)
            total_test_loss += loss.item()

            _, preds = torch.max(outputs, 1)
            correct = (preds == targets)
            total_correct += correct.sum().item()

            # 统计每个类别的正确预测数
            for c in range(num_classes):
                class_mask = (targets == c)
                class_correct[c] += correct[class_mask].sum().item()
                class_total[c] += class_mask.sum().item()

    avg_test_loss = total_test_loss / len(test_loader)
    test_accuracy = total_correct / test_data_size
    writer.add_scalar('Loss/Test', avg_test_loss, epoch)
    writer.add_scalar('Accuracy/Test', test_accuracy, epoch)

    # 记录每个类别的精度
    class_acc = (class_correct / (class_total + 1e-8))  # 防止除零
    for c in range(num_classes):
        writer.add_scalar(f'Accuracy/Class_{c}', class_acc[c], epoch)

    # 创建类别精度柱状图
    fig = plt.figure(figsize=(10, 5))
    plt.bar(range(num_classes), class_acc.numpy())
    plt.xlabel('Class')
    plt.ylabel('Accuracy')
    plt.title(f'Class Accuracy (Epoch {epoch + 1})')
    plt.xticks(range(num_classes))
    plt.ylim(0, 1)
    writer.add_figure('Class Accuracy Distribution', fig, epoch)
    plt.close(fig)

    # 更新最佳指标
    if test_accuracy > best_accuracy:
        best_accuracy = test_accuracy
        best_class_acc = class_acc.clone()
        best_epoch = epoch + 1

    # ==================== 控制台输出 ====================
    end_time = time.time()
    total_time = end_time - start_time
    format_time = time.strftime("%H:%M:%S", time.gmtime(total_time))

    print(f"\nEpoch {epoch + 1}/{epochs}")
    print(f"Train Loss: {avg_train_loss:.4f} | Test Loss: {avg_test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Class Accuracies: {[f'{acc:.2f}' for acc in class_acc.tolist()]}")
    print(f"Time Cost: {format_time}\n")

writer.close()

# 保存最佳结果的柱状图
plt.figure(figsize=(10, 5))
plt.bar(range(num_classes), best_class_acc.numpy())
plt.xlabel('Class')
plt.ylabel('Accuracy')
plt.title(f'Best Class Accuracy (Epoch {best_epoch})')
plt.xticks(range(num_classes))
plt.ylim(0, 1)

# 添加数值标签
for i, v in enumerate(best_class_acc.numpy()):
    plt.text(i, v + 0.01, f'{v:.2f}', ha='center')

plt.savefig('best_class_accuracy.png')
plt.close()

print(f"\n (Epoch {best_epoch}, Accuracy: {best_accuracy * 100:.2f}%)")