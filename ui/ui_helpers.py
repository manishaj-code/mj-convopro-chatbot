import streamlit as st
from datetime import datetime
import time

def apply_custom_css():
    """Apply premium custom CSS styling"""
    st.markdown("""
    <style>
        /* ==================== ROOT STYLES ==================== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            scroll-behavior: smooth;
        }

        /* ==================== MAIN CONTAINER ==================== */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 0;
        }

        /* ==================== SIDEBAR STYLING ==================== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1f3a 0%, #2d1b3d 100%);
            padding: 0 !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #1a1f3a 0%, #2d1b3d 100%) !important;
            padding: 0 !important;
        }

        /* Sidebar content */
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p {
            color: white !important;
        }

        /* Sidebar selectbox */
        [data-testid="stSidebar"] .stSelectbox label {
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }

        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 2px solid #667eea !important;
        }

        /* Sidebar buttons - TRANSPARENT WITH HOVER EFFECT */
        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
            margin: 0.5rem 0 !important;
            padding: 0.7rem 0.5rem !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.1) !important;
            transform: translateX(5px) !important;
            box-shadow: none !important;
        }

        /* ==================== HEADER SECTION ==================== */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2.5rem;
            color: white;
            text-align: center;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
            animation: slideDown 0.6s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header-title {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
            letter-spacing: -1px;
        }

        .header-subtitle {
            font-size: 1.1rem;
            opacity: 0.95;
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        /* ==================== CHAT MESSAGES ==================== */
        .chat-message-user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.3rem 1.6rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            margin-left: auto;
            max-width: 85%;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            border-bottom-right-radius: 8px;
            animation: slideInRight 0.4s ease-out;
            word-wrap: break-word;
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .chat-message-assistant {
            background: white;
            color: #2d1b3d;
            padding: 1.3rem 1.6rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            margin-right: auto;
            max-width: 85%;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            border-left: 5px solid #667eea;
            border-bottom-left-radius: 8px;
            animation: slideInLeft 0.4s ease-out;
            word-wrap: break-word;
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .message-content {
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .message-author {
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: block;
        }

        /* ==================== TIMESTAMP ==================== */
        .timestamp {
            font-size: 0.75rem;
            margin-top: 0.8rem;
            opacity: 0.7;
            font-style: italic;
        }

        /* ==================== EMPTY STATE ==================== */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: white;
            animation: fadeIn 0.6s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-20px);
            }
        }

        .empty-state-title {
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 0.8rem;
        }

        .empty-state-subtitle {
            font-size: 1rem;
            opacity: 0.9;
        }

        /* ==================== CHAT TITLE DISPLAY ==================== */
        .chat-title-display {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.2rem 1.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            border-left: 6px solid #667eea;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            animation: slideDown 0.5s ease-out;
        }

        .chat-title-text {
            font-size: 1rem;
            color: #2d1b3d;
            font-weight: 600;
        }

        /* ==================== INFO/ERROR BOXES ==================== */
        .info-box {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left: 6px solid #2196F3;
            padding: 1.3rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #1565c0;
            font-weight: 500;
            animation: slideDown 0.4s ease-out;
        }

        .error-box {
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
            border-left: 6px solid #f44336;
            padding: 1.3rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #c62828;
            font-weight: 500;
            animation: shake 0.3s ease-out;
        }

        @keyframes shake {
            0%, 100% {
                transform: translateX(0);
            }
            25% {
                transform: translateX(-5px);
            }
            75% {
                transform: translateX(5px);
            }
        }

        .warning-box {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            border-left: 6px solid #ff9800;
            padding: 1.3rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #e65100;
            font-weight: 500;
        }

        .success-box {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-left: 6px solid #4caf50;
            padding: 1.3rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #2e7d32;
            font-weight: 500;
        }

        /* ==================== CHAT INPUT ==================== */
        .stChatInput input {
            border-radius: 15px !important;
            border: 2px solid #667eea !important;
            padding: 1rem !important;
            font-size: 0.95rem !important;
            background: white !important;
            color: #2d1b3d !important;
            transition: all 0.3s ease !important;
        }

        .stChatInput input:focus {
            border-color: #764ba2 !important;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.3) !important;
        }

        .stChatInput input::placeholder {
            color: #999 !important;
        }

        /* ==================== BUTTONS ==================== */
        .stButton > button {
            border-radius: 12px !important;
            border: none !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
            padding: 0.8rem 1.5rem !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
        }

        /* ==================== BADGES ==================== */
        .model-badge {
            background: rgba(255, 255, 255, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 1.2rem;
            border-radius: 15px;
            font-size: 0.9rem;
            margin: 1.5rem 0;
            font-weight: 600;
            animation: slideDown 0.5s ease-out;
        }

        .provider-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            margin: 0.3rem;
        }

        /* ==================== DIVIDER ==================== */
        .stDivider {
            margin: 2rem 0 !important;
            border: none !important;
            border-top: 2px solid rgba(255, 255, 255, 0.2) !important;
        }

        /* ==================== FOOTER ==================== */
        .footer-text {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.85rem;
            padding: 2rem 1rem;
            border-top: 2px solid rgba(255, 255, 255, 0.1);
            margin-top: 3rem;
        }

        .footer-text p {
            margin: 0.3rem 0;
        }

        /* ==================== RESPONSIVE ==================== */
        @media (max-width: 768px) {
            .header-title {
                font-size: 2.5rem;
            }

            .chat-message-user,
            .chat-message-assistant {
                max-width: 95%;
            }

            .empty-state-icon {
                font-size: 3rem;
            }
        }

        /* ==================== SCROLLBAR ==================== */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }

        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
        }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    """Display premium app header with animation"""
    st.markdown("""
    <div class='header-container'>
        <div class='header-title'>💬 ConvoPro</div>
        <div class='header-subtitle'>✨ Your Intelligent AI Assistant</div>
    </div>
    """, unsafe_allow_html=True)

def show_user_message(content: str):
    """Display user message with animation"""
    st.markdown(f"""
    <div class='chat-message-user'>
        <span class='message-author'>👤 You</span>
        <div class='message-content'>{content}</div>
        <div class='timestamp'>{datetime.now().strftime('%H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

def show_assistant_message(content: str):
    """Display assistant message with animation"""
    st.markdown(f"""
    <div class='chat-message-assistant'>
        <span class='message-author'>🤖 ConvoPro</span>
        <div class='message-content'>{content}</div>
        <div class='timestamp'>{datetime.now().strftime('%H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

def show_error(message: str):
    """Display error message"""
    st.markdown(f"""
    <div class='error-box'>
        <strong>❌ Error:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def show_warning(message: str):
    """Display warning message"""
    st.markdown(f"""
    <div class='warning-box'>
        <strong>⚠️ Warning:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def show_info(message: str):
    """Display info message"""
    st.markdown(f"""
    <div class='info-box'>
        <strong>ℹ️ Info:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def show_success(message: str):
    """Display success message"""
    st.markdown(f"""
    <div class='success-box'>
        <strong>✅ Success:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def show_empty_state():
    """Display empty state when no messages"""
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-state-icon'>💭</div>
        <div class='empty-state-title'>Start a Conversation!</div>
        <div class='empty-state-subtitle'>Ask me anything and I'll help you...</div>
    </div>
    """, unsafe_allow_html=True)

def show_provider_info(provider: str, model: str, provider_info: dict):
    """Display current provider and model info"""
    info = provider_info.get(provider, {})
    st.markdown(f"""
    <div class='model-badge'>
        <div style='margin-bottom: 0.8rem; font-size: 1.1rem;'>📍 Current Setup</div>
        <div style='line-height: 1.8;'>
            <strong>{info.get("icon", "🔌")} Provider:</strong> <span class='provider-badge'>{provider.upper()}</span><br>
            <strong>🤖 Model:</strong> <span class='provider-badge'>{model}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_stats(total_conversations: int, total_messages: int = 0):
    """Display chat statistics"""
    st.markdown(f"""
    <div style='background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 12px; margin: 1rem 0;'>
        <div style='display: flex; justify-content: space-around; text-align: center; color: white;'>
            <div>
                <div style='font-size: 1.8rem; font-weight: 800;'>{total_conversations}</div>
                <div style='font-size: 0.85rem; opacity: 0.8;'>Conversations</div>
            </div>
            <div style='border-left: 2px solid rgba(255, 255, 255, 0.2);'></div>
            <div>
                <div style='font-size: 1.8rem; font-weight: 800;'>💬</div>
                <div style='font-size: 0.85rem; opacity: 0.8;'>Active Chat</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_footer():
    """Display footer"""
    st.divider()
    st.markdown("""
    <div class='footer-text'>
        <p><strong>💬 ConvoPro v1.0</strong> | Your Private AI Assistant</p>
        <p>Built with ❤️ | Powered by Groq AI</p>
        <p style='margin-top: 1rem; opacity: 0.6;'>© 2024 ConvoPro. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def show_loading_animation(text: str = "Loading..."):
    """Show loading animation"""
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem;'>
        <div style='font-size: 2rem; animation: bounce 1s infinite;'>⏳</div>
        <p style='margin-top: 1rem; color: #666;'>{text}</p>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar_header():
    """Show enhanced sidebar header"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem 1rem; background: rgba(255,255,255,0.05); border-radius: 15px; margin-bottom: 1.5rem;'>
        <div style='font-size: 2.8rem; margin-bottom: 0.5rem;'>💬</div>
        <h2 style='font-size: 1.8rem; margin: 0.5rem 0 0 0; color: white; font-weight: 800;'>ConvoPro</h2>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: rgba(255,255,255,0.8);'>AI Chat Assistant</p>
    </div>
    """, unsafe_allow_html=True)

def show_conversation_item(title: str, is_current: bool = False):
    """Show individual conversation item in sidebar"""
    bg_color = "rgba(255,255,255,0.15)" if is_current else "rgba(255,255,255,0.05)"
    border = "left: 4px solid #ffd700;" if is_current else ""
    icon = "📌" if is_current else "💬"
    
    st.markdown(f"""
    <div style='background: {bg_color}; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; {border}'>
        {icon} <strong>{title[:30]}</strong>
    </div>
    """, unsafe_allow_html=True)