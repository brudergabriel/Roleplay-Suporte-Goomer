import streamlit as st
import requests
from datetime import datetime

# ===== CONFIGURAÇÃO =====
st.set_page_config(
    page_title="Goomer - Roleplay Suporte",
    page_icon="💙",
    layout="wide"
)

AGENT_SIMULATE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/simular_cliente"
AGENT_ANALYZE_URL = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"


# ===== ESTADO =====
def init_session_state():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

    if "test_completed" not in st.session_state:
        st.session_state.test_completed = False

    if "processing_message" not in st.session_state:
        st.session_state.processing_message = False

    if "test_start_time" not in st.session_state:
        st.session_state.test_start_time = None

    if "last_user_message" not in st.session_state:
        st.session_state.last_user_message = None


init_session_state()


# ===== FUNÇÕES =====

def add_client_message(message):
    st.session_state.chat_history.append({
        "sender": "client",
        "message": message
    })


def add_candidate_message(message):
    st.session_state.chat_history.append({
        "sender": "candidate",
        "message": message
    })


def format_conversation():

    conversation = ""

    for msg in st.session_state.chat_history:

        sender = "Cliente" if msg["sender"] == "client" else "Analista"

        conversation += f"{sender}: {msg['message']}\n"

    return conversation


def get_initial_message():

    return """Oi, bom dia.

Ontem falei com vocês sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?"""


# ===== LLM CLIENTE =====

def get_client_llm_response(candidate_message):

    payload = {
        "mensagem_candidato": candidate_message,
        "historico_conversa": format_conversation(),
        "cenario": "estorno_duplicado"
    }

    try:

        response = requests.post(
            AGENT_SIMULATE_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):

            return (
                data.get("resposta_cliente")
                or data.get("output")
                or data.get("reply")
                or data.get("response")
                or str(data)
            )

        return str(data)

    except Exception as e:

        return "Desculpe, tive um problema técnico. Pode repetir?"


# ===== PROCESSAMENTO =====

def process_new_message(message):

    if st.session_state.processing_message:
        return

    st.session_state.processing_message = True

    add_candidate_message(message)

    candidate_messages = len([
        m for m in st.session_state.chat_history
        if m["sender"] == "candidate"
    ])

    if candidate_messages < 8:

        with st.spinner("Cliente digitando..."):

            response = get_client_llm_response(message)

            add_client_message(response)

    st.session_state.processing_message = False


# ===== TIMER =====

def format_timer():

    if not st.session_state.test_start_time:
        return "00:00"

    elapsed = datetime.now() - st.session_state.test_start_time

    minutes = int(elapsed.total_seconds() // 60)
    seconds = int(elapsed.total_seconds() % 60)

    return f"{minutes:02d}:{seconds:02d}"


# ===== UI =====

def main():

    st.title("💬 Roleplay - Suporte Goomer")

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


    st.write(f"⏱️ Tempo: {format_timer()}")

    st.divider()

    for msg in st.session_state.chat_history:

        if msg["sender"] == "client":

            with st.chat_message("assistant"):
                st.markdown(msg["message"])

        else:

            with st.chat_message("user"):
                st.markdown(msg["message"])


    prompt = st.chat_input("Digite sua resposta...")

    if (
        prompt
        and prompt.strip()
        and prompt != st.session_state.last_user_message
    ):

        process_new_message(prompt)

        st.session_state.last_user_message = prompt

        st.rerun()


    st.divider()

    if st.button("Finalizar Teste"):

        conversation = format_conversation()

        payload = {
            "nome_candidato": st.session_state.nome,
            "vaga": st.session_state.vaga,
            "conversa_completa": conversation
        }

        with st.spinner("Analisando atendimento..."):

            try:

                response = requests.post(
                    AGENT_ANALYZE_URL,
                    json=payload,
                    timeout=30
                )

                response.raise_for_status()

                st.success("Teste enviado com sucesso!")

                st.session_state.test_completed = True

            except Exception as e:

                st.error("Erro ao enviar teste.")


if __name__ == "__main__":
    main()
