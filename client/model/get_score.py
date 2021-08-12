from numpy.lib.twodim_base import eye
from model.find_landmark import image_to_eyes
from model.model import Resnext 
from facenet_pytorch import MTCNN
import torch
from PIL import Image
import cv2
import numpy as np

# from database.write import writer


class TTancent():
    def __init__(self):
        self.avg_score = -1000
        self.crt_score = -1000
        self.score_list = []
        self.location_list = np.array([]) 

        self.eye_model = Resnext() 
        self.eye_model.to(torch.device('cpu'))
        self.eye_model.load_state_dict(torch.load('./model/models/model_eye_0808.pt', map_location=torch.device('cpu')))

        self.face_model = MTCNN(select_largest=True)
        self.face_model.to(torch.device('cpu')) 

        self.img_width = 100.
        self.img_height = 100.

        self.first = 0

    def get_eye_score(self, roi): 
        if roi.shape[2] == 3: # have rgb channel
            roi = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))
        from torchvision import transforms 
        transforms = transforms.Compose([ 
                    transforms.Resize((100, 100)), 
                    transforms.ToTensor()  
                ])  
        x = transforms(roi).unsqueeze(0) 
        self.eye_model.eval()
        
        with torch.no_grad():
            outputs = self.eye_model(x) 
            _, preds = torch.max(outputs, dim=1)  
        return outputs[0][1].item() #[[opened score, closed score]]


    def get_movement_degree(self, img, need_eye = False):
        # img = cv2.imread(path) 
        boxes, probs, landmarks = self.face_model.detect(img, landmarks=True)
        if boxes is not None:
            face_coord = boxes[0].astype(np.int32)
            
            if need_eye == True:
                landmark = landmarks[0].astype(np.int32)
                ymin, ymax = landmark[0][0]-15, landmark[0][0]+15
                xmin, xmax = landmark[0][1]-15, landmark[0][1]+15

                le_eye = img[ymin:ymax, xmin:xmax, :]
 
                ymin, ymax = landmark[1][0]-15, landmark[1][0]+15
                xmin, xmax = landmark[1][1]-15, landmark[1][1]+15

                re_eye = img[ymin:ymax, xmin:xmax, :]
                # print('cropped', len(landmark), eye_crop.shape)
                # print(landmark)
            else:
                re_eye, le_eye = None, None
            return face_coord, (re_eye, le_eye)
        else:
            return None, None


    def ttancent_score(self, img):
        '''
        input : image path, model
        output : current score, average score
        calculate the probability of concentration
        1) if eye in the input image is opened or closed
        2) if the location of face in the input image is moved
        '''

        # get eye score
        eye_result = image_to_eyes(img) 
        if eye_result is not None:
            re_crop, le_crop, re_coord, le_coord = eye_result  
            if re_crop is not None and len(re_crop) > 0 and re_coord[0] > 0 and le_coord[0] > 0:
                re_score = self.get_eye_score(re_crop)
            else:
                re_score = -1

            if le_crop is not None and len(le_crop) > 0 and le_coord[0] > 0 and le_coord[0] > 0:
                le_score = self.get_eye_score(le_crop)
            else:
                le_score = -1 
        else: 
            re_coord, le_coord = None, None
            le_score, re_score = -1, -1
        eye_score = (le_score + re_score) / 2
        need_eye = True if eye_score == -1 else False
        

        # get face movement degree 
        face_coord, eye_crop_2 = self.get_movement_degree(img, need_eye) # [xmin, ymin, xmax, ymax]
        if face_coord is not None:
            # calculate eye score
            if need_eye == True and eye_crop_2 is not None:
                re_crop, le_crop = eye_crop_2[0], eye_crop_2[1]
                print(re_crop.shape)
                if re_crop is not None and len(re_crop) > 0 and re_crop.shape[1] > 0:
                    re_score = self.get_eye_score(re_crop)
                else:
                    re_score = -1

                if le_crop is not None and len(le_crop) > 0 and le_crop.shape[1] > 0:
                    le_score = self.get_eye_score(le_crop)
                else:
                    le_score = -1 

            # calculate the difference of face coordinates
            if len(self.location_list) > 0: # except for the first time
                diff = np.abs(self.location_list - face_coord) 
                diff = diff.astype('float32')
            else:
                diff = np.array([0., 0., 0., 0.])
            
            diff[0] /= self.img_width        
            diff[2] /= self.img_width
            diff[1] /= self.img_height
            diff[3] /= self.img_height 
    
            mvm_degree = np.mean(diff)
            self.location_list = face_coord

            if eye_score != -1:
                self.crt_score = eye_score * (1 - mvm_degree)
            else:
                self.crt_score = -1
            
        else: 
            le_score, re_score = -1, -1
            mvm_degree = 0
            self.crt_score = eye_score * (1 - mvm_degree)


        
        
        print('[Eye Score] ', eye_score)
        print('[Movement Degree] ', mvm_degree)
        print('[Current] ', self.crt_score)
        print('[Average] ', self.avg_score)
        print()
        #writer.write_user_score(self.crt_score)
        self.score_list.append(self.crt_score) 
        self.avg_score = sum(self.score_list) / len(self.score_list)
        
 
        return self.crt_score, self.avg_score, (re_coord, le_coord), face_coord
        
        
