# dataloader\

import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

test_data = torchvision.datasets.CIFAR10('./datasets/CIFAR10', train=False, transform=torchvision.transforms.ToTensor())

test_loader = DataLoader(test_data, batch_size=64, shuffle=True, num_workers=0, drop_last=False)
# shuffle打乱图片选择
# num_workers 多进程加载
# drop_last 最后数据不满足batch_size时是否丢弃

# 测试数据集中第一张图片，及target
img, target = test_data[0]
print(img.shape)
print(target)
writer = SummaryWriter("logs")

#dataloader把数据按batchsize柔和在一起
for epoch in range(2):
    step = 0
    for data in test_loader:
        imgs, targets = data
        # print(imgs.shape)
        # print(target)
        writer.add_images("epoch:{}".format(epoch), imgs, step)
        step += 1
    epoch += 1
writer.close()


