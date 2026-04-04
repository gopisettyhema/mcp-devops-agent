import streamlit as st
import requests

# Your deployed Cloud Run URL
API_URL = "https://mcp-agent-591209795062.asia-south1.run.app/chat"

st.set_page_config(page_title="MCP DevOps Agent", layout="centered")

st.title("🤖 MCP DevOps AI Agent")
st.write("Ask questions about GitHub repositories")

# Input box
user_input = st.text_input("Enter your query:",
                          placeholder="e.g. Show github issues for octocat/Hello-World")

# Button
if st.button("Submit"):

    if not user_input:
        st.warning("Please enter a question")
    else:
        with st.spinner("Fetching data..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": user_input}
                )

                result = response.json()

                st.success("Response:")
                st.markdown(result.get("response", "No response"))

            except Exception as e:
                st.error(f"Error: {str(e)}")