from ultralytics import YOLO

# Load and export the model to NCNN format

from ultralytics import YOLO

# Load a YOLO11n PyTorch model
model = YOLO("yolo11n-cls.pt")

# Export the model to NCNN format
model.export(format="ncnn")  # creates 'yolo11n_ncnn_model'

# Load the exported NCNN model
ncnn_model = YOLO("yolo11n-cls_ncnn_model")

# Run inference
results = ncnn_model("https://ultralytics.com/images/bus.jpg")


# Note: Loading the NCNN model in Python directly is not supported via ultralytics,
# so further inference would typically require a platform compatible with NCNN.
