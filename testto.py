from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n-cls.pt")  # load an official model
#model = YOLO("path/to/best.pt")  # load a custom model

results = model("test.jpg")  # predict on an image
