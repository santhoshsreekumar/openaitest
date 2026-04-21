import os
import streamlit as st
from openai import OpenAI

# Configure Streamlit page
st.set_page_config(
    page_title="OpenAI Query App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_client():
    """Initialize OpenAI client with API key from environment or sidebar"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        api_key = st.sidebar.text_input(
            "Enter your OpenAI API Key",
            type="password",
            help="Your API key is never stored or logged"
        )
    
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'client' not in st.session_state:
        st.session_state.client = initialize_client()

def main():
    st.title("🤖 OpenAI Model Query App")
    st.markdown("*Query OpenAI models with an interactive chat interface*")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        model = st.selectbox(
            "Select Model",
            ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            help="Choose which OpenAI model to use"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher values = more creative, Lower values = more focused"
        )
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=500,
            step=100,
            help="Maximum length of the response"
        )
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    if st.session_state.client is None:
        st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to continue.")
        return
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare messages for API call
                    messages_for_api = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages
                    ]
                    
                    # Call OpenAI API
                    response = st.session_state.client.chat.completions.create(
                        model=model,
                        messages=messages_for_api,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    # Extract and display response
                    assistant_message = response.choices[0].message.content
                    st.markdown(assistant_message)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    # Remove the user message if API call failed
                    st.session_state.messages.pop()

if __name__ == "__main__":
    main()