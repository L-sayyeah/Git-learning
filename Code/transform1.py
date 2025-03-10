# 即更好使用transforms的各个类

from torchvision import transforms
from PIL import Image
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")
img = Image.open("./images/J9xjxe1jIg_small.jpg")

# ToTensor
tensor_trans = transforms.ToTensor()
img_tensor = tensor_trans(img)

writer.add_image("ToTensor", img_tensor)

# Normalize归一化
print(img_tensor)
trans_norm = transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
img_norm = trans_norm(img_tensor)
print((img_norm))
writer.add_image("Normalize", img_norm)

# Resize
print(img.size)
trans_resize = transforms.Resize((512, 512))
img_resize = trans_resize(img)
print(img_resize.size)
img_resize = tensor_trans(img_resize)
writer.add_image("Resize", img_resize)

# Compose - resize - 2 有点组合操作的意思，有点意思的
trans_compose = transforms.Compose([trans_resize, tensor_trans, trans_norm])
img_compose = trans_compose(img)
writer.add_image("Compose", img_compose)

# RandomCrop,随机裁剪
trans_randomCrop = transforms.RandomCrop(512)
trans_compose = transforms.Compose([trans_randomCrop, tensor_trans])
for i in range(10):
    img_randomCrop = trans_compose(img)
    writer.add_image("RandomCrop", img_randomCrop, i)

writer.close()



''' 

transforms使用注意：

1.关注输入输出类型

2.关注官方文档

3.关注方法需要的参数

4.不知道返回值的时候可以print，print(type())

5.熟练使用TensorBoard

'''
