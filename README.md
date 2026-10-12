# virtual_Cube 🧊

A browser-based, webcam-driven virtual Rubik's Cube using Streamlit, Three.js, MediaPipe Hands, and Firebase Google sign-in.

## How it works

The cube and Firebase Google sign-in now run together on Firebase Hosting at **https://virtualcube-571b7.web.app**. The Streamlit page embeds that regular HTTPS page in an iframe. This intentionally avoids a custom Streamlit component handshake, which was repeatedly failing in the deployed app.

## Features

- Google sign-in UI powered by Firebase Authentication.
- Interactive 3D 3×3 cube with six colored faces.
- A live holographic 3D hand is rendered from MediaPipe’s 21 hand landmarks, with glowing joints, connected finger bones, and a translucent palm.
- Open palm motion rotates the whole cube in real time with bounded, smoother movement.
- Select U / D / L / R / F / B, then pinch and drag to turn a face.
- Light glassmorphism UI with frosted panels, reflective edges, soft shadows, and cyan/violet ambient lighting.
- Tutorial, scramble, and reset controls.
- Hand landmarks are processed in the browser; this app does not upload or record video.

## Deploy changes

The Firebase Hosting folder is `firebase-auth-component`, configured in `firebase.json`.

From the repository root, update local files and deploy the hosted cube page:

```powershell
git pull
firebase deploy --project virtualcube-571b7 --only hosting
```

The Streamlit Community Cloud app should rebuild from the connected GitHub branch after `app.py` changes. If it does not, open **Manage app → Reboot app**.

## Firebase Console setup

In Firebase Console for project `virtualcube-571b7`:

1. Open **Authentication → Sign-in method** and enable **Google**. Select a support email if prompted.
2. Open **Authentication → Settings → Authorized domains** and ensure both hostnames are listed:
   - `virtualcube.streamlit.app`
   - `virtualcube-571b7.web.app`

The Firebase Web config is client-side configuration. Never place a service-account private key in this file or in GitHub.

## Run locally

Python 3.10–3.12 recommended.

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Security note

This is an interactive client-side demo. Firebase sign-in gates the UI, but it does not replace server-side authorization for protected APIs or private data. If protected backend resources are added later, verify Firebase ID tokens on the server and enforce authorization there.

## Troubleshooting

- **Google sign-in says unauthorized domain:** add the exact host in Firebase Authentication's authorized domains.
- **Camera does not start in the embedded view:** click **Open virtual_Cube full-screen** below the embedded app, then allow camera access in the browser.
- **The iframe shows the older login-only page:** deploy Hosting again with the command above.

Stack: Python, Streamlit, OpenCV, Firebase Authentication, Google Sign-In, MediaPipe Hands, Three.js.
