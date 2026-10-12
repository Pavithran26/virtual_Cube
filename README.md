# virtual_Cube 🧊

A webcam-driven virtual Rubik's Cube built with Streamlit, Three.js, and MediaPipe Hands. Google sign-in uses Firebase Authentication; the Streamlit server verifies the Firebase ID token with Firebase Admin before showing the cube.

## Features

- Google sign-in through the Firebase Hosting component.
- Server-side Firebase ID-token verification.
- Interactive 3D 3×3 cube with six colored faces.
- Open palm motion rotates the whole cube view.
- Select U / D / L / R / F / B, then pinch and drag to turn a face.
- Interactive tutorial, scramble, and reset controls.
- Camera landmarks are processed in the browser; this app does not upload or record video.

## Required configuration

The deployed Streamlit app needs **two secret sections**. Adding only the Firebase web config is not enough.

### 1. Create a Firebase Admin service-account key

1. Open [Firebase Console](https://console.firebase.google.com/) and select project **virtualcube-571b7**.
2. Open **Project settings → Service accounts**.
3. Click **Generate new private key** and download the JSON file.
4. Keep the downloaded file private. Do not commit it to GitHub and do not send it in chat.

### 2. Configure Streamlit Community Cloud

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and select the **virtualcube** app.
2. Open **Manage app → Settings → Secrets**.
3. Add the following TOML. Replace the example URL only if your Firebase Hosting site URL is different. For the service account, copy the **entire contents** of the downloaded JSON file into the multiline string, replacing the placeholder. Keep the JSON's double quotes and its `\\n` sequences intact.

```toml
[auth_component]
url = "https://virtualcube-571b7.web.app"

[firebase_admin]
service_account_json = '''
PASTE THE ENTIRE SERVICE-ACCOUNT JSON FILE CONTENTS HERE
'''
```

The placeholder is not valid service-account data; replace it with the actual JSON content before saving. Do not paste the private key into GitHub or this conversation. Save the Secrets settings, then reboot the Streamlit app.

The app also supports putting each service-account JSON property directly under `[firebase_admin]`, but the single `service_account_json` field above is easier and less error-prone.

### 3. Check Firebase Authentication domains

In Firebase Console, open **Authentication → Settings → Authorized domains** and ensure both hostnames are present:

- `virtualcube.streamlit.app`
- `virtualcube-571b7.web.app`

Under **Authentication → Sign-in method**, enable **Google** and choose a support email if prompted.

### 4. Deploy the Firebase Hosting component

The repo includes `firebase.json` and `firebase-auth-component/index.html`. From the repository root, deploy the component with the Firebase CLI:

```bash
npm install -g firebase-tools
firebase login
firebase use virtualcube-571b7
firebase deploy --only hosting
```

Confirm the Hosting URL configured in Streamlit Secrets matches the deployed site. Opening the Hosting URL directly should show the sign-in page, but it does not by itself prove the full Streamlit sign-in flow is working.

## Run locally

Python 3.10–3.12 recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` with the same `[auth_component]` and `[firebase_admin]` entries shown above, then run:

```bash
streamlit run app.py
```

Open http://localhost:8501 and allow camera access. Never commit `.streamlit/secrets.toml` or the service-account JSON.

## Troubleshooting

- **“Firebase authentication is missing Streamlit secret”**: add the named section in **Manage app → Settings → Secrets**.
- **Service-account / certificate errors**: verify that the JSON is from project `virtualcube-571b7` and that its entire contents were pasted into the multiline string.
- **Google sign-in reports unauthorized domain**: add the exact hostname under Firebase Authentication's authorized domains.
- **Sign-in succeeds but the cube stays locked**: reboot the Streamlit app, verify the Hosting component URL and service-account credentials, then retry.

Firebase web-app config is client-side configuration; the Firebase Admin service-account private key is sensitive and must remain server-side.

Stack: Python, Streamlit, OpenCV, Firebase Authentication, Firebase Admin, Google Sign-In, MediaPipe Hands, Three.js.
