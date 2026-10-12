# Firebase Web Client (virtual_Cube)

This directory contains the production web client hosted on Firebase Hosting (`https://virtualcube-571b7.web.app`).

It provides:
- Firebase Google Authentication gate
- 3D Rubik's Cube simulation powered by Three.js
- Real-time client-side hand tracking with MediaPipe Hands
- Holographic 3D skeletal hand mesh and interactive gesture controls

Deploy changes from the repository root:
```powershell
firebase deploy --project virtualcube-571b7 --only hosting
```
