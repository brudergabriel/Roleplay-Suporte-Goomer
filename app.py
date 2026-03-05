import streamlit as st
import requests
from datetime import datetime

# =================================
# CONFIGURAÇÃO
# =================================

st.set_page_config(
    page_title="Goomer - Roleplay Suporte",
    page_icon="💙",
    layout="wide"
)

AGENT_SIMULATE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/simular_cliente"
AGENT_ANALYZE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

# =================================
# SESSION STATE
# =================================

def init_session():
    defaults = {
        "chat_history": [],
        "conversation_started": False,
        "processing_message": False,
        "test_completed": False,
        "test_start_time": None,
        "last_user_message": None,
        "interaction_count": 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# =================================
# CHAT FUNCTIONS
# =================================

def add_client_message(msg):
    st.session_state.chat_history.append({
        "sender": "client",
        "message": msg
    })

def add_candidate_message(msg):
    st.session_state.chat_history.append({
        "sender": "candidate", 
        "message": msg
    })
    st.session_state.interaction_count += 1

def format_conversation():
    text = ""
    for msg in st.session_state.chat_history:
        role = "Cliente" if msg["sender"] == "client" else "Analista"
        text += f"{role}: {msg['message']}\n"
    return text

def get_conversation_context():
    """Retorna últimas 3 mensagens como contexto"""
    recent = st.session_state.chat_history[-6:] if len(st.session_state.chat_history) > 6 else st.session_state.chat_history
    context = ""
    for msg in recent:
        role = "Cliente" if msg["sender"] == "client" else "Analista"
        context += f"{role}: {msg['message']}\n"
    return context

# =================================
# TIMER
# =================================

def format_timer():
    if not st.session_state.test_start_time:
        return "00:00"
    
    delta = datetime.now() - st.session_state.test_start_time
    minutes = int(delta.total_seconds() // 60)
    seconds = int(delta.total_seconds() % 60)
    return f"{minutes:02d}:{seconds:02d}"

# =================================
# INITIAL MESSAGE
# =================================

def get_initial_message():
    return """Oi, bom dia.

Ontem falei com vocês sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?"""

# =================================
# CLIENT LLM
# =================================

def get_client_persona():
    """Define persona baseada no número de interações"""
    if st.session_state.interaction_count <= 1:
        return "irritado"
    elif st.session_state.interaction_count <= 3:
        return "impaciente"
    else:
        return "exigente"

def get_client_llm_response(candidate_message):
    # Payload correto para seu agente
    payload = {
        "mensagem_candidato": candidate_message,
        "tipo_cliente": get_client_persona(),
        "cenario": "estorno_duplicado"
    }
    
    # Debug: mostrar o que está sendo enviado
    print(f"Enviando para API: {payload}")
    
    try:
        response = requests.post(
            AGENT_SIMULATE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Debug: mostrar o que foi recebido
        print(f"Resposta da API: {data}")
        
        # Tratamento da resposta baseado na estrutura do seu agente
        if isinstance(data, dict):
            # Tenta diferentes chaves possíveis
            client_response = (
                data.get("Output") or          # Se usar APIOutput
                data.get("resposta_cliente") or 
                data.get("output") or
                data.get("reply") or
                data.get("response")
            )
            
            if client_response:
                return str(client_response)
        
        # Fallback se não conseguir extrair
        return "Entendi... mas ainda não ficou claro pra mim."
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")
        return "Desculpe, tive um problema técnico agora. Pode repetir?"
    except Exception as e:
        print(f"Erro geral: {e}")
        return "Certo, mas isso resolve o meu prejuízo?"

# =================================
# PROCESS MESSAGE
# =================================

def process_message(message):
    if st.session_state.processing_message:
        return
    
    st.session_state.processing_message = True
    
    add_candidate_message(message)
    
    # Limite de 8 respostas do candidato
    if st.session_state.interaction_count < 8:
        with st.spinner("Cliente digitando..."):
            client_reply = get_client_llm_response(message)
            add_client_message(client_reply)
    
    st.session_state.processing_message = False

# =================================
# ANALYSIS API
# =================================

def send_analysis():
    payload = {
        "nome_candidato": st.session_state.nome,
        "vaga": st.session_state.vaga,
        "conversa_completa": format_conversation()
    }
    
    try:
        r = requests.post(
            AGENT_ANALYZE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Erro na análise: {e}")
        return False

# =================================
# UI
# =================================

def main():
    st.title("💬 Roleplay - Suporte Goomer")
    
    # Tela de configuração
    if not st.session_state.conversation_started:
        nome = st.text_input("Nome do candidato")
        vaga = st.selectbox(
            "Nível da vaga",
            ["Suporte Jr", "Suporte Pleno", "Suporte Sr"]
        )
        
        if st.button("Iniciar Simulação", disabled=not nome):
            st.session_state.nome = nome
            st.session_state.vaga = vaga
            st.session_state.conversation_started = True
            st.session_state.test_start_time = datetime.now()
            
            add_client_message(get_initial_message())
            st.rerun()
        
        return
    
    # Interface de chat
    st.write(f"⏱ Tempo: {format_timer()}")
    st.write(f"🎭 Persona atual: {get_client_persona()}")
    st.write(f"📊 Interações: {st.session_state.interaction_count}")
    
    st.divider()
    
    # Histórico de mensagens
    for msg in st.session_state.chat_history:
        if msg["sender"] == "client":
            with st.chat_message("assistant"):
                st.markdown(msg["message"])
        else:
            with st.chat_message("user"):
                st.markdown(msg["message"])
    
    # Input de nova mensagem
    prompt = st.chat_input("Digite sua resposta")
    
    if (prompt and 
        prompt.strip() and 
        prompt != st.session_state.last_user_message and
        not st.session_state.processing_message):
        
        process_message(prompt)
        st.session_state.last_user_message = prompt
        st.rerun()
    
    st.divider()
    
    # Botão finalizar
    if st.button("Finalizar Teste"):
        with st.spinner("Analisando atendimento..."):
            success = send_analysis()
        
        if success:
            st.success("Teste enviado com sucesso!")
            st.session_state.test_completed = True
        else:
            st.error("Erro ao enviar teste.")

# =================================
if __name__ == "__main__":
    main()
