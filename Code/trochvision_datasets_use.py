# transforms 和 datasets的联合使用

import torchvision
from torch.utils.tensorboard import SummaryWriter


dataset_transform = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor()
])

train_set = torchvision.datasets.CIFAR10(root='./datasets/CIFAR10', train=True, transform=dataset_transform, download=True)
test_set = torchvision.datasets.CIFAR10(root='./datasets/CIFAR10', train=False, transform=dataset_transform, download=True)

# print(test_set[0])
#
#
# img, target = test_set[0]
# print(test_set.classes[target])
# print(img)
# img.show()

print(test_set[0])

writer = SummaryWriter('logs')

for i in range(10):
    img, target = test_set[i]
    writer.add_image("test_set", img, i)
writer.close()
