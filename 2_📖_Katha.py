import streamlit as st
import boto3

# Main radio button
main_option = st.radio("Select Category:", ["Cross Border", "WW Stores Finance", "New Team"], horizontal=True)
st.divider()
# Sub radio buttons based on main selection
if main_option == "Cross Border":
    sub_option = st.radio("Select Cross Border Line Item:", ["MVR", "Ship-Cost", "P&L"], horizontal=True)
    
elif main_option == "WW Stores Finance":
    sub_option = st.radio("Select WW-Stores-Finance:", ["P&L", "OpEx", "xBR"], horizontal=True)
    
elif main_option == "New Team":
    sub_option = st.radio("Select New-Team:", ["P&L", "OpEx", "xBR"], horizontal=True)
st.divider()
# Display selection
if main_option:
    st.write(f"You selected: {main_option} → {sub_option}")


# Radio button selection

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.file_uploader("Upload Raw Data", type=['txt', 'pdf', 'docx'])
    
    with col2:
        st.file_uploader("Upload Metric Calculation", type=['txt', 'pdf', 'docx'])
    
    with col3:
        st.file_uploader("Upload Knowledge Base", type=['txt', 'pdf', 'docx'])
    st.divider()
    # Chat section
    st.subheader("Generated Narrative")
    # Chat input
    user_input = st.text_area("", height=100)
    copy_button = st.button("📋 Copy to Clipboard")
    st.divider()
  # Initialize Bedrock client
@st.cache_resource
def init_bedrock_client():
    return boto3.client('bedrock-runtime', region_name='us-east-1')

def call_bedrock_llm(prompt, client):
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.7,
        "top_p": 0.9,
    })
    
    response = client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2",
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body.get('completion')

st.subheader("Chat Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])




# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Bedrock
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = init_bedrock_client()
                response = call_bedrock_llm(prompt, client)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()