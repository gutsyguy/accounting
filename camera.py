import cv2
import numpy as np
import pytesseract
import tensorflow as tf

interpreter = tf.lite.Interpreter(model_path="mnist_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Unable to open camera")
else:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera")
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        resized = cv2.resize(gray, (28, 28))
        normalized = resized / 255.0
        input_data = np.expand_dims(normalized, axis=0).astype(np.float32)

        interpreter.set_tensor(input_details[0]['index'], input_data)


        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])

        predicted_class = np.argmax(output_data)

        print("Predicted:", predicted_class)

        text = pytesseract.image_to_string(frame)

        cash_index = text.find("cash")
        credit_index = text.find('credit')

        if cash_index != -1:
            cash_amount = text[cash_index:].split()[1]
            print("Cash amount:", cash_amount)
        else:
            print("Unable to detect cash amount")

        if credit_index != -1:
            credit_amount = text[credit_index:].split()[1]
            print("Credit amount:", credit_amount)
        else:
            print("Unable to detect credit amount")

cap.release()
