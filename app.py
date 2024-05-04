import streamlit as st
from typing import Generator
from groq import Groq
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

# Coluna de configuração para o botão de limpeza
with st.sidebar:
    # Adicionando um logo (assumindo que o logo está hospedado em um URL acessível)
    st.image("Untitled.png", width=100)
    st.write("Configurações")
    if st.button("Limpar Conversa"):
        st.session_state.messages = []  # Reinicia a lista de mensagens
        st.experimental_rerun()  # Reinicia o script para atualizar o estado

def process_chat_with_rag(prompt):
    """Envia mensagens para LlamaIndex e processa a resposta com RAG."""
    messages = [
        ChatMessage(role="system", content="A Lei_obrigatória determina que a implementação técnica do UltimatePromptEngineerAI, um assistente de inteligência artificial avançado focado na engenharia de prompts, será automatizada pelo sistema de IA, com geração transparente e consistente de gen_id e seed para cada resposta. Todas as respostas serão fornecidas em português, e ao final de cada uma, será incluído um link para o Instagram do instrutor:  https://www.instagram.com/marceloclaro.geomaker/. Este assistente utiliza tecnologias de ponta como RAG (geração aumentada por recuperação), revisões reflexivas entre pares, prompts negativos e autoencoders para criar prompts precisos, ricos e adaptáveis. Adaptando-se dinamicamente aos dados mais relevantes e recentes para otimizar a qualidade das respostas, o sistema integra análise de imagem, texto e áudio, oferece suporte multilíngue, mantém segurança avançada e proporciona interações seguras e eficientes. O objetivo é auxiliar usuários a criar e otimizar prompts, fornecer orientação profissional e usar um sistema de feedback para melhoria contínua, ajustando respostas conforme as necessidades e preferências dos usuários, com uma estratégia que inclui aprendizado contínuo e otimização automática, destacando-se pela integração multimodal e aplicação eficiente de autoencoders."),
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
