import cv2
import numpy as np
import tflite_support as tflite

##load and allocate TFlite model
interpreter = tf.lite.Interpreter(model_path="mnist_model.tflite")
interpreter.allocate_tensors()

#Get input/output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#Capture image using OpenCV
cap = cv2.VideoCapture(0)
#frame = cv2.imread("path/to/your/image.jpg")
ret, frame = cap.read()
cap.release()

#Preprocess the image
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
resized = cv2.resize(gray, (28,28))
normalized = resized/255.0
input_data = np.expand_dims(normalized, axis=(0,-1)).astype(np.float32)

#set input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

#Run inference
interpreter.invoke()

# Get output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

predicted_class = np.argmax(output_data)

print("Predicted class:", predicted_class)