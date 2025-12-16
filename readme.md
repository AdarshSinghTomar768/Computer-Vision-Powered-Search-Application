# 🧠 YOLOv11 Computer Vision Powered Search Application

A **Streamlit-based computer vision search engine** powered by **YOLOv11**, allowing users to process large image datasets, perform object detection, and **search images using intelligent filters** such as object class, count thresholds, and logical conditions (OR / AND).

---

## 🚀 Features

### 🔍 Intelligent Image Search
- Search images by detected object classes
- OR / AND logic for multi-class queries
- Optional object count thresholds per class

### 📸 Visual Result Exploration
- Bounding box visualization
- Highlight matched classes
- Responsive image grid layout
- Modern card-style UI

### ⚙️ Inference & Metadata Management
- Run YOLOv11 inference on image folders
- Save metadata as JSON
- Load previously processed metadata
- Avoids re-processing images unnecessarily

### 🧠 User-Friendly UI
- Built using Streamlit
- Interactive filters & controls
- Real-time result updates

---

## 🗂 Project Structure

```

YOLO_IMAGE_SEARCH/
│
├── app.py                      # Streamlit application
├── README.md                   # Project documentation
│
├── configs/
│   └── default.yaml            # Model & data configuration
│
├── src/
│   ├── inference.py            # YOLOv11 inference logic
│   ├── utils.py                # Metadata utilities
│   └── config.py               # Config loader
│
├── data/
│   └── processed/              # Generated metadata
│
└── requirements.txt            # Python dependencies

```

---

## 🛠 Tech Stack

- **Python 3.9+**
- **YOLOv11 (Ultralytics)**
- **Streamlit**
- **PyTorch**
- **Pillow (PIL)**
- **NumPy**

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```

git clone [https://github.com/AdarshSinghTomar768/Computer-Vision-Powered-Search-Application](https://github.com/AdarshSinghTomar768/Computer-Vision-Powered-Search-Application)
cd yolo-image-search

```

### 2️⃣ Create and activate virtual environment
```

python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

```

### 3️⃣ Install dependencies
```

pip install -r requirements.txt

```

---

## ▶️ Run the Application

```

streamlit run app.py

```

Open in browser:
```

[http://localhost:8501](http://localhost:8501)

````

---

## 📂 How to Use

### 🔹 Process New Images
1. Enter image directory path
2. Provide YOLOv11 model weights (`yolo11m.pt`)
3. Click **Start Inference**
4. Metadata is saved automatically

### 🔹 Load Existing Metadata
1. Provide path to `metadata.json`
2. Instantly load results without re-running inference

---

## 🔍 Search Options

| Feature | Description |
|------|------------|
| OR Search | Match any selected object |
| AND Search | Match all selected objects |
| Count Threshold | Limit object count per class |
| Bounding Boxes | Toggle detection boxes |
| Highlight Matches | Emphasize matched classes |
| Grid Layout | Adjustable image grid |

---

## 📁 Metadata Format (Example)

```json
{
  "image_path": "path/to/image.jpg",
  "detections": [
    {
      "class": "person",
      "confidence": 0.92,
      "bbox": [34, 45, 230, 400]
    }
  ],
  "class_counts": {
    "person": 2,
    "car": 1
  }
}
````

---

## ⚡ Performance Notes

* Supports **CPU**, **Apple Silicon (MPS)**, and **CUDA**
* Metadata caching improves performance
* Suitable for large image datasets

---

## 🚧 Future Improvements

* 🔍 Click-to-zoom image preview
* 📤 Export filtered results
* 🧠 Semantic search using embeddings
* 📊 Analytics dashboard

---

## 👨‍💻 Author

**Adarsh**
Machine Learning & Computer Vision Enthusiast
