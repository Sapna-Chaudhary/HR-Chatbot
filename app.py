import streamlit as st
from hr_backend import hr_bot

# Demo users
USERS = {
    "hr": "hr123",
    "emp005": "sapna123",
    "emp002": "ankit123",
    "emp001" : "amit123",
    "admin": "admin123",
    "emp003" : "ravi123",
    "emp004" : "mohit123"
}
# Login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.set_page_config(
    page_title="HR Assistant",
    page_icon="🏢",
    layout="wide"
)
# Login screen
if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        username = username.lower()

        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()

        else:
            st.error("Invalid username or password.")

    st.stop()
# Logout button
with st.sidebar:
    st.write(f"Logged in as: {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    

st.markdown(
    """
    <div style='text-align:center;'>
        <h1>🏢 PyApp Technologies Pvt. Ltd.</h1>
        <h3>HR Assistant Portal</h3>
        <p>AI-Powered Employee Support System</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.sidebar.title("🏢 HR Assistant")

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Capabilities")

st.sidebar.markdown("""
✅ Employee Information

✅ Manager Details

✅ Leave Information

✅ Attendance Details

✅ HR Handbook Policies
""")

st.sidebar.markdown("---")

st.sidebar.subheader("💡 Example Questions")

st.sidebar.markdown("""
- Who is Sapna's manager?
- What is Sapna's CL balance?
- What department does Ankit work in?
- When did Sapna join?
- What is the leave policy?
- Show Sapna's attendance percentage.
""")

st.sidebar.markdown("---")

st.sidebar.caption("🤖 Powered by Ollama + FAISS + Streamlit")



# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
question = st.chat_input("Ask your HR question...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = hr_bot(question)

        st.write(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )