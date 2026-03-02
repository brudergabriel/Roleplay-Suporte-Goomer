import streamlit as st
import requests
import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Roleplay - Suporte Goomer", layout="centered")

# ------------------------
# ESTADO DA SESSÃO
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "finished" not in st.session_state:
    st.session_state.finished = False


# ------------------------
# FUNÇÃO PARA ENVIAR À API
# ------------------------
def enviar_para_analise(nome, email, vaga, conversa_texto):
    url = "https://cmm3ufw1v9rn2ih5tr5uohspm.agent.a.smyth.ai/api/analisar_conversa"

    payload = {
        "nome_candidato": nome,
        "email": email,
        "vaga": vaga,
        "conversa_completa": conversa_texto,
        "timestamp": str(datetime.datetime.now())
    }

    try:
        response = requests.post(url, json=payload, timeout=90)
        return response.status_code == 200
    except:
        return False


# ------------------------
# INTERFACE
# ------------------------
st.title("Roleplay - Suporte Goomer 💙")
st.caption("Simulação de atendimento via chat")

# Dados do candidato
nome = st.text_input("Nome completo")
email = st.text_input("Email")
vaga = st.selectbox("Nível da vaga", ["Suporte Jr", "Suporte Pleno", "Suporte Sr"])

st.divider()

# ------------------------
# MENSAGEM INICIAL DO CLIENTE
# ------------------------
if not st.session_state.initialized:
    mensagem_inicial = """
Oi, bom dia.

Ontem falei com você sobre um estorno de um pedido que tinha sido cobrado duas vezes.

Hoje vi que o valor foi devolvido duas vezes.

Isso vai me gerar prejuízo.

O que aconteceu?
"""
    st.session_state.messages.append(
        {"role": "assistant", "content": mensagem_inicial}
    )
    st.session_state.initialized = True


# ------------------------
# CHAT
# ------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.finished:
    prompt = st.chat_input("Digite sua resposta...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        st.rerun()


# ------------------------
# FINALIZAR TESTE
# ------------------------
if not st.session_state.finished:
    if st.button("Finalizar Teste"):
        if not nome or not email:
            st.warning("Preencha nome e email antes de finalizar.")
        else:
            st.session_state.finished = True

            # Montar texto completo da conversa
            conversa_texto = ""
            for msg in st.session_state.messages:
                role = "Cliente" if msg["role"] == "assistant" else "Analista"
                conversa_texto += f"{role}:\n{msg['content']}\n\n"

            sucesso = enviar_para_analise(nome, email, vaga, conversa_texto)

            if sucesso:
                st.success("Teste enviado com sucesso! ✅")
                st.info("Nossa equipe analisará seu atendimento.")
            else:
                st.error("Erro ao enviar teste. Tente novamente.")
