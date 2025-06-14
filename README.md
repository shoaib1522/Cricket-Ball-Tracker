# 🏏 Cricket Ball Tracking System (CBT)

A powerful, low-cost computer vision system to automatically track cricket ball deliveries from standard video footage. This project leverages the YOLOv5 object detection model and Kalman Filters to provide insightful analytics for coaches and players **without** the need for expensive commercial hardware.

---

## ✨ Features

- 🎯 **Accurate Ball Detection**: Uses a pre-trained YOLOv5 model to reliably detect the cricket ball in each frame.  
- 🛤️ **Smooth Trajectory Tracking**: Implements a Kalman Filter to maintain a continuous track of the ball's path, even through brief occlusions.  
- 🌍 **Real-World Pitch Mapping**: Employs Homography transformation to convert video pixel coordinates into real-world meters on the pitch.  
- 📊 **Automated Analytics**: Automatically classifies each delivery based on its bounce point (e.g., _Full_, _Good Length_, _Short_).  
- 🎥 **Annotated Video Output**: Generates a new video file with the trajectory and analytics visually overlaid for easy review.  
- 💾 **Data Logging**: Saves key metrics for each delivery to a CSV file for long-term performance analysis.  
- 💻 **Accessible & Low-Cost**: Designed to run on a standard laptop with a webcam or pre-recorded video files.  

---

## 🔬 Understanding the Analytics

The system classifies each delivery's **length** based on where the ball first bounces on the pitch, relative to the batsman.

📍 **Bounce Point (Y)**: The most important metric — calculated in meters from the batsman's popping crease. This is detected at the lowest point in the ball’s trajectory.

### 📐 Classification Types:
- **Full**: Bounces very close to the batsman (typically within ~2.5 meters). Often driven or yorkers.
- **Good Length**: Ideal range (2.5m to 6m). Causes uncertainty in footwork.
- **Short**: Bounces farther than 6m away. Offers more time; suitable for pull/hook shots.

> ⚙️ *Thresholds can be configured in* `config.py` *as per pitch conditions or coaching preferences.*

---

## 🛠️ Technology Stack

- **Python 3.10+**
- 🧠 **YOLOv5** – for object detection
- 🧮 **NumPy** – numerical operations, Kalman Filter
- 📹 **OpenCV** – video & image processing
- 🐼 **Pandas** – structured data handling
- 🔥 **PyTorch** – deep learning inference

---

## 📂 Project Structure

```

CricketBallTracker/
│
├── 📄 main.py               # 🚀 Master script to run the system
├── 📄 config.py             # ⚙️ Configuration for paths and parameters
├── 📄 drawing\_utils.py      # 🎨 Draws overlays, lines, and labels on frames
├── 📄 ball\_detector.py      # 🔍 YOLOv5-based detection
├── 📄 ball\_tracker.py       # 🏃‍♂️ Kalman Filter tracking
├── 📄 pitch\_mapper.py       # 🗺️ Homography pixel-to-pitch conversion
├── 📄 analytics\_engine.py   # 📈 Classifies delivery length
├── 📄 requirements.txt      # 📦 Python dependencies
├── 📄 README.md             # 📖 You're here!
│
├── 📁 data/
│   └── 📁 videos/
│       └── 📹 cricket.mp4   # ➕ Add your input videos here
│
├── 📁 models/
│   └── 🧠 yolov5s.pt        # 🔍 Pre-trained model weights
│
├── 📁 output/               # 📤 Stores results: video + analytics.csv
│
└── 📁 venv/                 # 🐍 Python virtual environment

````

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- ✅ Python 3.10+ → [python.org](https://www.python.org/)
- ✅ Git → [git-scm.com](https://git-scm.com/)

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/CricketBallTracker.git
cd CricketBallTracker
````

### 3️⃣ Set Up Virtual Environment

```bash
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Download the YOLOv5 Model

📥 Download `yolov5s.pt` from:

👉 [https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt)
📁 Move it to the `models/` directory.

---

## 🏃‍♀️ How to Run the System

### 🖼️ Step 1: Add Your Video

Place your video (e.g., `my_delivery.mp4`) inside:

```bash
data/videos/
```

### 🛠️ Step 2: Update Configuration

In `config.py`, set the video path:

```python
INPUT_VIDEO_PATH = 'data/videos/my_delivery.mp4'
```

### 📏 Step 3: Calibrate the Pitch (⭐ Most Important Step!)

* Pause your video and take a screenshot of a frame where the **crease is visible**.
* Open screenshot in MS Paint or any image editor.
* Get pixel (x, y) coordinates for the four corners of the crease:

  * Top-Left
  * Top-Right
  * Bottom-Left
  * Bottom-Right
* Update in `main.py`:

```python
src_points_px = [(605, 452), (691, 450), (560, 580), (745, 575)]
```

### ▶️ Step 4: Run It!

```bash
python main.py
```

Your annotated video and `analytics.csv` will be saved in the `output/` folder!

---

## 🤝 Contributing

Contributions welcome! 🙌

1. 🍴 Fork this repo
2. 🌿 Create a feature branch: `git checkout -b feature/MyFeature`
3. 💾 Commit: `git commit -m 'Add amazing feature'`
4. 🚀 Push: `git push origin feature/MyFeature`
5. 📬 Open a Pull Request

---

## 📜 License

📝 This project is licensed under the MIT License.
See the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgements

* 🔬 *"Deep-Learning-Based Computer Vision Approach for the Segmentation of Ball Deliveries and Tracking in Cricket"* – Abbas et al. (2022)
* 💡 [Ultralytics](https://github.com/ultralytics/yolov5) for the YOLOv5 implementation

---

✅ Made with passion for cricket and code.

---
