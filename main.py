import streamlit as st
from datetime import datetime

# Import services
from services import get_models_list, get_provider_info, get_chat_title, get_answer
from db import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
    delete_conversation
)
from ui import (
    apply_custom_css,
    show_header,
    show_user_message,
    show_assistant_message,
    show_error,
    show_warning,
    show_info,
    show_empty_state,
    show_provider_info,
    show_stats,
    show_footer,
    show_sidebar_header,
)

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="ConvoPro - AI Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# ============= LOAD DATA =============
if "MODELS" not in st.session_state:
    st.session_state.MODELS = get_models_list()

if "PROVIDER_INFO" not in st.session_state:
    st.session_state.PROVIDER_INFO = get_provider_info()

# ============= SESSION STATE =============
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])
default_provider = "groq" if "groq" in st.session_state.MODELS else "gemini"
st.session_state.setdefault("selected_provider", default_provider)
st.session_state.setdefault("selected_model", None)

# ============= SIDEBAR =============
with st.sidebar:
    # Sidebar Header
    show_sidebar_header()
    
    st.divider()
    
    # SETTINGS SECTION
    st.markdown("<div style='color: white; font-size: 1.3rem; font-weight: 800; margin: 1.5rem 0 1rem 0;'>⚙️ Settings</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Provider Selection with icons
    available_providers = list(st.session_state.MODELS.keys()) if st.session_state.MODELS else []
    
    if not available_providers:
        st.error("❌ No providers configured. Check .env file!")
    else:
        # Create provider options with icons
        provider_options = {
            "groq": "⚡ Groq - Ultra Fast",
            "gemini": "🔮 Gemini - Advanced",
        }
        
        display_options = [provider_options.get(p, p) for p in available_providers]
        
        selected_idx = st.selectbox(
            "🔧 Select Provider",
            range(len(available_providers)),
            format_func=lambda x: display_options[x],
            key="provider_select",
            help="Choose your AI provider"
        )
        selected_provider = available_providers[selected_idx]
        st.session_state.selected_provider = selected_provider
        
        # Model Selection
        available_models = st.session_state.MODELS.get(selected_provider, [])
        
        if not available_models:
            st.error(f"❌ No models for {selected_provider}")
        else:
            selected_model = st.selectbox(
                "🤖 Select Model",
                available_models,
                key="model_select",
                help="Choose your AI model"
            )
            st.session_state.selected_model = selected_model
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Current Setup Badge
    if st.session_state.selected_model:
        show_provider_info(
            st.session_state.selected_provider,
            st.session_state.selected_model,
            st.session_state.PROVIDER_INFO
        )
    
    st.divider()
    
    # CHAT HISTORY SECTION
    st.markdown("<div style='color: white; font-size: 1.3rem; font-weight: 800; margin: 1.5rem 0 1rem 0;'>💬 History</div>", unsafe_allow_html=True)
    
    # New Chat Button
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.conversation_id = None
            st.session_state.conversation_title = None
            st.session_state.chat_history = []
            st.rerun()
    
    st.divider()
    
    # Conversations List
    conversations = get_all_conversations()
    
    if conversations:
        st.markdown(f"<div style='color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-bottom: 1rem;'>📊 <strong>{len(conversations)}</strong> conversations</div>", unsafe_allow_html=True)
        
        # Search conversations
        search_query = st.text_input("🔍 Search chats...", "", key="search_convs", label_visibility="collapsed")
        
        for cid, title in conversations.items():
            # Filter by search
            if search_query.lower() not in title.lower():
                continue
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                is_current = cid == st.session_state.conversation_id
                label = f"📌 {title[:25]}" if is_current else f"💬 {title[:25]}"
                
                # ✅ REMOVED BACKGROUND - Clean button styling
                if st.button(label, use_container_width=True, key=f"conv_{cid}", help=title):
                    doc = get_conversation(cid) or {}
                    st.session_state.conversation_id = cid
                    st.session_state.conversation_title = doc.get("title", "Untitled")
                    st.session_state.chat_history = [
                        {"role": m["role"], "content": m["content"]}
                        for m in doc.get("messages", [])
                    ]
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{cid}", help="Delete conversation"):
                    if st.session_state.conversation_id == cid:
                        st.session_state.conversation_id = None
                        st.session_state.conversation_title = None
                        st.session_state.chat_history = []
                    delete_conversation(cid)
                    st.rerun()
    else:
        st.markdown("""
        <div style='text-align: center; color: rgba(255,255,255,0.7); padding: 2rem 0;'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📭</div>
            <p><strong>No conversations yet</strong></p>
            <p style='font-size: 0.85rem; opacity: 0.8;'>Start chatting to create history</p>
        </div>
        """, unsafe_allow_html=True)

# ============= MAIN CONTENT AREA =============

# Show header
show_header()

# Check if model is selected
if not st.session_state.selected_model:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("👈 **Step 1:** Choose Provider", icon="1️⃣")
    with col2:
        st.info("🤖 **Step 2:** Select Model", icon="2️⃣")
    with col3:
        st.info("💬 **Step 3:** Start Chatting", icon="3️⃣")
    
    st.markdown("<br>", unsafe_allow_html=True)
    show_warning("Please select a model from the sidebar to continue.")

else:
    # Display current chat title
    if st.session_state.conversation_title:
        st.markdown(f"""
        <div class='chat-title-display'>
            <div class='chat-title-text'>📝 <strong>Chat:</strong> {st.session_state.conversation_title}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    show_user_message(msg["content"])
                else:
                    show_assistant_message(msg["content"])
        else:
            show_empty_state()
    
    st.divider()
    
    # Chat input with interactive features
    col_input, col_buttons = st.columns([5, 1])
    
    with col_input:
        user_query = st.chat_input("💬 Type your message here...", key="chat_input")
    
    if user_query:
        # Display user message
        show_user_message(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Create or update conversation
        if st.session_state.conversation_id is None:
            with st.spinner("✨ Generating title..."):
                try:
                    title = get_chat_title(
                        st.session_state.selected_provider,
                        st.session_state.selected_model,
                        user_query
                    ) or "New Chat"
                except Exception as e:
                    title = "New Chat"
            
            conv_id = create_new_conversation(
                title=title,
                role="user",
                content=user_query
            )
            st.session_state.conversation_id = conv_id
            st.session_state.conversation_title = title
        else:
            add_message(st.session_state.conversation_id, "user", user_query)
        
        # Get assistant response
        with st.spinner("🤔 ConvoPro is thinking..."):
            try:
                assistant_text = get_answer(
                    st.session_state.selected_provider,
                    st.session_state.selected_model,
                    st.session_state.chat_history
                )
                show_assistant_message(assistant_text)
            
            except ValueError as e:
                error_msg = f"⚙️ Configuration Error: {str(e)}"
                show_error(error_msg)
                assistant_text = error_msg
            
            except Exception as e:
                error_msg = f"{str(e)}"
                show_error(error_msg)
                assistant_text = error_msg
        
        # Save to database
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": assistant_text
        })
        
        if st.session_state.conversation_id:
            add_message(
                st.session_state.conversation_id,
                "assistant",
                assistant_text
            )
        
        st.rerun()

# ============= FOOTER =============
show_footer()