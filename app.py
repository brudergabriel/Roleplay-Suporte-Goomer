import streamlit as st
import requests
from datetime import datetime

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="Goomer - Roleplay Suporte",
    page_icon="💙",
    layout="wide"
)

# URLs da API do seu agente SmythOS
AGENT_SIMULATE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/simular_cliente"
AGENT_ANALYZE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

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
    .typing-indicator {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
        font-style: italic;
        color: #666;
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
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0
    if 'processing_message' not in st.session_state:
        st.session_state.processing_message = False
    if 'client_persona' not in st.session_state:
        st.session_state.client_persona = "irritado"  # Cliente inicialmente irritado

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
        "id": st.session_state.message_counter
    })
    st.session_state.message_counter += 1

def add_candidate_message(message):
    """Adiciona mensagem do candidato ao histórico"""
    st.session_state.chat_history.append({
        "sender": "candidate",
        "message": message,
        "id": st.session_state.message_counter
    })
    st.session_state.message_counter += 1

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
            AGENT_ANALYZE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

def get_initial_client_message():
    """Retorna a mensagem inicial específica do cliente sobre estorno duplicado"""
    return """Oi, bom dia.

Ontem falei com vocês sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?"""

def get_client_llm_response(candidate_message):
    """Chama a LLM do SmythOS para simular resposta do cliente"""
    # Define cenário específico do estorno duplicado
    cenario = "estorno_duplicado"
    
    # Ajusta persona do cliente baseado no progresso da conversa
    candidate_msg_count = len([m for m in st.session_state.chat_history if m["sender"] == "candidate"])
    
    if candidate_msg_count <= 1:
        persona = "irritado"  # Início: cliente irritado
    elif candidate_msg_count <= 3:
        persona = "impaciente"  # Meio: impaciente mas ouvindo
    else:
        persona = "exigente"  # Final: mais exigente, quer garantias
    
    payload = {
        "mensagem_candidato": candidate_message,
        "tipo_cliente": persona,
        "cenario": cenario
    }
    
    try:
        response = requests.post(
            AGENT_SIMULATE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        
        # Extrai resposta do cliente da resposta da API
        data = response.json()
        
        # A resposta pode vir em diferentes formatos dependendo da sua configuração
        if isinstance(data, dict):
            # Tenta diferentes chaves possíveis
            client_response = (data.get("resposta_cliente") or 
                             data.get("output") or 
                             data.get("reply") or 
                             data.get("response") or
                             str(data))
        else:
            client_response = str(data)
            
        return client_response
        
    except requests.exceptions.RequestException as e:
        # Fallback para resposta de erro
        return f"Desculpe, tive um problema técnico. Você pode repetir? (Erro: {str(e)})"

def process_new_message(message):
    """Processa uma nova mensagem do candidato"""
    if st.session_state.processing_message:
        return
    
    st.session_state.processing_message = True
    
    # Adiciona mensagem do candidato
    add_candidate_message(message.strip())
    
    # Chama a LLM para gerar resposta do cliente (limitado a 8 trocas)
    if len(st.session_state.chat_history) < 16:  # 8 do candidato + 8 do cliente
        try:
            # Mostra indicador de digitação temporariamente
            with st.spinner("Cliente está digitando..."):
                client_response = get_client_llm_response(message.strip())
                add_client_message(client_response)
        except Exception as e:
            # Em caso de erro, usa resposta padrão
            add_client_message("Hmm, parece que tive um problema. Pode explicar novamente?")
    
    st.session_state.processing_message = False

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
                
                # Contexto do cenário
                st.markdown("""
                <div class="initial-message">
                    <strong>📝 Cenário do Teste:</strong><br>
                    • Cliente solicitou estorno de pedido cobrado em duplicidade<br>
                    • Estorno foi processado duas vezes por erro<br>
                    • Cliente está preocupado com prejuízo financeiro<br>
                    • <strong>Seja empático, resolutivo e proativo!</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Instruções
                st.markdown("""
                <div class="initial-message">
                    <strong>⚡ Como funciona:</strong><br>
                    • IA simula cliente real com base nas suas respostas<br>
                    • Conversas dinâmicas e contextualizadas<br>
                    • Teste cronometrado e gravado<br>
                    • Análise automática do atendimento
                </div>
                """, unsafe_allow_html=True)
                
                # Botão para iniciar
                if st.button("🚀 Iniciar Simulação com IA", 
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
                    
                    st.rerun()
    
    # Interface de chat (aparece após iniciar)
    else:
        # Timer do teste
        st.markdown(f'<div class="timer">⏱️ Tempo de teste: {format_timer()}</div>', 
                   unsafe_allow_html=True)
        
        # Título da seção de chat
        st.markdown("### 💬 Chat de Atendimento")
        st.markdown("*🤖 Cliente simulado por IA - Cenário: Estorno Duplicado*")
        
        # Container do histórico de mensagens
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Renderiza todas as mensagens do histórico
            for msg in st.session_state.chat_history:
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
        
        # Usar formulário para controlar o envio
        with st.form("message_form", clear_on_submit=True):
            nova_mensagem = st.text_area(
                "Digite sua resposta:",
                placeholder="Como você resolveria essa situação de estorno duplicado?",
                height=100,
                disabled=st.session_state.processing_message
            )
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                enviar_clicked = st.form_submit_button(
                    "📤 Enviar", 
                    type="primary", 
                    use_container_width=True,
                    disabled=st.session_state.processing_message
                )
        
        # Processa o envio de nova mensagem
        if enviar_clicked and nova_mensagem and nova_mensagem.strip():
            process_new_message(nova_mensagem)
            st.rerun()
        
        # Botões de ação
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🗑️ Reiniciar Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.message_counter = 0
                st.session_state.client_persona = "irritado"
                add_client_message(get_initial_client_message())
                st.rerun()
        
        with col2:
            # Mostra contador de mensagens e persona atual
            total_messages = len(st.session_state.chat_history)
            candidate_messages = len([m for m in st.session_state.chat_history 
                                    if m["sender"] == "candidate"])
            
            # Determina persona atual
            if candidate_messages <= 1:
                persona = "😠 Irritado"
            elif candidate_messages <= 3:
                persona = "⏳ Impaciente"
            else:
                persona = "🎯 Exigente"
                
            st.write(f"📊 Suas: {candidate_messages} | Cliente: {persona}")
        
        with col3:
            if st.button("✅ Finalizar Teste", 
                        type="primary", 
                        use_container_width=True,
                        disabled=st.session_state.processing_message):
                
                # Validação mínima
                candidate_messages = len([m for m in st.session_state.chat_history 
                                        if m["sender"] == "candidate"])
                
                if candidate_messages >= 3:  # Mínimo de 3 respostas para cenário complexo
                    # Prepara dados para envio
                    conversa_formatada = format_conversation_for_api()
                    
                    # Envia para análise
                    with st.spinner("🔄 Enviando teste para análise inteligente..."):
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
                    st.warning("⚠️ Para um cenário complexo como este, responda pelo menos 3 mensagens do cliente.")

# ===== EXECUÇÃO DA APLICAÇÃO =====
if __name__ == "__main__":
    main()
