import torch
from torch import nn, optim
from torch.autograd.variable import Variable
#from torchvision import transforms, datasets

class Generator(torch.nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        in_image = torch.empty(size=(8,8,13))
        
        self.encoder0 = nn.Sequential(
            nn.Conv2d(13, 64, (4,4), stride=(2,2), padding=0),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(negative_slope=0.2)
        )
        
        self.encoder1 = nn.Sequential(
            nn.Conv2d(64, 128, (4,4), stride=(2,2), padding=0),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(negative_slope=0.2)
        )
        
        self.hidden0 = nn.Sequential(
            nn.Conv2d(128, 512, (4,4), stride=(2,2), padding=(0)),
            nn.ReLU()
        )
        
        self.decoder0 = nn.Sequential(
            nn.ConvTranspose2d(512, 128, (4,4), stride=(2,2)),
            nn.BatchNorm2d(128),
            nn.DropOut()
            # CONCATENATE OUTPUT WITH OUTPUT OF ENC1
        )
        
        self.decoder1 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, (4,4), stride=(2,2)),
            nn.BatchNorm2d(64),
            nn.DropOut()
            # CONCATENATE OUTPUT WITH OUTPUT OF ENC0
        )
        
        self.hidden1 = nn.Sequential(
            nn.ConvTranspose2d(64, 13, (4,4), stride=(2,2)),
            nn.Softmax()
        )
        
    def forward(self, x):
        x1 = self.encoder0(x)
        x2 = self.encoder1(x1)
        x = self.hidden0(x2)
        x = self.decoder0(x)
        # concatenate output of decoder0 with output of encoder1
        x = torch.cat((x,x2))
        x = self.decoder1(x)
        # concatenate output of decoder1 with output of encoder0
        x = torch.cat((x,x1))
        x = self.hidden1(x)
        return x
    


class Discriminator(torch.nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        in_src_image = torch.empty(size=(8,8,13))
        in_target_image = torch.empty(size=(8,8,13))
        merged = torch.cat((in_src_image, in_target_image))
        
        self.hidden0 = nn.Sequential( 
            #how to do conv2d()(merged)?
            nn.Conv2d(13, 64, (4,4), stride=(2,2), padding=0),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self.hidden1 = nn.Sequential(
            nn.Conv2d(64, 128, (4,4), stride=(2,2), padding=0),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self.hidden2 = nn.Sequential(
            nn.Conv2d(128, 256, (4,4), stride=(2,2), padding=0),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self.hidden3 = nn.Sequential(
            nn.Conv2d(256, 512, (4,4), stride=(2,2), padding=0),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self.hidden4 = nn.Sequential(
            nn.Conv2d(512, 512, (4,4), padding=0),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self.out = nn.Sequential(
            nn.Conv2d(512, 1, (4,4), padding=0),
            nn.Sigmoid()
        )

    def forward(self, x):
        # assuming x is the already merged boards before and after the move
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.hidden3(x)
        x = self.hidden4(x)
        x = self.out(x)
        return x



