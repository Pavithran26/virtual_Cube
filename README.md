# virtual_Cube 🧊

A webcam-driven virtual Rubik's Cube built with Streamlit, Three.js, and MediaPipe Hands.

## Features
- Interactive 3D 3×3 cube with six colored faces.
- Open palm motion rotates the whole cube view.
- Select U / D / L / R / F / B, then pinch and drag to turn a face.
- Interactive tutorial with next/back steps and gesture cues.
- Scramble and reset controls.
- Camera landmarks are processed in the browser; this app does not upload or record video.

## Run locally
Python 3.10–3.12 recommended.

    python -m venv .venv
    # Windows PowerShell: .venv\\Scripts\\Activate.ps1
    # macOS/Linux: source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

Open http://localhost:8501 and allow camera access.

## Deploy on Streamlit Community Cloud
1. Visit https://share.streamlit.io/
2. Create an app from this repository.
3. Set main file path to app.py and deploy.
4. Camera access requires HTTPS and visitor permission.

## Notes
- Gesture recognition is heuristic; lighting and hand angle affect detection.
- Face buttons are the reliable way to select a layer.
- Three.js and MediaPipe are loaded from CDNs, so internet access is needed.
- OpenCV is installed for future local calibration/image-processing utilities; the current landmark pipeline runs in the browser.

Stack: Python, Streamlit, OpenCV, MediaPipe Hands, Three.js.
