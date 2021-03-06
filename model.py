# -*- coding: utf-8 -*-

#Imports

import cv2
import numpy as np
import pafy

class video():

  def link(self, url):
    #get youtube video
    vpafy = pafy.new(url)
    play = vpafy.getbest(preftype = "mp4")
    
    #capturing video using open-cv
    self.cap = cv2.VideoCapture(play.url)
    self.cap.set(3, 480)
    self.cap.set(4, 640)

    self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
 
    self.age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)'] #age labels
    
    self.gender_list = ['MALE', 'FEMALE']             #gender labels

  def caffe_models(self):
    
    self.gender_net = cv2.dnn.readNet('./Deploy/deploy_gender.prototxt', 'gender_net.caffemodel')   #load pre-trained caffe weights for gender

    self.age_net = cv2.dnn.readNet('./Deploy/deploy_age.prototxt', 'age_net.caffemodel')        #load pre-trained caffe weights for age



    return(self.age_net, self.gender_net)

  def video_detector(self, age_net, gender_net):
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
      ret, image = self.cap.read()
      face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')  #detect faces using harcascade classifier 
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                                                   #converting  frames into grayscale
      faces = face_cascade.detectMultiScale(gray, 1.1, 5)

      if (len(faces) > 0):
        print("Found {} faces".format(str(len(faces))))
        
       #creating boxes over faces
      for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)

        face_img = image[y:y+h, x:x+w].copy()
        blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), self.MODEL_MEAN_VALUES, swapRB=False)

        #prediciting gender of the detected faces
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()    
        gender = self.gender_list[gender_preds[0].argmax()] 
        print("Gender : " + gender)
        
        #prediciting age of the detected faces
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = self.age_list[age_preds[0].argmax()]
        print("Age Range: " + age)

        #printing age and gneder in overlay
        overlay_text = "%s %s" % (gender, age)
        cv2.putText(image, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        cv2.imshow('frame', image)             #show images
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
          break

if __name__ == "__main__": 
  youtube_link = ''         #add your youtube link
  v = video()
  v.link(youtube_link)
  age_net, gender_net = v.caffe_models()
  v.video_detector(age_net, gender_net)
