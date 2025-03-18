import torch
from torch.utils.data import Dataset
from PIL import Image
import os

from torchvision import transforms


class PMU_Dataset(Dataset):
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)

        # 定义图片处理的转换操作
        self.transform = transforms.Compose([
            transforms.CenterCrop(80),
            transforms.Resize((32, 32)),
            transforms.ToTensor()
        ])



    def __getitem__(self, idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.root_dir, self.label_dir, img_name)
        img = Image.open(img_item_path)
        img = self.transform(img)
        # 将标签字符串转换为整数
        label = int(self.label_dir)
        # 将整数标签转换为 torch.LongTensor 类型
        label = torch.tensor(label, dtype=torch.long)
        return img, label


    def __len__(self):
        return len(self.img_path)