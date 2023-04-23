import cv2
import numpy as np
import pytesseract
from tflite_runtime.interpreter import Interpreter

# Load and allocate TFLite model
interpreter = Interpreter(model_path="mnist_model.tflite")
interpreter.allocate_tensors()

# Get input/output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Capture image using OpenCV
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

# Preprocess the image
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
resized = cv2.resize(gray, (28, 28))
normalized = resized/255.0
input_data = np.expand_dims(normalized, axis=(0, -1)).astype(np.float32)

# Set input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

predicted_class = np.argmax(output_data)

print("Predicted:", predicted_class)

text = pytesseract.image_to_string(frame)

# Search for the words "cash" or "credit" and extract the amounts next to them
cash_index = text.find("cash")
credit_index = text.find('credit')

if cash_index != -1:
    cash_amount = text[cash_index:].split()[1]
    print("Cash amount:", cash_amount)

if credit_index != -1:
    credit_amount = text[credit_index:].split()[1]
    print("Credit amount:", credit_amount)
