import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Load TFLite model
interpreter = tflite.Interpreter(model_path="src//model4.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Setup camera
cap = cv2.VideoCapture(0)

# Set higher resolution (optional, bigger window)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 1280 or 1920
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 720 or 1080

# Try to set higher frame rate
cap.set(cv2.CAP_PROP_FPS, 60)  # Request 60 FPS (if camera supports)

def preprocess(frame, input_shape):
    frame_resized = cv2.resize(frame, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(frame_resized, axis=0)
    input_data = input_data.astype(np.uint8)
    return input_data

# Load label map
def load_labels(path):
    labels = {}
    with open(path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            labels[i] = line.strip()
    return labels

def centreCross(frame, color=(0, 0, 255), size=20, thickness=2):
    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2
    # Horizontal line
    cv2.line(frame, (center_x - size, center_y), (center_x + size, center_y), color, thickness)
    # Vertical line
    cv2.line(frame, (center_x, center_y - size), (center_x, center_y + size), color, thickness)

labels = load_labels("src//label.txt")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    input_shape = input_details[0]['shape']
    input_data = preprocess(frame, input_shape)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    h, w, _ = frame.shape

    for i in range(len(scores)):
        if scores[i] > 0.5:
            ymin, xmin, ymax, xmax = boxes[i]
            (startX, startY, endX, endY) = (int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h))
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            class_id = int(classes[i])
            class_name = labels.get(class_id, 'N/A')
            label = f"{class_name}: {scores[i]:.2f}"
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    centreCross(frame)
    # Resize the displayed window (optional, make it even bigger)
    display_frame = cv2.resize(frame, (1280, 720))  # or any size you want
    cv2.imshow('TFLite Detection', display_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
