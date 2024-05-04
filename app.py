from typing import Generator
import streamlit as st
from groq import Groq
from llama_index.llms.groq import Groq as LlamaGroq
from llama_index.core.llms import ChatMessage

def icon(emoji: str):
    """Mostra um emoji como ícone de página no estilo Notion."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

# Configuração da página
st.set_page_config(page_icon="💬 Prof. Marcelo Claro", layout="wide", page_title="Geomaker Chat Interface")
icon("🌎")  # Exibe o ícone do globo

st.subheader("Geomaker Chat Streamlit App")
st.subheader("Professor Marcelo Claro")

# Configuração da chave API e inicialização dos clientes
api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else "your_api_key_here"
groq_client = Groq(api_key=api_key)
llama_groq = LlamaGroq(model="llama3-70b-8192", api_key=api_key)  # Usando LlamaGroq para RAG

if "messages" not in st.session_state:
    st.session_state.messages = []

models = {
    "llama3-70b-8192": {"name": "LLaMA3-70b-Instruct", "tokens": 3276800, "developer": "Facebook"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-chat", "tokens": 3276800, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 3276800, "developer": "Mistral"},
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 3276800, "developer": "Google"}
}

model_option = st.selectbox("Choose a model:", options=list(models.keys()), format_func=lambda x: models[x]["name"], index=0)
max_tokens_range = models[model_option]["tokens"]
max_tokens = st.slider("Max Tokens:", min_value=512, max_value=max_tokens_range, value=min(32768, max_tokens_range), step=512, help=f"Adjust the maximum number of tokens for the model's response: {max_tokens_range}")

# Adição de uma área de entrada para personalizar o prompt do sistema
system_prompt = st.text_area("Customize the system prompt:", value="Enter a system prompt here...")
if st.button("Confirm System Prompt"):
    st.session_state.messages.append({"role": "system", "content": system_prompt})

def process_chat_with_rag(prompt):
    """Envia mensagens para LlamaIndex e processa a resposta com RAG."""
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=prompt)
    ]
    response = llama_groq.chat(messages)
    return response

if prompt := st.text_input("Insira sua pergunta aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = process_chat_with_rag(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Exibição das mensagens do chat
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
