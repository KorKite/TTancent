<<<<<<< Updated upstream:client/model/face_detect.py
from collections import OrderedDict
import numpy as np
import cv2
import argparse
import dlib
import imutils
import matplotlib.pyplot as plt
from PIL import Image
import dlib

def get_frontal_face(image):
    face_detector = dlib.get_frontal_face_detector()
    try:
        faces = face_detector(image)
    except:
        return []
    if len(faces)>1:
        size_list = []
        for face in faces:
            size = (face.bottom()-face.top())*(face.right()-face.left())
            size_list.append(size)
        face = faces[np.argmax(size_list)]
    elif len(faces)==1:
        face = faces[0]
    else:
        return []

    front_face = image[face.top():face.bottom(),face.left():face.right()]
    if 0 in front_face.shape:
        return []
    front_face = cv2.resize(front_face, dsize=(200,200))
    front_face = cv2.cvtColor(front_face.astype('uint8'), cv2.COLOR_BGR2RGB)
    return front_face



def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    # create two copies of the input image -- one for the
    # overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()

    # if the colors list is None, initialize it with a unique
    # color for each facial landmark region
    if colors is None:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32),
                  (163, 38, 32), (180, 42, 220)]

    # loop over the facial landmark regions individually
    for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
        # grab the (x, y)-coordinates associated with the
        # face landmark
        (j, k) = FACIAL_LANDMARKS_INDEXES[name]
        pts = shape[j:k]
        facial_features_cordinates[name] = pts

        # check if are supposed to draw the jawline
        if name == "Jaw":
            # since the jawline is a non-enclosed facial region,
            # just draw lines between the (x, y)-coordinates
            for l in range(1, len(pts)):
                ptA = tuple(pts[l - 1])
                ptB = tuple(pts[l])
                cv2.line(overlay, ptA, ptB, colors[i], 2)

        # otherwise, compute the convex hull of the facial
        # landmark coordinates points and display it
        else:
            hull = cv2.convexHull(pts)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)

    # apply the transparent overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # return the output image
    return output,facial_features_cordinates



def shape_to_numpy_array(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coordinates = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coordinates


def get_eyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = shape_to_numpy_array(shape)

        output,facial_features_cordinates = visualize_facial_landmarks(img, shape)

    re = facial_features_cordinates['Right_Eye']
    le = facial_features_cordinates['Left_Eye']

    x1 = np.min(re[:,0])
    x2 = np.max(re[:,0])
    y1 = np.min(re[:,1])
    y2 = np.max(re[:,1])

    re_r = img[y1:y2, x1:x2]

    x1 = np.min(le[:,0])
    x2 = np.max(le[:,0])
    y1 = np.min(le[:,1])
    y2 = np.max(le[:,1])

    le_r = img[y1:y2, x1:x2]

    return le_r, re_r


FACIAL_LANDMARKS_INDEXES = OrderedDict([
    ("Right_Eye", (36, 42)),
    ("Left_Eye", (42, 48))
])
facial_features_cordinates = {} 
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./model/models/shape_predictor_68_face_landmarks.dat')



def crop_eyes(eyes, img):
  add = 15
  x1 = np.min(eyes[:,0]) - add
  x2 = np.max(eyes[:,0]) + add
  y1 = np.min(eyes[:,1]) - add
  y2 = np.max(eyes[:,1]) + add

  width = x2-x1
  height = y2-y1

  if width > height:
    diff = width - height
    y2 += int(diff/2)
    y1 -= int(diff/2)
  else:
    diff = height - width
    x2 += int(diff/2)
    x1 -= int(diff/2) 

  roi = img[y1:y2, x1:x2]
  return roi


def image_to_eyes(path):
  img = cv2.imread(path, cv2.COLOR_BGR2GRAY) 
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  rects = detector(gray, 1)
  find = 0

  for (i, rect) in enumerate(rects):
      shape = predictor(gray, rect)
      shape = shape_to_numpy_array(shape)

      output,facial_features_cordinates = visualize_facial_landmarks(img, shape)
      find = 1

  if find ==1:
    re = facial_features_cordinates['Right_Eye']
    le = facial_features_cordinates['Left_Eye']

    re_crop = crop_eyes(re, img)
    le_crop = crop_eyes(le, img)
    return re_crop, le_crop
  else:
    return -1
=======
from collections import OrderedDict
import numpy as np
import cv2
import argparse
import dlib
import imutils
import matplotlib.pyplot as plt
from PIL import Image
import dlib

def get_frontal_face(image):
    face_detector = dlib.get_frontal_face_detector()
    try:
        faces = face_detector(image)
    except:
        return []
    if len(faces)>1:
        size_list = []
        for face in faces:
            size = (face.bottom()-face.top())*(face.right()-face.left())
            size_list.append(size)
        face = faces[np.argmax(size_list)]
    elif len(faces)==1:
        face = faces[0]
    else:
        return []

    front_face = image[face.top():face.bottom(),face.left():face.right()]
    if 0 in front_face.shape:
        return []
    front_face = cv2.resize(front_face, dsize=(200,200))
    front_face = cv2.cvtColor(front_face.astype('uint8'), cv2.COLOR_BGR2RGB)
    return front_face



def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    # create two copies of the input image -- one for the
    # overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()

    # if the colors list is None, initialize it with a unique
    # color for each facial landmark region
    if colors is None:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32),
                  (163, 38, 32), (180, 42, 220)]

    # loop over the facial landmark regions individually
    for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
        # grab the (x, y)-coordinates associated with the
        # face landmark
        (j, k) = FACIAL_LANDMARKS_INDEXES[name]
        pts = shape[j:k]
        facial_features_cordinates[name] = pts

        # check if are supposed to draw the jawline
        if name == "Jaw":
            # since the jawline is a non-enclosed facial region,
            # just draw lines between the (x, y)-coordinates
            for l in range(1, len(pts)):
                ptA = tuple(pts[l - 1])
                ptB = tuple(pts[l])
                cv2.line(overlay, ptA, ptB, colors[i], 2)

        # otherwise, compute the convex hull of the facial
        # landmark coordinates points and display it
        else:
            hull = cv2.convexHull(pts)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)

    # apply the transparent overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # return the output image
    return output,facial_features_cordinates



def shape_to_numpy_array(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coordinates = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coordinates


def get_eyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = shape_to_numpy_array(shape)

        output,facial_features_cordinates = visualize_facial_landmarks(img, shape)

    re = facial_features_cordinates['Right_Eye']
    le = facial_features_cordinates['Left_Eye']

    x1 = np.min(re[:,0])
    x2 = np.max(re[:,0])
    y1 = np.min(re[:,1])
    y2 = np.max(re[:,1])

    re_r = img[y1:y2, x1:x2]

    x1 = np.min(le[:,0])
    x2 = np.max(le[:,0])
    y1 = np.min(le[:,1])
    y2 = np.max(le[:,1])

    le_r = img[y1:y2, x1:x2]

    return le_r, re_r


FACIAL_LANDMARKS_INDEXES = OrderedDict([
    ("Right_Eye", (36, 42)),
    ("Left_Eye", (42, 48))
])
facial_features_cordinates = {} 
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./client/model/models/shape_predictor_68_face_landmarks.dat')



def crop_eyes(eyes, img):
  add = 15
  x1 = np.min(eyes[:,0]) - add
  x2 = np.max(eyes[:,0]) + add
  y1 = np.min(eyes[:,1]) - add
  y2 = np.max(eyes[:,1]) + add

  width = x2-x1
  height = y2-y1

  if width > height:
    diff = width - height
    y2 += int(diff/2)
    y1 -= int(diff/2)
  else:
    diff = height - width
    x2 += int(diff/2)
    x1 -= int(diff/2) 

  roi = img[y1:y2, x1:x2]
  return roi, (x1, y1, x2, y2)


def image_to_eyes(img):
#   img = cv2.imread(path, cv2.COLOR_BGR2GRAY) 
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  rects = detector(gray, 1)
  find = 0

  for (i, rect) in enumerate(rects):
      shape = predictor(gray, rect)
      shape = shape_to_numpy_array(shape)

      output,facial_features_cordinates = visualize_facial_landmarks(img, shape)
      find = 1

  if find == 1:
    re = facial_features_cordinates['Right_Eye']
    le = facial_features_cordinates['Left_Eye']

    re_crop, (r_x1, r_y1, r_x2, r_y2) = crop_eyes(re, img)
    le_crop, (l_x1, l_y1, l_x2, l_y2) = crop_eyes(le, img)
    return re_crop, le_crop, [r_x1, r_y1, r_x2, r_y2], [l_x1, l_y1, l_x2, l_y2]
  else:
    return None
>>>>>>> Stashed changes:client/model/find_landmark.py
