
import streamlit as st
from agent import agent_executor

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Atlas AI Assistant",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS - LIGHT THEME
# ==========================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #F8FAFC !important;
    color: #1E293B !important;
}

[data-testid="stAppViewContainer"] {
    background: #F8FAFC !important;
}

[data-testid="stHeader"] {
    background: #F8FAFC !important;
}

/* Main content */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5EAF1;
}

[data-testid="stSidebar"] * {
    color: #334155;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172B4D !important;
}

[data-testid="stSidebar"] p {
    color: #64748B !important;
}

/* Hero section */
.hero {
    background: linear-gradient(
        120deg,
        #EAF2FF,
        #F4F7FF
    );
    padding: 32px;
    border-radius: 18px;
    border: 1px solid #DCE8FA;
    margin-bottom: 28px;
}

.hero h1 {
    color: #172B4D !important;
    font-size: 32px;
    font-weight: 700;
}

.hero p {
    color: #64748B !important;
    font-size: 16px;
}

/* Feature cards */
.feature-card {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #E5EAF1;
    min-height: 145px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

.feature-card h3 {
    color: #1E3A5F !important;
    font-size: 18px;
}

.feature-card p {
    color: #64748B !important;
    font-size: 14px;
}

/* Chat section */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #E8EDF4;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    background: #FFFFFF;
}

/* Buttons */
.stButton > button {
    background: #FFFFFF;
    color: #334155 !important;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 10px 14px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #EFF6FF;
    color: #2563EB !important;
    border-color: #93C5FD;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #F8FAFC;
    color: #334155 !important;
    border: 1px solid #E5EAF1;
    text-align: left;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #EFF6FF;
    border-color: #93C5FD;
}

/* Headings */
h1, h2, h3 {
    color: #172B4D !important;
}

/* Divider */
hr {
    border-color: #E5EAF1 !important;
}


/* =================================
   CHAT INPUT - TEXT VISIBILITY FIX
================================= */

/* Chat input container */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE3ED !important;
    border-radius: 14px !important;
}

/* Actual typing area */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputTextArea"] {
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    background-color: #FFFFFF !important;
    caret-color: #2563EB !important;
    font-size: 16px !important;
}

/* Placeholder text */
[data-testid="stChatInput"] textarea::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
}

/* Focus state */
[data-testid="stChatInput"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
}

/* Chat input toolbar */
[data-testid="stChatInput"] button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border-radius: 9px !important;
}


</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🌤️ Atlas AI")

    st.caption("Your Research & Weather Assistant")

    st.divider()

    st.markdown("### 🧭 Capabilities")

    st.markdown("""
    **🔎 Web Research**

    Search the internet for useful information.

    **🌦️ Weather Updates**

    Get current weather information for any city.

    **🤖 AI Assistant**

    Ask questions using natural language.
    """)

    st.divider()

    st.markdown("### 💡 Example Prompts")

    examples = [
        "Find the capital of India and its weather.",
        "What is artificial intelligence?",
        "Search for the latest AI developments.",
        "Tell me the current weather in Mumbai."
    ]

    for example in examples:

        if st.button(
            example,
            use_container_width=True,
            key=f"example_{examples.index(example)}"
        ):
            st.session_state.pending_prompt = example

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Gemini • Tavily • Weatherstack")


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown("""
<div class="hero">

    <h1>👋 Your AI Research Assistant</h1>

    <p>
        Ask questions, search the web and explore
        current weather conditions with your intelligent AI agent.
    </p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# FEATURE CARDS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="feature-card">

        <h3>🔎 Web Research</h3>

        <p>
            Find useful information from the internet
            using intelligent web search.
        </p>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="feature-card">

        <h3>🌦️ Weather Information</h3>

        <p>
            Get current temperature, weather conditions
            and humidity for your city.
        </p>

    </div>
    """, unsafe_allow_html=True)


st.write("")
st.divider()


# ==========================================
# CHAT INTERFACE
# ==========================================

st.markdown("### 💬 Chat with Atlas AI")

if not st.session_state.messages:

    st.info(
        "Welcome! Ask me anything to get started."
    )


# Display chat history

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# USER INPUT
# ==========================================

prompt = st.chat_input(
    "Ask anything or check the weather..."
)

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# ==========================================
# AGENT EXECUTION
# ==========================================

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Atlas AI is thinking..."
        ):

            try:

                response = agent_executor.invoke({
                    "input": prompt
                })

                answer = response["output"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"Error: {str(e)}")


# ==========================================
# FOOTER
# ==========================================

st.write("")

st.caption(
    "Atlas AI • Intelligent Research & Weather Assistant"
)
