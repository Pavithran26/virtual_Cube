import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="virtual_Cube",
    page_icon="🧊",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    .stApp {
        background: radial-gradient(ellipse at top, #172746, #080c16 65%);
        color: #eef4ff;
        font-family: 'Space Grotesk', sans-serif;
    }
    header, footer { visibility: hidden; }
    .block-container { padding-top: 1rem; max-width: 1600px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "## 🧊 virtual_Cube · "
    "<span style='font-size:13px;color:#9db1d2'>REAL-TIME HAND TRACKING LAB</span>",
    unsafe_allow_html=True,
)
st.caption(
    "Open palm = rotate the whole cube · Select a face, then pinch and drag to turn it."
)
st.info(
    "Sign in with Google inside the cube below. If your browser blocks camera access "
    "inside the embedded view, open the full-screen version using the link underneath."
)

# Use a normal URL iframe, not a declared Streamlit custom component. This avoids the
# custom-component componentReady handshake entirely. Firebase Auth and the cube run
# together on the Firebase Hosting origin, where HTTPS and browser storage are available.
components.iframe(
    "https://virtualcube-571b7.web.app/",
    height=850,
    scrolling=True,
)

st.markdown(
    "[Open virtual_Cube full-screen](https://virtualcube-571b7.web.app/)",
)
