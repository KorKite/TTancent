from model.face_detect import image_to_eyes
import torch
from PIL import Image
import cv2

def get_score(roi, model):
  roi = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))
  from torchvision import transforms, datasets
  transforms = transforms.Compose([ 
            transforms.Resize((100, 100)), 
            transforms.ToTensor() # ToTensor : numpy 이미지에서 torch 이미지로 변경
        ])  
  x = transforms(roi).unsqueeze(0) 
  model = model.eval()
  
  with torch.no_grad():
      outputs = model(x) 
      _, preds = torch.max(outputs, dim=1)
#   decision = 'opened' if preds==1 else 'closed'
  return outputs[0][1].item() #[[opened score, closed score]]




def test(path, model):
  '''
  input : image path
  output : none
  print the probability of eye in the input image is opened or closed
  '''
  result = image_to_eyes(path)
  if result != -1:
      re_crop, le_crop = result[0], result[1]
      if re_crop is not None:
          re_score = get_score(re_crop, model)
      else:
          re_score = -1

      if le_crop is not None:
          le_score = get_score(le_crop, model)
      else:
          le_score = -1
      return le_score, re_score
  else:
      print('Nothing detected!')
      return -1, -1
  
#   print(f'Predicted :  {decision}')
#   print(f'Actual :   {actual}')
#   print('Opened : %.2f%%, Closed : %.2f%%'%(outputs[0][1].item()*100, outputs[0][0].item()*100))




