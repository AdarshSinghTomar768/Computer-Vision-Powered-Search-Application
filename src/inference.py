from ultralytics import YOLO
from pathlib import Path
from src.config import load_config

class YOLOv11Inference:
    def __init__(self, model_name, device="cpu"):
        self.model = YOLO(model_name)
        self.device = device
        self.model.to(self.device)

        # Load config
        config = load_config()
        self.conf_thereshold = config["model"]["conf_thereshold"]
        self.extensions = config["data"]["image_extension"]   

    def process_image(self, image_path):
        results = self.model.predict(
            source=image_path,
            conf=self.conf_thereshold,
            device=self.device
        )

        detection = []
        class_counts = {}

        for result in results:
            for box in result.boxes:
                cls = result.names[int(box.cls)]
                conf = float(box.conf)
                bbox = box.xyxy[0].tolist()

                detection.append({
                    'class': cls,
                    'confidence': conf,
                    'bbox': bbox,
                    'count': 1
                })

                class_counts[cls] = class_counts.get(cls, 0) + 1

        for det in detection:
            det['count'] = class_counts[det['class']]

        return {
            'image_path': str(image_path),
            'detections': detection,
            'total_objects': len(detection),
            'unique_classes': list(class_counts.keys()),
            'class_counts': class_counts
        }

    def process_directory(self, directory):
        metadata = []
        patterns = []
        for ext in self.extensions:
            patterns.append(f"*{ext.lower()}")
            patterns.append(f"*{ext.upper()}")
   

        image_paths = []
        for pattern in patterns:
            image_paths.extend(Path(directory).rglob(pattern))

        for img_path in image_paths:
            try:
                metadata.append(self.process_image(img_path))
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
                continue

        return metadata  
