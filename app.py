import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.base import BaseCallbackHandler
from tools import tools

st.title("🧠 Agentic Healthcare Assistant")
st.warning("This is not medical advice. For educational purposes only.")

# 🔑 API key
groq_api_key = st.text_input("Enter your GROQ API Key:", type="password")

# 💬 Query
query = st.text_input("Ask a healthcare question:")


# 🔁 Callback Handler (for live tool + token streaming)
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.container.markdown(f"🛠 **Using Tool:** {serialized['name']}")
        self.container.markdown(f"📥 Input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        self.container.markdown(f"📤 Output: {output}")
        self.container.markdown("---")

    def on_llm_new_token(self, token, **kwargs):
        self.text += token
        self.container.markdown(self.text)


# 🚀 Run
if st.button("Run Query"):

    if not groq_api_key:
        st.error("Please enter your Groq API key.")

    elif not query:
        st.error("Please enter a question.")

    else:
        try:
            # LLM with streaming
            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model="llama-3.1-8b-instant",
                temperature=0,
                streaming=True
            )

            # UI containers
            reasoning_box = st.expander("🔍 Agent Reasoning (Live)", expanded=True)
            answer_box = st.empty()

            callback_handler = StreamlitCallbackHandler(reasoning_box)

            # Agent with loop control + better prompt
            agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                max_iterations=5,
                early_stopping_method="generate",
                agent_kwargs={
                    "prefix": """You are a healthcare assistant.

Use tools ONLY if needed.
Do NOT call tools repeatedly.
After getting enough information, give FINAL ANSWER clearly.

Avoid loops and unnecessary tool usage."""
                },
                callbacks=[callback_handler]
            )

            with st.spinner("Thinking..."):
                response = agent.run(query)

            answer_box.subheader("Final Answer")
            answer_box.write(response)

        except Exception as e:
            st.error(f"Error: {str(e)}")