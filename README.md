# 🧠 Agentic Healthcare Assistant

An AI-powered healthcare assistant built using LLMs and tool-based agents. The system dynamically selects external tools such as PubMed, Wikipedia, and web search to answer medical queries with transparency.

---

## 🚀 Live Demo

👉 Try the app here:
https://agentic-healthcare-assistant-nlt68lq8fuscnw7w5hqn9p.streamlit.app/

⚠️ You will need your own Groq API key to use the app.

## 🚀 Features

* 🔍 Multi-tool agent (Wikipedia, PubMed, Web Search, Drug Info, BMI Calculator)
* ⚡ Powered by Groq LLM (LLaMA3)
* 🔁 Real-time streaming responses
* 🛠 Tool usage visibility (agent reasoning)
* 🔐 User-provided API key (no hardcoding)

---

## 🧠 Architecture

User Query → LLM Agent → Tool Selection → Tool Output → Final Answer

---

## 🧰 Tech Stack

* Python
* Streamlit
* LangChain
* Groq (LLaMA3)
* APIs: PubMed, FDA, Wikipedia, DuckDuckGo

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/agentic-healthcare.git
cd agentic-healthcare

pip install -r requirements.txt
streamlit run app.py
```

---

## 🔑 API Key

Enter your Groq API key directly in the UI.

---

## ⚠️ Disclaimer

This project is for educational purposes only and should not be used for medical advice.

---

