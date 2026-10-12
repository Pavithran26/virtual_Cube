import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="virtual_Cube",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
    .stApp {
        color: #1d3150;
        font-family: 'Space Grotesk', sans-serif;
        background:
            radial-gradient(ellipse at 10% 8%, rgba(122,204,255,.32), transparent 32%),
            radial-gradient(ellipse at 90% 12%, rgba(197,174,255,.25), transparent 31%),
            radial-gradient(ellipse at 62% 100%, rgba(144,242,220,.22), transparent 38%),
            linear-gradient(135deg, #f7fbff 0%, #edf5ff 48%, #f8f5ff 100%);
    }
    header, footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 1rem; padding-bottom: .5rem; max-width: 1700px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='color:#1b2e4b;letter-spacing:-.055em;margin-bottom:0'>"
    "🧊 virtual_Cube <span style='font-size:13px;letter-spacing:.12em;"
    "color:#6d83a4;font-weight:700'>HAND-TRACKING PLAYGROUND</span></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#637995;margin-top:8px'>Sign in, choose <b>Play Guide</b> "
    "to learn the gestures, or choose <b>Play</b> for an immersive cube-only view. "
    "Your camera feed stays hidden; only hand tracking is used.</p>",
    unsafe_allow_html=True,
)

# The hosted page owns Firebase sign-in and the gameplay. Play opens a top-level
# Firebase tab so camera permission and immersive fullscreen are not constrained
# by the Streamlit iframe.
components.iframe(
    "https://virtualcube-571b7.web.app/",
    height=870,
    scrolling=True,
)

st.markdown(
    "<div style='text-align:center;color:#8193ad;font-size:11px;padding:2px 0 8px'>"
    "Light glass UI · Real-time hand tracking · Video stays in your browser"
    "</div>",
    unsafe_allow_html=True,
)
