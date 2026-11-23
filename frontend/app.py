"""Streamlit user interface for the Secure Multimodal AI Companion."""

import streamlit as st
from frontend.config import APP_TITLE, APP_ICON, APP_SUBTITLE
from frontend.services.api_client import api_client

# Streamlit Page Setup
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom minimal modern styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .status-healthy {
        background-color: #d1e7dd;
        color: #0f5132;
    }
    .status-unreachable {
        background-color: #f8d7da;
        color: #842029;
    }
    .safety-banner {
        background-color: #f0f7ff;
        border-left: 4px solid #0d6efd;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption("v1.0.0-MVP")

    st.markdown("---")
    st.subheader("System Status")
    health = api_client.check_health()
    if health.get("status") == "healthy":
        st.markdown(
            '<span class="status-badge status-healthy">● Backend Online</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Database: {health.get('database', {}).get('type', 'Connected')}")
        st.caption(f"LLM Provider: {health.get('providers', {}).get('llm', 'Ready')}")
    else:
        st.markdown(
            '<span class="status-badge status-unreachable">○ Backend Offline</span>',
            unsafe_allow_html=True,
        )
        st.warning("FastAPI backend is not reachable. Please start the backend service.")

    st.markdown("---")
    st.subheader("Active Modalities")
    st.markdown("- 💬 **Text**: Full conversational continuity")
    st.markdown("- 📄 **RAG Documents**: PDF, DOCX, TXT, MD")
    st.markdown("- 🖼️ **Vision**: Image analysis & visual QA")
    st.markdown("- 🎙️ **Audio**: Speech-to-text & Text-to-speech")

    st.markdown("---")
    st.info(
        "**AI Companion Safety Notice**\n\n"
        "This assistant provides supportive, empathetic conversations. It is an AI system and not a licensed mental health professional, doctor, or crisis counselor."
    )

# Main Application Window
st.markdown(f'<div class="main-header">{APP_ICON} {APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="safety-banner">
        <strong>🔒 Security & Privacy Notice:</strong> This MVP runs in a controlled single-user environment.
        Retrieved document fragments are treated as untrusted data, and crisis safeguards are active at all times.
    </div>
    """,
    unsafe_allow_html=True,
)

# Conversation Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your AI Companion. I'm here to listen, support, and help answer your questions—whether you want to talk through how you're feeling, explore ideas, or ask questions about documents and images you upload. How can I assist you today?",
        }
    ]

# Render chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input widget
if prompt := st.chat_input("Share your thoughts or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initial placeholder response for Phase 1
    with st.chat_message("assistant"):
        response_text = f"Thank you for sharing. I hear you. [Phase 1 Foundation Active - Chat Orchestration connects in Phase 2]"
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
