import streamlit as st
import time

st.set_page_config(page_title="Roleplay Goomer", layout="centered")

# Estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "finished" not in st.session_state:
    st.session_state.finished = False


# ---------- HEADER ----------
st.title("Roleplay - Suporte Goomer 💙")
st.caption("Simulação de atendimento via chat")


# ---------- CRONÔMETRO ----------
elapsed_time = int(time.time() - st.session_state.start_time)
minutes = elapsed_time // 60
seconds = elapsed_time % 60

st.info(f"⏱ Tempo de teste: {minutes:02d}:{seconds:02d}")


# ---------- CHAT ----------
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


# ---------- BOTÃO FINALIZAR ----------
if not st.session_state.finished:
    if st.button("Finalizar Teste"):
        st.session_state.finished = True
        st.success("Teste finalizado. Obrigado por participar!")
