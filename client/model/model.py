import torchvision.models as models 
import torch.nn as nn
import torch
from facenet_pytorch import MTCNN

class Resnext(nn.Module):
    def __init__(self):
        super(Resnext, self).__init__()
        self.conv1 = nn.Conv2d(1, 3, kernel_size=7, stride=2, padding=3,
                               bias=False)
        self.resnet = models.resnext50_32x4d(pretrained=True)
        self.fc = nn.Linear(self.resnet.fc.out_features, 2)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.resnet(x)  
        x = self.fc(x) 
        x = self.softmax(x)
        return x
 
 
# class MTCNN(nn.Module):
#     def __init__(self):
#         super(MTCNN, self).__init__()
#         self.mtcnn = MTCNN(select_largest=True)
    
#     def forward(self, x):
#         return self.mtcnn(x)
