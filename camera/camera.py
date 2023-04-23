from cv2 import VideoCapture,imshow,imwrite, waitKey,destroyWindow

cam = VideoCapture(0)

  

result, image = cam.read()

image_id = 0
  
if result:
  
    imshow("TrainingImage{}".format(image_id), image)
  
    #saves image in local repository
    imwrite("TrainingImage{}.jpg".format(image_id), image)
  

    waitKey(0)
    destroyWindow("TrainingImage{}".format(image_id))
    image_id += 1
  
# If captured image is corrupted, moving to else part
else:
    print("No image detected. Please! try again")