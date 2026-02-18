import streamlit as st
import tempfile
import os
from rag_engine import PDFQAAgent

# Page Configuration
st.set_page_config(
    page_title="PDF Insight Agent",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for a better look
st.markdown("""
    <style>
    .stChatInput {
        padding-bottom: 20px;
    }
    .stMarkdown h1 {
        color: #4A90E2; 
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "agent" not in st.session_state:
    st.session_state.agent = None

if "agent_error" not in st.session_state:
    st.session_state.agent_error = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False


def _ensure_agent():
    """Lazily initialize the agent on first use."""
    if st.session_state.agent is None:
        st.session_state.agent = PDFQAAgent()


# Sidebar UI
with st.sidebar:
    st.title("📂 Document Center")
    st.write("Upload a PDF to start chatting.")
    
    uploaded_files = st.file_uploader("Choose PDF file(s)", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        with st.status("Processing Documents...", expanded=True) as status:
            total_chunks = 0
            for uploaded_file in uploaded_files:
                # Check if this file has already been processed (simple check by name)
                # In a real app, hash checking would be better
                if uploaded_file.name not in st.session_state.get('processed_files', dict()):
                     st.write(f"📥 Reading {uploaded_file.name}...")
                     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                         tmp.write(uploaded_file.read())
                         tmp_path = tmp.name
                     
                     try:
                         _ensure_agent()
                         num_chunks = st.session_state.agent.load_pdf(tmp_path)
                         total_chunks += num_chunks
                         
                         # Mark as processed
                         if 'processed_files' not in st.session_state:
                             st.session_state.processed_files = {}
                         st.session_state.processed_files[uploaded_file.name] = True
                         
                         st.write(f"✅ {uploaded_file.name}: Added {num_chunks} chunks.")
                     except Exception as e:
                         st.error(f"Failed to process {uploaded_file.name}: {e}")
                     finally:
                         os.unlink(tmp_path)
            
            if total_chunks > 0:
                st.session_state.pdf_processed = True
                status.update(label="✅ Ready!", state="complete", expanded=False)
                st.success(f"Processed {total_chunks} new chunks!")

    if st.session_state.pdf_processed:
        st.divider()
        st.write("✅ Document Active")
        if st.button("🗑️ Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()
        if st.button("🔄 Reset Documents"):
            st.session_state.agent = PDFQAAgent() # Re-init agent to clear vectorstore
            st.session_state.pdf_processed = False
            st.session_state.processed_files = {} # Clear tracked files
            st.session_state.chat_history = []
            st.rerun()

# Main Chat UI
st.title("🧠 PDF Insight Agent")
st.caption("Powered by RAG & Groq (Llama 3.3) - Chat with PDFs or ask General Questions")

# Show API key warning if needed
api_key = os.getenv("GROQ_API_KEY", "")
if not api_key:
    st.warning("⚠️ GROQ_API_KEY is not set in your `.env` file. Please add it to use the chatbot.")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your PDF or anything else..."):
    # Ensure agent is initialized
    _ensure_agent()
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = st.session_state.agent.ask(prompt)
            st.markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
