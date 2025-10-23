import streamlit as st
import requests
import logging

from core.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Hackathon Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)


def api_call(method, url, **kwargs):

    def _show_error_popup(message):
        """Show error message as a popup in the top-right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }

    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid response format from server"}

        if response.ok:
            return True, response_data

        return False, response_data

    except requests.exceptions.ConnectionError:
        _show_error_popup("Connection error. Please check your network connection.")
        return False, {"message": "Connection error"}
    except requests.exceptions.Timeout:
        _show_error_popup("The request timed out. Please try again later.")
        return False, {"message": "Request timeout"}
    except Exception as e:
        _show_error_popup(f"An unexpected error occurred: {str(e)}")
        return False, {"message": str(e)}


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

if "used_context" not in st.session_state:
    st.session_state.used_context = []


with st.sidebar:
    # Create tabs in the sidebar
    suggestions_tab, settings_tab = st.tabs(["🔍 Suggestions", "⚙️ Settings"])
    
    # Settings Tab
    with settings_tab:
        st.subheader("Authentication")
        
        # Password input
        app_password = st.text_input(
            "Application Password", 
            type="password",
            help="Enter the application password to access the API",
            placeholder="Enter password..."
        )
        
        if app_password:
            st.success("✅ Password entered")
        else:
            st.warning("⚠️ Please enter the password")
    
    # Suggestions Tab
    with suggestions_tab:
        if st.session_state.used_context:
            for idx, item in enumerate(st.session_state.used_context):
                st.caption(item.get('project_description', 'No description'))
                st.caption(f"Link: {item['project_link']}")
                st.divider()
        else:
            st.info("No suggestions yet")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello! How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Check if password is provided
        if not app_password:
            st.error("❌ Please enter the application password in the Settings tab")
            # error should be displayed in the chat
            st.session_state.messages.append({"role": "assistant", "content": "❌ Please enter the application password in the Settings tab"})
        else:
            # Prepare request payload with password
            payload = {
                "query": prompt,
                "password": app_password
            }
            status, output = api_call("post", f"{config.API_URL}/rag", json=payload)
            
            if status:
                answer = output["answer"]
                used_context = output["used_context"]
                st.session_state.used_context = used_context
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = output.get("detail", "Unknown error occurred")
                if "Invalid password" in error_msg:
                    st.error("❌ Invalid password. Please check your password in the Settings tab.")
                else:
                    st.error(f"❌ Error: {error_msg}")

    st.rerun()