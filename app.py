import streamlit as st
import requests
from datetime import datetime
import uuid
import random
import time

# =========================
# CONFIGURAÇÕES
# =========================

AGENT_SIMULATE_URL = "URL_DO_SEU_AGENTE_DE_CLIENTE"
AGENT_ANALYZE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

# =========================
# CONFIG STREAMLIT
# =========================

st.set_page_config(
    page_title="Roleplay - Suporte Goomer",
    page_icon="💙",
    layout="centered"
)

st.title("Roleplay - Suporte Goomer 💙")
st.markdown("Simulação de atendimento via chat")

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "test_finished" not in st.session_state:
    st.session_state.test_finished = False


# =========================
# CLIENTE PERSONA
# =========================

def get_client_persona():
    personas = [
        "impaciente",
        "confuso",
        "irritado",
        "exigente"
    ]
    return random.choice(personas)


# =========================
# RESPOSTA DO CLIENTE
# =========================

def get_client_llm_response(candidate_message):

    unique_context = f"[Conversa #{st.session_state.interaction_count} - {datetime.now().strftime('%H:%M:%S')}] {candidate_message}"

    payload = {
        "mensagem_candidato": unique_context,
        "tipo_cliente": get_client_persona(),
        "cenario": "estorno_duplicado"
    }

    try:

        response = requests.post(
            AGENT_SIMULATE_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "X-Request-ID": str(uuid.uuid4())
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):

            result = (
                data.get("Output")
                or data.get("resposta_cliente")
                or data.get("reply")
                or str(data)
            )

            return result

        return str(data)

    except Exception:

        fallbacks = [
            "Tá, mas como vocês vão resolver isso?",
            "Quanto tempo vai levar?",
            "Mas isso resolve o meu prejuízo?",
            "Vocês conseguem verificar isso agora?"
        ]

        return fallbacks[
            st.session_state.interaction_count % len(fallbacks)
        ]


# =========================
# FORMATAR CONVERSA
# =========================

def format_conversation():

    conversation = ""

    for msg in st.session_state.messages:

        role = msg["role"]
        content = msg["content"]

        if role == "cliente":
            conversation += f"Cliente: {content}\n\n"

        else:
            conversation += f"Analista: {content}\n\n"

    return conversation


# =========================
# ENVIAR PARA AVALIAÇÃO
# =========================

def send_to_analysis(nome, vaga):

    payload = {
        "nome_candidato": nome,
        "conversa_completa": format_conversation(),
        "vaga": vaga
    }

    try:

        requests.post(
            AGENT_ANALYZE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

    except Exception:
        pass


# =========================
# FORMULÁRIO INICIAL
# =========================

if not st.session_state.test_started:

    nome = st.text_input("Seu nome")
    vaga = st.selectbox(
        "Nível da vaga",
        ["Suporte Jr", "Suporte Pleno", "Suporte Sr"]
    )

    if st.button("Iniciar teste"):

        if nome:

            st.session_state.nome = nome
            st.session_state.vaga = vaga
            st.session_state.test_started = True
            st.session_state.start_time = time.time()

            # mensagem inicial do cliente
            first_message = """Oi, bom dia.

Ontem falei com vocês sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?"""

            st.session_state.messages.append(
                {"role": "cliente", "content": first_message}
            )

            st.rerun()

        else:
            st.warning("Por favor informe seu nome")

# =========================
# CHAT
# =========================

elif not st.session_state.test_finished:

    # CRONÔMETRO

    elapsed = int(time.time() - st.session_state.start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60

    st.info(f"Tempo de teste: {minutes:02d}:{seconds:02d}")

    # HISTÓRICO

    for msg in st.session_state.messages:

        if msg["role"] == "cliente":
            st.chat_message("assistant").write(msg["content"])

        else:
            st.chat_message("user").write(msg["content"])

    # INPUT

    user_input = st.chat_input("Digite sua resposta")

    if user_input:

        st.session_state.messages.append(
            {"role": "analista", "content": user_input}
        )

        st.session_state.interaction_count += 1

        client_reply = get_client_llm_response(user_input)

        st.session_state.messages.append(
            {"role": "cliente", "content": client_reply}
        )

        st.rerun()

    # FINALIZAR TESTE

    if st.button("Finalizar teste"):

        send_to_analysis(
            st.session_state.nome,
            st.session_state.vaga
        )

        st.session_state.test_finished = True
        st.rerun()


# =========================
# FINAL
# =========================

else:

    st.success("Teste enviado com sucesso. Obrigado pela participação.")
