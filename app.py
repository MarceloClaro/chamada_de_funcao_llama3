import streamlit as st
from groq import Groq  # Certifique-se de que 'groq' seja o módulo correto, pois não é padrão.
from llama_index.llms.groq import Groq as LlamaGroq
from llama_index.core.llms import ChatMessage

def icon(emoji: str):
    """Mostra um emoji como ícone de página no estilo Notion."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

# Configuração da página
st.set_page_config(page_icon="💬", layout="wide", page_title="Interface de Chat Geomaker")
icon("")  # Exibe um ícone personalizado

st.subheader("Aplicativo de Chat Geomaker")
st.write("Professor Marcelo Claro")

# Configuração da API Key
api_key = st.secrets.get("GROQ_API_KEY", "your_api_key_here")
groq_client = Groq(api_key=api_key)
llama_groq = LlamaGroq(model="llama3-70b-8192", api_key=api_key)

# Inicialização do estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configuração dos modelos disponíveis
models = {
    "llama3-70b-8192": {"name": "LLaMA3-70b-Instruct", "tokens": 32768, "developer": "Facebook"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-chat", "tokens": 32768, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 32768, "developer": "Google"}
}

# Seletor de modelos com descrição melhorada
model_option = st.selectbox("Escolha um modelo:", options=list(models.keys()), format_func=lambda x: models[x]["name"])
max_tokens_range = models[model_option]["tokens"]
max_tokens = st.slider("Máximo de Tokens:", min_value=512, max_value=max_tokens_range, value=min(32768, max_tokens_range), step=512)

# Configurações adicionais na barra lateral
with st.sidebar:
    st.image("Untitled.png", width=100)
    st.write("Configurações")
    # Campo para definir o prompt do sistema
    system_prompt = st.text_area("UltimatePromptEngineerAI, apelidado de 至尊AI提示工程师, é um sistema de inteligência artificial de elite, projetado especificamente para otimizar e integrar tecnologias de vanguarda com eficiência. Este sistema se destaca pela sua capacidade de fornecer respostas altamente precisas e contextualizadas, dotado de funcionalidades avançadas como a geração de identificadores únicos (gen_id) para cada interação e o registro detalhado do estado exato do modelo de IA no momento da resposta (seend). Equipado com tecnologias revolucionárias, incluindo inteligência contextual RAG, otimização automática e aprendizado contínuo, o sistema adapta-se dinamicamente para melhorar continuamente suas interações com os usuários. Ideal para uma ampla gama de aplicações, desde análise de grandes volumes de dados até criação de conteúdo interativo e soluções personalizadas de IA para setores específicos, o UltimatePromptEngineerAI garante interações eficientes e seguras. Ele implementa rigorosas medidas de segurança, como criptografia e monitoramento proativo, para proteger dados e interações. Além disso, oferece orientação especializada para integrar rapidamente novas tecnologias e se aprimorar com base em feedback em tempo real e análises de explicabilidade aprimorada da IA (XAI), promovendo uma personalização profunda e adaptação às necessidades dos usuários. Suportando múltiplos idiomas, o sistema favorece uma abordagem inclusiva e global, com um forte enfoque no desenvolvimento continuado em processamento de linguagem natural e visão computacional. Comprometido com os mais altos padrões éticos, o sistema trabalha ativamente para eliminar vieses e garantir interações equitativas e precisas, estabelecendo um novo padrão em inteligência artificial adaptativa e responsiva.")
    if st.button("Confirmar Prompt"):
        st.session_state.system_prompt = system_prompt
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.experimental_rerun()

# Processamento de chat com RAG
def process_chat_with_rag(prompt):
    messages = [
        ChatMessage(role="system", content=st.session_state.system_prompt),
        ChatMessage(role="user", content=prompt)
    ]
    response = llama_groq.chat(messages)
    return response

# Área para inserção de perguntas
if prompt := st.text_area("Insira sua pergunta aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = process_chat_with_rag(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Exibição das mensagens
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
