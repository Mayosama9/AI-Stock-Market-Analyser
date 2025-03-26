import streamlit as st
from ai_chat import chat_with_ai

st.set_page_config(page_title="AI Chat Assistant", layout="wide")
st.title("💬 AI Financial Analyst")
print(st.session_state.ai_summary)
# Ensure chat history is initialized
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an AI financial analyst."}
    ]
    if "ticker" in st.session_state and "ai_summary" in st.session_state:
        st.session_state.chat_history.append(
            {"role": "user", "content": f"Stock analysis for {st.session_state.ticker}:\n\n"
                       f"{st.session_state.ai_summary}\n\n"
                       f"📊 **Recent Stock Prices:**\n```\n{st.session_state.stock_data}\n```"}
        )

# Display existing chat messages (excluding system message)
for chat in st.session_state.chat_history[2:]:
    with st.chat_message("user" if chat["role"] == "user" else "assistant"):
        st.markdown(chat["content"])

# Chat input (without reload)
if user_query := st.chat_input("Ask anything about stocks:"):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_query)

    # Append user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Get AI response
    chat_response = chat_with_ai(st.session_state.chat_history)

    # Display AI response immediately
    with st.chat_message("assistant"):
        st.markdown(chat_response)

    # Append AI response to history
    st.session_state.chat_history.append({"role": "assistant", "content": chat_response})
