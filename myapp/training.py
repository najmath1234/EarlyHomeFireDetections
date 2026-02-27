from ultralytics import YOLO

# Load pretrained model
model = YOLO("yolov8n.pt")  # nano version (fast)

# Train model
model.train(
    data=r"C:\Users\najum\Downloads\Fire and Smoke Dataset\Fire and Smoke Dataset\data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,

)