import streamlit as st
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64
import io

from src.inference import YOLOv11Inference
from src.utils import save_metadata, load_metadata, get_unique_classes_counts

# -------------------------------------------------
# Add project root to PYTHONPATH
# -------------------------------------------------
sys.path.append(str(Path(__file__).parent))


# -------------------------------------------------
# Utils
# -------------------------------------------------
def img_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
def init_session_state():
    defaults = {
        "metadata": None,
        "unique_classes": [],
        "count_options": {},
        "search_results": [],
        "search_params": {
            "search_mode": "Any of the selected classes (OR)",
            "selected_classes": [],
            "threshold": {}
        },
        "show_boxes": True,
        "grid_columns": 3,
        "highlight_matches": True
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="YOLOv11 Search App",
    layout="wide"
)

st.title("🧠 Computer Vision Powered Search Application")


# -------------------------------------------------
# Card CSS
# -------------------------------------------------
st.markdown(
    """
    <style>
    .image-card {
        position: relative;
        background: #111;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(0,0,0,0.6);
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }

    .image-card:hover {
        transform: scale(1.02);
    }

    .image-container img {
        width: 100%;
        height: auto;
        display: block;
    }

    .meta-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 10px;
        font-size: 13px;
        color: #fff;
        background: linear-gradient(
            rgba(0,0,0,0),
            rgba(0,0,0,0.85)
        );
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Main Mode Selection
# -------------------------------------------------
option = st.radio(
    "Choose an option:",
    ("Process new images", "Load existing metadata"),
    horizontal=True
)


# -------------------------------------------------
# Process New Images
# -------------------------------------------------
if option == "Process new images":
    with st.expander("📂 Process new images", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            image_dir = st.text_input(
                "Image directory path:",
                placeholder="/Users/adarsh/Downloads/archive/raw-img"
            )

        with col2:
            model_path = st.text_input(
                "Model weights path:",
                "yolo11m.pt"
            )

        if st.button("🚀 Start Inference"):
            if not image_dir:
                st.warning("Please enter an image directory path.")
            else:
                try:
                    with st.spinner("Running object detection..."):
                        inferencer = YOLOv11Inference(model_path)
                        metadata = inferencer.process_directory(image_dir)

                        metadata_path = save_metadata(metadata, image_dir)

                        st.session_state.metadata = metadata
                        (
                            st.session_state.unique_classes,
                            st.session_state.count_options
                        ) = get_unique_classes_counts(metadata)

                    st.success(f"Processed {len(metadata)} images. Metadata saved to:")
                    st.code(str(metadata_path))

                except Exception as e:
                    st.error(f"Error during inference: {str(e)}")


# -------------------------------------------------
# Load Existing Metadata
# -------------------------------------------------
else:
    with st.expander("📄 Load Existing Metadata", expanded=True):
        metadata_path = st.text_input(
            "Metadata file path:",
            placeholder="/Users/adarsh/Downloads/processed/raw-img/metadata.json"
        )

        if st.button("📥 Load Metadata"):
            if not metadata_path:
                st.warning("Please enter metadata file path.")
            else:
                try:
                    with st.spinner("Loading metadata..."):
                        metadata = load_metadata(metadata_path)

                        st.session_state.metadata = metadata
                        (
                            st.session_state.unique_classes,
                            st.session_state.count_options
                        ) = get_unique_classes_counts(metadata)

                    st.success(
                        f"Successfully loaded metadata for {len(metadata)} images."
                    )

                except Exception as e:
                    st.error(f"Error loading metadata: {str(e)}")


# -------------------------------------------------
# Search Functionality
# -------------------------------------------------
if st.session_state.metadata is not None:
    if len(st.session_state.metadata) == 0:
        st.warning("⚠️ Metadata is empty. Please check your image directory.")
    else:
        st.header("🔍 Search Engine")

        st.session_state.search_params["search_mode"] = st.radio(
            "Search mode:",
            ("Any of the selected classes (OR)", "All selected classes (AND)"),
            horizontal=True
        )

        st.session_state.search_params["selected_classes"] = st.multiselect(
            "Classes to search for:",
            options=st.session_state.unique_classes
        )

        if st.session_state.search_params["selected_classes"]:
            st.subheader("Count Threshold (Optional)")
            cols = st.columns(len(st.session_state.search_params["selected_classes"]))
            for i, cls in enumerate(st.session_state.search_params["selected_classes"]):
                with cols[i]:
                    st.session_state.search_params["threshold"][cls] = st.selectbox(
                        f"Max count for {cls}",
                        options=["None"] + st.session_state.count_options[cls]
                    )

        if st.button("Search Images", type="primary") and st.session_state.search_params["selected_classes"]:
            results = []
            params = st.session_state.search_params

            for item in st.session_state.metadata:
                class_matches = {}

                for cls in params["selected_classes"]:
                    detections = [d for d in item["detections"] if d["class"] == cls]
                    count = len(detections)

                    threshold = params["threshold"].get(cls, "None")

                    if threshold == "None":
                        class_matches[cls] = count >= 1
                    else:
                        class_matches[cls] = 1 <= count <= int(threshold)

                if params["search_mode"] == "Any of the selected classes (OR)":
                    matches = any(class_matches.values())
                else:
                    matches = all(class_matches.values())

                if matches:
                    results.append(item)

            st.session_state.search_results = results


# -------------------------------------------------
# Display Results
# -------------------------------------------------
if st.session_state.search_results:
    results = st.session_state.search_results
    params = st.session_state.search_params

    st.subheader(f"📷 Results: {len(results)} matching images")

    with st.expander("Display Options", expanded=True):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.session_state.show_boxes = st.checkbox(
                "Show Bounding Boxes", value=st.session_state.show_boxes
            )

        with c2:
            st.session_state.grid_columns = st.slider(
                "Grid columns", 2, 6, st.session_state.grid_columns
            )

        with c3:
            st.session_state.highlight_matches = st.checkbox(
                "Highlight matching classes", value=st.session_state.highlight_matches
            )

    grid_cols = st.columns(st.session_state.grid_columns)
    col_index = 0

    for result in results:
        with grid_cols[col_index]:
            try:
                img = Image.open(result["image_path"]).convert("RGB")
                draw = ImageDraw.Draw(img)

                if st.session_state.show_boxes:
                    try:
                        font = ImageFont.truetype("Arial.ttf", 12)
                    except:
                        font = ImageFont.load_default()

                    for det in result["detections"]:
                        cls = det["class"]
                        bbox = det["bbox"]

                        if cls in params["selected_classes"]:
                            color, thickness = "#30C938", 3
                        elif not st.session_state.highlight_matches:
                            color, thickness = "#666666", 1
                        else:
                            continue

                        draw.rectangle(bbox, outline=color, width=thickness)

                        label = f"{cls} {det['confidence']:.2f}"
                        text_bbox = draw.textbbox((0, 0), label, font=font)
                        w, h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

                        draw.rectangle(
                            [bbox[0], bbox[1], bbox[0] + w + 8, bbox[1] + h + 4],
                            fill=color
                        )
                        draw.text(
                            (bbox[0] + 4, bbox[1] + 2),
                            label,
                            fill="white",
                            font=font
                        )

                meta_items = [
                    f"{k}: {v}"
                    for k, v in result["class_counts"].items()
                    if k in params["selected_classes"]
                ]

                st.markdown(
                    f"""
                    <div class="image-card">
                        <div class="image-container">
                            <img src="data:image/png;base64,{img_to_base64(img)}" />
                        </div>
                        <div class="meta-overlay">
                            <strong>{Path(result["image_path"]).name}</strong><br>
                            {" , ".join(meta_items) if meta_items else "No matches"}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Error displaying {result['image_path']}: {str(e)}")

        col_index = (col_index + 1) % st.session_state.grid_columns
