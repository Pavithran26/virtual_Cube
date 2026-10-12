# virtual_Cube 🧊

A webcam-driven virtual Rubik's Cube built with Streamlit, Three.js, and MediaPipe Hands, gated by Firebase Authentication with Google sign-in.

## Features
- Firebase Authentication **Google sign-in required** before the cube UI is shown.
- Signed-in user's Google display name, email fallback, and profile photo are shown, with sign-out.
- Interactive 3D 3×3 cube with six colored faces.
- Open palm motion rotates the whole cube view.
- Select U / D / L / R / F / B, then pinch and drag to turn a face.
- Interactive tutorial with next/back steps and gesture cues.
- Scramble and reset controls.
- Camera landmarks are processed in the browser; this app does not upload or record video.

## Run locally
Python 3.10–3.12 recommended.

    python -m venv .venv
    # Windows PowerShell: .venv\Scripts\Activate.ps1
    # macOS/Linux: source .venv/bin/activate
    pip install -r requirements.txt

Create `.streamlit/secrets.toml` (this file is ignored by Git) with the Firebase **Web app config** values:

```toml
[firebase]
apiKey = "YOUR_FIREBASE_WEB_API_KEY"
authDomain = "YOUR_PROJECT_ID.firebaseapp.com"
projectId = "YOUR_PROJECT_ID"
appId = "YOUR_FIREBASE_WEB_APP_ID"
messagingSenderId = "YOUR_SENDER_ID"
storageBucket = "YOUR_PROJECT_ID.firebasestorage.app"
```

Only the four required fields `apiKey`, `authDomain`, `projectId`, and `appId` are required by the current app; the other standard web config fields are optional. Firebase Web API configuration is client-side configuration, not an admin credential. Never put a service-account private key or other server secrets in this section.

Then run:

    streamlit run app.py

Open http://localhost:8501 and allow camera access.

## Firebase Console setup
1. Open https://console.firebase.google.com/ and select/create the Firebase project.
2. In **Project settings → General → Your apps**, register a **Web app** and copy its Firebase config values into the local secrets file / Streamlit Cloud secrets.
3. Open **Authentication → Sign-in method** and enable **Google**. Choose the project support email if prompted.
4. Open **Authentication → Settings → Authorized domains** and add the exact hostnames used for the app. For local development, add `localhost` if it is not already present. For Streamlit Community Cloud, add the deployed hostname (for example, `YOUR-APP-NAME.streamlit.app`).
5. For Google OAuth consent screen / branding, complete any setup Google prompts for in the Google Cloud project connected to Firebase.

## Deploy on Streamlit Community Cloud
1. Visit https://share.streamlit.io/ and create an app from this repository.
2. Set main file path to `app.py`.
3. In the app's **Settings → Secrets**, paste the TOML config shown above using your real Firebase web app values.
4. Deploy/reboot the app and test Google sign-in on its HTTPS hostname.
5. Ensure that hostname is in Firebase Authentication's authorized domains.

## Security notes and current limitations
- The cube is a client-side experience, so this login gate protects access to the cube UI but is **not server-side authorization for protected data or APIs**. If future versions store user data or expose backend APIs, verify Firebase ID tokens on the server and apply authorization there.
- Firebase Web config values are designed to be included in browser apps. Do not commit service-account JSON, private keys, or local `.streamlit/secrets.toml`.
- Google popup sign-in can be affected by browser popup/privacy settings or embedded iframe restrictions. Test the deployed HTTPS app in the target browsers; if popup flow is blocked, change to a top-level redirect flow or move the sign-in page to a dedicated web frontend.
- Gesture recognition is heuristic; lighting and hand angle affect detection. Face buttons are the reliable way to select a layer.
- Three.js and MediaPipe are loaded from CDNs, so internet access is needed.

Stack: Python, Streamlit, OpenCV, Firebase Authentication, Google Sign-In, MediaPipe Hands, Three.js.
