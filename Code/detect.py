import torch
import torchvision
from PIL import Image
from torch import nn
from torch.nn import Conv2d
from torchvision import transforms

img_path = './images/dog.png'
img = Image.open(img_path)
img = img.convert('RGB')
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor()
])


img = transform(img)


class Tudui(nn.Module):

    def __init__(self):
        super(Tudui, self).__init__()

        self.model1 = nn.Sequential(
            Conv2d(3, 32, 5, padding=2),
            nn.MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            nn.MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.Linear(64, 10)
        )

model = torch.load('./run/tudui_9.pth', map_location=torch.device('cpu'))

img = torch.reshape(img, (1, 3, 32, 32))

model.eval()
with torch.no_grad():
    output = model(img)
print(output.argmax(1).item())

