### **一、基本操作**

#### **1. 初始化与克隆**

```
# 初始化本地仓库（首次使用时）
git init

# 克隆远程仓库到本地
git clone <repository-url>  # e.g. git clone https://github.com/user/repo.git
```

#### **2. 添加与提交**

```
# 添加单个文件到暂存区
git add <filename>

# 添加所有修改文件到暂存区
git add .  # 或 git add --all

# 提交暂存区的内容到本地仓库
git commit -m "提交信息（需简洁明确）"
```

#### **3. 推送与拉取**

```
# 推送本地提交到远程仓库（第一次推送需指定分支）
git push origin <branch-name>  # e.g. git push origin main

# 拉取远程仓库最新代码（自动合并到当前分支）
git pull origin <branch-name>
```

#### **4. 分支管理**

```
# 查看所有分支
git branch -a

# 创建并切换到新分支
git checkout -b <new-branch-name>

# 切换分支
git checkout <branch-name>

# 合并分支（需先切换到目标分支）
git merge <source-branch-name>

# 删除分支（-d 为安全删除，-D 为强制删除）
git branch -d <branch-name>
```

------

### **二、复杂操作（回溯与修复）**

#### **1. 撤销工作区修改**

```
# 撤销单个文件的未暂存修改（危险：丢弃更改！）
git checkout -- <filename>   # Git < 2.23
git restore <filename>       # Git ≥ 2.23

# 撤销所有未暂存修改
git checkout -- .            # Git < 2.23
git restore .                # Git ≥ 2.23
```

#### **2. 撤销暂存区修改**

```
# 从暂存区移除单个文件（保留工作区修改）
git reset HEAD <filename
```