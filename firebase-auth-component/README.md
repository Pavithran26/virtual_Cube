# Firebase auth component

This page is hosted on Firebase Hosting, outside the Streamlit iframe. It signs in with Firebase Google Authentication and returns the Firebase ID token using Streamlit's component protocol. The Python app must verify this token with Firebase Admin before rendering the cube.

Deploy from the repository root with Firebase CLI: `firebase deploy --only hosting`.
