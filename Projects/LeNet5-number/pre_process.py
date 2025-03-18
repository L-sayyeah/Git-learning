from sklearn.model_selection import train_test_split
from torch.utils.data import ConcatDataset, Subset
from PMU_Dataset import PMU_Dataset


# 加载数据集，合并为一类并切割为测试集和训练集
def load_images():
    # 导入数据集
    root_dir = './PMU-UD'
    # 用于存储每个类别的训练集和测试集
    train_datasets = []
    test_datasets = []

    # 遍历每个类别
    for idx in range(0, 10):
        dataset = PMU_Dataset(root_dir, str(idx))
        # 生成索引列表
        indices = list(range(len(dataset)))
        # 使用 train_test_split 进行划分， 20% 作为测试集
        train, test = train_test_split(indices, test_size=0.2, random_state=42)

        # 创建训练集和测试集的子集
        train_subset = Subset(dataset, train)
        test_subset = Subset(dataset, test)

        # 将子集添加到对应的列表中
        train_datasets.append(train_subset)
        test_datasets.append(test_subset)

    # 合并所有类别的训练集和测试集
    train_dataset = ConcatDataset(train_datasets)
    test_dataset = ConcatDataset(test_datasets)

    # 打印测试集和训练集样本数量
    print(f"训练集样本数量: {len(train_dataset)}")
    print(f"测试集样本数量: {len(test_dataset)}")

    return train_dataset, test_dataset

