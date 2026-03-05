import streamlit as st
import requests
from datetime import datetime

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="Goomer - Roleplay Suporte",
    page_icon="💙",
    layout="wide"
)

# URL da API do seu agente SmythOS (atualize com a sua)
AGENT_API_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

# ===== ESTILOS CSS =====
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1E88E5;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .message-client {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    .message-candidate {
        background-color: #1E88E5;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .timer {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        color: #f57c00;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.1rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== INICIALIZAÇÃO DO ESTADO =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "test_start_time" not in st.session_state:
    st.session_state.test_start_time = None
if "test_completed" not in st.session_state:
    st.session_state.test_completed = False
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "nome_candidato" not in st.session_state:
    st.session_state.nome_candidato = ""
if "vaga" not in st.session_state:
    st.session_state.vaga = "Suporte Jr"

# ===== FUNÇÕES AUXILIARES =====
def format_timer():
    """Formata o cronômetro do teste"""
    if st.session_state.test_start_time:
        elapsed = datetime.now() - st.session_state.test_start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        return f"{minutes:02d}:{seconds:02d}"
    return "00:00"

def add_client_message(message):
    """Adiciona mensagem do cliente simulado"""
    st.session_state.chat_history.append({
        "sender": "client",
        "message": message
    })

def add_candidate_message(message):
    """Adiciona mensagem do candidato"""
    st.session_state.chat_history.append({
        "sender": "candidate",
        "message": message
    })

def format_conversation_for_api():
    """Formata a conversa para envio à API"""
    conversation = ""
    for msg in st.session_state.chat_history:
        sender = "Cliente" if msg["sender"] == "client" else "Candidato"
        conversation += f"{sender}: {msg['message']}\n"
    return conversation.strip()

def simulate_client_response():
    """Retorna uma resposta simulada do cliente baseada no número de mensagens"""
    responses = [
        "Olá! Preciso de ajuda com meu pedido que está atrasado há mais de 1 hora.",
        "Fiz um pedido às 12h e ainda não chegou. Estou com muita fome!",
        "O aplicativo está mostrando que o pedido foi entregue
Vou criar uma aplicação Streamlit completa para seu sistema de simulação de atendimento da Goomer. Aqui está o código estruturado:

## 📁 **Arquivo `app.py` - Aplicação Completa**

```python
import streamlit as st
import requests
from datetime import datetime
import time

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="Goomer - Roleplay Suporte",
    page_icon="💙",
    layout="wide"
)

# URL da API do seu agente SmythOS
AGENT_API_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

# ===== ESTILOS CSS =====
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1E88E5;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .message-client {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .message-candidate {
        background-color: #1E88E5;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .timer {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        color: #f57c00;
        margin-bottom: 1rem;
        border: 1px solid #ffcc02;
    }
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.3rem;
        margin-top: 2rem;
        border: 2px solid #4caf50;
    }
    .chat-input-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .initial-message {
        background-color: #fff9c4;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #ff9800;
    }
    .clear-both {
        clear: both;
        height: 0;
    }
</style>
""", unsafe_allow_html=True)

# ===== INICIALIZAÇÃO DO ESTADO =====
def init_session_state():
    """Inicializa todas as variáveis de estado da sessão"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'test_start_time' not in st.session_state:
        st.session_state.test_start_time = None
    if 'test_completed' not in st.session_state:
        st.session_state.test_completed = False
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'initial_message_sent' not in st.session_state:
        st.session_state.initial_message_sent = False

# Chama a função de inicialização
init_session_state()

# ===== FUNÇÕES AUXILIARES =====
def format_timer():
    """Formata o cronômetro do teste em MM:SS"""
    if st.session_state.test_start_time:
        elapsed = datetime.now() - st.session_state.test_start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        return f"{minutes:02d}:{seconds:02d}"
    return "00:00"

def add_client_message(message):
    """Adiciona mensagem do cliente ao histórico"""
    st.session_state.chat_history.append({
        "sender": "client",
        "message": message,
        "timestamp": datetime.now()
    })

def add_candidate_message(message):
    """Adiciona mensagem do candidato ao histórico"""
    st.session_state.chat_history.append({
        "sender": "candidate",
        "message": message,
        "timestamp": datetime.now()
    })

def format_conversation_for_api():
    """Formata toda a conversa em texto para envio à API"""
    conversation = ""
    for msg in st.session_state.chat_history:
        sender = "Cliente" if msg["sender"] == "client" else "Candidato"
        conversation += f"{sender}: {msg['message']}\n"
    return conversation.strip()

def send_to_analysis_api(nome_candidato, conversa_completa, vaga):
    """Envia os dados da conversa para análise via API SmythOS"""
    payload = {
        "nome_candidato": nome_candidato,
        "conversa_completa": conversa_completa,
        "vaga": vaga
    }
    
    try:
        response = requests.post(
            AGENT_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

def get_initial_client_message():
    """Retorna a mensagem inicial específica do cliente"""
    return """Oi, bom dia.

Ontem falei com vocês sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?"""

def simulate_additional_client_responses():
    """Simula respostas adicionais do cliente baseadas no contexto"""
    responses = [
        "Entendi sua explicação, mas preciso de uma solução rápida.",
        "Quanto tempo vai demorar para resolver isso?",
        "Já tive outros problemas com vocês antes.",
        "Espero que isso não aconteça novamente.",
        "Obrigado pela ajuda, mas quero acompanhar o processo.",
        "Quando posso esperar uma resposta definitiva?",
        "Vou aguardar o contato de vocês então."
    ]
    
    # Conta apenas mensagens do cliente (excluindo a inicial)
    client_messages = len([m for m in st.session_state.chat_history 
                          if m["sender"] == "client"]) - 1
    
    if client_messages < len(responses):
        return responses[client_messages]
    else:
        return "Entendo. Vou aguardar seu retorno."

def reset_conversation():
    """Reseta toda a conversa para começar novamente"""
    st.session_state.chat_history = []
    st.session_state.conversation_started = False
    st.session_state.test_start_time = None
    st.session_state.initial_message_sent = False

# ===== INTERFACE PRINCIPAL =====
def main():
    # Cabeçalho da aplicação
    st.markdown('<h1 class="main-header">Roleplay - Suporte Goomer 💙</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Simulação de atendimento via chat</p>', unsafe_allow_html=True)
    
    # Se o teste foi completado, mostrar apenas mensagem de sucesso
    if st.session_state.test_completed:
        st.markdown("""
        <div class="success-message">
            ✅ Teste enviado com sucesso!<br><br>
            Obrigado pela sua participação.
        </div>
        """, unsafe_allow_html=True)
        
        # Botão para fazer novo teste
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄 Fazer Novo Teste", type="primary"):
                # Reset completo do estado
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        return
    
    # Formulário de informações do candidato
    if not st.session_state.conversation_started:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("### 📋 Informações do Candidato")
                
                nome_candidato = st.text_input(
                    "Nome completo:",
                    placeholder="Digite seu nome completo",
                    help="Informe seu nome completo para identificação"
                )
                
                vaga = st.selectbox(
                    "Nível da vaga:",
                    ["Suporte Jr", "Suporte Pleno", "Suporte Sr"],
                    help="Selecione o nível da vaga para a qual está se candidatando"
                )
                
                # Instrução sobre o teste
                st.markdown("""
                <div class="initial-message">
                    <strong>📝 Instruções do Teste:</strong><br>
                    • Você receberá uma mensagem de um cliente<br>
                    • Responda como um analista de suporte<br>
                    • Seja educado, empático e resolutivo<br>
                    • O teste será cronometrado<br>
                    • Clique em "Finalizar Teste" quando terminar
                </div>
                """, unsafe_allow_html=True)
                
                # Botão para iniciar
                if st.button("🚀 Iniciar Simulação", 
                           type="primary", 
                           disabled=not nome_candidato,
                           use_container_width=True):
                    # Inicia o teste
                    st.session_state.conversation_started = True
                    st.session_state.test_start_time = datetime.now()
                    st.session_state.nome_candidato = nome_candidato
                    st.session_state.vaga = vaga
                    
                    # Adiciona a mensagem inicial do cliente
                    add_client_message(get_initial_client_message())
                    st.session_state.initial_message_sent = True
                    
                    st.rerun()
    
    # Interface de chat (aparece após iniciar)
    else:
        # Timer do teste
        timer_placeholder = st.empty()
        with timer_placeholder:
            st.markdown(f'<div class="timer">⏱️ Tempo de teste: {format_timer()}</div>', 
                       unsafe_allow_html=True)
        
        # Título da seção de chat
        st.markdown("### 💬 Chat de Atendimento")
        
        # Container do histórico de mensagens
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Renderiza todas as mensagens do histórico
            for i, msg in enumerate(st.session_state.chat_history):
                if msg["sender"] == "client":
                    st.markdown(f"""
                    <div class="message-client">
                        <strong>Cliente:</strong><br>{msg["message"].replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message-candidate">
                        <strong>Você:</strong><br>{msg["message"].replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Garante que as mensagens flutuem corretamente
            st.markdown('<div class="clear-both"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Campo de entrada para nova mensagem
        st.markdown("---")
        
        with st.container():
            st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                nova_mensagem = st.text_area(
                    "Digite sua resposta:",
                    placeholder="Digite aqui sua resposta ao cliente...",
                    height=100,
                    key="input_mensagem"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
                enviar_clicked = st.button("📤 Enviar", 
                                         type="primary", 
                                         use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Processa o envio de nova mensagem
        if enviar_clicked and nova_mensagem and nova_mensagem.strip():
            # Adiciona mensagem do candidato
            add_candidate_message(nova_mensagem.strip())
            
            # Simula resposta do cliente (limitada a algumas interações)
            if len(st.session_state.chat_history) < 10:  # Máximo de 10 mensagens totais
                time.sleep(1)  # Simula tempo de resposta
                client_response = simulate_additional_client_responses()
                add_client_message(client_response)
            
            st.rerun()
        
        # Botões de ação
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🗑️ Limpar Chat", use_container_width=True):
                reset_conversation()
                st.rerun()
        
        with col2:
            # Mostra contador de mensagens
            total_messages = len(st.session_state.chat_history)
            candidate_messages = len([m for m in st.session_state.chat_history 
                                    if m["sender"] == "candidate"])
            st.write(f"📊 Mensagens: {candidate_messages} suas, {total_messages - candidate_messages} do cliente")
        
        with col3:
            if st.button("✅ Finalizar Teste", 
                        type="primary", 
                        use_container_width=True):
                
                # Validação mínima
                candidate_messages = len([m for m in st.session_state.chat_history 
                                        if m["sender"] == "candidate"])
                
                if candidate_messages >= 2:  # Mínimo de 2 respostas do candidato
                    # Prepara dados para envio
                    conversa_formatada = format_conversation_for_api()
                    
                    # Envia para análise
                    with st.spinner("🔄 Enviando teste para análise..."):
                        result = send_to_analysis_api(
                            st.session_state.nome_candidato, 
                            conversa_formatada, 
                            st.session_state.vaga
                        )
                    
                    if result["success"]:
                        st.session_state.test_completed = True
                        st.rerun()
                    else:
                        st.error(f"❌ Erro ao enviar teste: {result['error']}")
                        st.write("Tente novamente em alguns instantes.")
                else:
                    st.warning("⚠️ Responda pelo menos 2 mensagens do cliente antes de finalizar o teste.")

        # Auto-atualiza o timer a cada segundo (opcional)
        if st.session_state.test_start_time:
            time.sleep(0.1)  # Pequena pausa para performance

# ===== EXECUÇÃO DA APLICAÇÃO =====
if __name__ == "__main__":
    main()
