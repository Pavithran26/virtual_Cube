# virtual_Cube 🧊

A webcam-driven virtual Rubik's Cube built with Streamlit, Three.js, MediaPipe Hands, and Firebase Google sign-in.

## Features

- Google sign-in through the Firebase Hosting component.
- Interactive 3D 3×3 cube with six colored faces.
- Open palm motion rotates the whole cube view.
- Select U / D / L / R / F / B, then pinch and drag to turn a face.
- Interactive tutorial, scramble, and reset controls.
- Camera landmarks are processed in the browser; this app does not upload or record video.

## Firebase setup

The current Streamlit app loads its sign-in component from:

`https://virtualcube-571b7.web.app`

The component's Firebase web config is client-side config in `firebase-auth-component/index.html`; you do **not** need to add a `[firebase]` or `[auth_component]` section in Streamlit Secrets.

In Firebase Console for project **virtualcube-571b7**:

1. Open **Authentication → Sign-in method** and enable **Google**. Choose a support email if prompted.
2. Open **Authentication → Settings → Authorized domains** and ensure both domains are listed:
   - `virtualcube.streamlit.app`
   - `virtualcube-571b7.web.app`

The Firebase Hosting sign-in component is deployed from the repository root with:

```bash
npm install -g firebase-tools
firebase login
firebase use virtualcube-571b7
firebase deploy --only hosting
```

## Optional server-side ID-token verification

This project is a client-side cube demo and currently has no protected user data or backend API. Without Firebase Admin credentials, Firebase sign-in gates the Streamlit UI, but the app does not claim server-side identity verification.

If you later want the Streamlit server to verify every token, configure a Firebase Admin service account:

1. In Firebase Console, open **Project settings → Service accounts → Generate new private key** and download the JSON file.
2. In Streamlit Community Cloud, open **Manage app → Settings → Secrets** and add:

```toml
[firebase_admin]
service_account_json = '''
PASTE THE ENTIRE SERVICE-ACCOUNT JSON FILE CONTENTS HERE
'''
```

Replace the placeholder with the full JSON file contents. Never commit the service-account file or its private key to GitHub or share it in chat. Save the secrets and reboot the Streamlit app. When this optional section is present, the app verifies the Firebase ID token server-side; invalid credentials will stop the app rather than bypass verification.

## Run locally

Python 3.10–3.12 recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 and allow camera access. The hosted Firebase sign-in page must be deployed and Google Authentication must be enabled.

## Troubleshooting

- **Google sign-in says unauthorized domain**: add the exact hostname in Firebase Authentication's authorized domains.
- **Firebase server-side token verification failed**: check that the service-account JSON belongs to `virtualcube-571b7`, is complete, and is configured only in Streamlit Secrets.
- **Sign-in succeeds but cube stays locked**: refresh the Streamlit app and confirm the Firebase Hosting component loads successfully.

Stack: Python, Streamlit, OpenCV, Firebase Authentication, Firebase Admin (optional), Google Sign-In, MediaPipe Hands, Three.js.
