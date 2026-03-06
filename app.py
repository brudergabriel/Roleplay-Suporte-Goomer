import streamlit as st
import requests
import random
import time

# =============================
# CONFIGURAÇÕES
# =============================

CLIENT_AGENT_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/simular_cliente"
ANALYSIS_API_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

# =============================
# CONFIG STREAMLIT
# =============================

st.set_page_config(
    page_title="Roleplay - Suporte Goomer",
    page_icon="💙", 
    layout="centered"
)

st.title("Roleplay - Suporte Goomer 💙")
st.caption("Simulação de atendimento via chat")

# =============================
# SESSION STATE
# =============================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0

if "processing" not in st.session_state:
    st.session_state.processing = False

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "test_finished" not in st.session_state:
    st.session_state.test_finished = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "nome" not in st.session_state:
    st.session_state.nome = ""

if "vaga" not in st.session_state:
    st.session_state.vaga = ""

# =============================
# PERSONA CLIENTE
# =============================

def get_client_persona():
    personas = [
        "impaciente",
        "confuso",
        "irritado", 
        "exigente"
    ]
    return random.choice(personas)

# =============================
# CLIENTE SIMULADO (CORRIGIDO)
# =============================

def get_client_response(message):
    # ✅ CORRIGIDO: Monta histórico completo SEM duplicar a mensagem atual
    conversation = ""
    for msg in st.session_state.messages:
        role = "Cliente" if msg["role"] == "cliente" else "Analista"
        conversation += f"{role}: {msg['content']}\n"

    payload = {
        "historico_conversa": conversation,
        "tipo_cliente": get_client_persona(),
        "cenario": "estorno_duplicado"
    }

    # 🔧 DEBUG: Mostrar histórico enviado
    st.write("**DEBUG - Histórico enviado para a API:**")
    st.write(conversation)
    st.write("---")

    try:
        response = requests.post(CLIENT_AGENT_URL, json=payload, timeout=20)
        data = response.json()
        
        if isinstance(data, dict):
            return data.get("Output", "Pode explicar melhor?")
        
        return str(data)
        
    except Exception as e:
        fallbacks = [
            "Tá, mas como vocês vão resolver isso?",
            "Quanto tempo vai levar?",
            "Mas isso resolve o prejuízo?", 
            "Vocês conseguem verificar isso agora?"
        ]
        return random.choice(fallbacks)

# =============================
# FORMATAR CONVERSA
# =============================

def format_conversation():
    conversation = ""
    for msg in st.session_state.messages:
        if msg["role"] == "cliente":
            conversation += f"Cliente: {msg['content']}\n\n"
        else:
            conversation += f"Analista: {msg['content']}\n\n"
    return conversation

# =============================
# ENVIAR PARA IA
# =============================

def send_to_analysis():
    payload = {
        "nome_candidato": st.session_state.nome,
        "conversa_completa": format_conversation(),
        "vaga": st.session_state.vaga
    }
    try:
        requests.post(ANALYSIS_API_URL, json=payload, timeout=60)
    except:
        pass

# =============================
# TELA INICIAL
# =============================

if not st.session_state.test_started:
    nome = st.text_input("Seu nome")
    vaga = st.selectbox("Nível da vaga", ["Suporte Jr", "Suporte Pleno", "Suporte Sr"])

    if st.button("Iniciar teste"):
        if nome:
            st.session_state.nome = nome
            st.session_state.vaga = vaga
            st.session_state.test_started = True
            st.session_state.start_time = time.time()

            first_message = """Oi, bom dia.

Ontem falei com vocês sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?"""

            st.session_state.messages.append({
                "role": "cliente",
                "content": first_message
            })
            st.rerun()
        else:
            st.warning("Informe seu nome para iniciar.")

# =============================
# CHAT
# =============================

elif not st.session_state.test_finished:
    elapsed = int(time.time() - st.session_state.start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    st.info(f"Tempo de teste: {minutes:02d}:{seconds:02d}")
    st.divider()

    # HISTÓRICO
    for msg in st.session_state.messages:
        if msg["role"] == "cliente":
            with st.chat_message("assistant"):
                st.write(msg["content"])
        else:
            with st.chat_message("user"):
                st.write(msg["content"])

    # INPUT CHAT
    user_input = st.chat_input("Digite sua resposta...")
    
    if user_input and not st.session_state.processing:
        if user_input.strip() == "":
            st.stop()

        st.session_state.processing = True
        
        # ✅ ADICIONA mensagem do analista ANTES de chamar a API
        st.session_state.messages.append({
            "role": "analista",
            "content": user_input
        })
        st.session_state.interaction_count += 1

        try:
            with st.spinner("Cliente digitando..."):
                reply = get_client_response(user_input)
        except:
            reply = "Desculpe, tive um problema para responder."

        if not reply:
            reply = "Pode explicar melhor?"

        # ✅ ADICIONA resposta do cliente
        st.session_state.messages.append({
            "role": "cliente", 
            "content": reply
        })

        st.session_state.processing = False
        st.rerun()

    # FINALIZAR TESTE
    if st.button("Finalizar teste"):
        send_to_analysis()
        st.session_state.test_finished = True
        st.rerun()

# =============================
# FINAL
# =============================

else:
    st.success("Teste enviado com sucesso. Obrigado pela participação.")
