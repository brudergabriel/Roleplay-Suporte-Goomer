import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Goomer - Simulação de Suporte", layout="wide")

# URL base do seu agente SmythOS
AGENT_BASE_URL = "https://seu-agente.smythos.com/api"

# Inicializa estado da conversa
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

st.title("🎭 Simulação de Atendimento - Goomer")

# Sidebar para configurações do candidato
with st.sidebar:
    st.header("Configuração do Candidato")
    nome_candidato = st.text_input("Nome do Candidato")
    vaga = st.selectbox("Vaga", ["Suporte Jr", "Suporte Pleno", "Suporte Senior"])
    if st.button("Iniciar Simulação"):
        st.session_state.chat_history = []
        st.session_state.analysis_done = False

# Função para enviar mensagem do candidato e receber resposta simulada do cliente
def enviar_mensagem_candidato(mensagem):
    payload = {
        "mensagem_candidato": mensagem,
        # Se precisar, envie mais dados para o endpoint simular_cliente
    }
    try:
        resp = requests.post(f"{AGENT_BASE_URL}/simular_cliente", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("resposta_cliente", "Erro: resposta vazia")
    except Exception as e:
        return f"Erro na comunicação: {str(e)}"

# Função para enviar toda conversa para análise
def analisar_conversa(conversa_completa):
    payload = {
        "nome": nome_candidato,
        "conversa": conversa_completa,
        "vaga": vaga,
    }
    try:
        resp = requests.post(f"{AGENT_BASE_URL}/analisar_conversa", json=payload)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Erro na análise: {str(e)}")
        return None

# Interface principal de chat
if nome_candidato and vaga:
    st.subheader(f"Candidato: {nome_candidato} | Vaga: {vaga}")

    # Mostra histórico da conversa
    for i, (autor, msg) in enumerate(st.session_state.chat_history):
        if autor == "Candidato":
            st.markdown(f"**Você:** {msg}")
        else:
            st.markdown(f"**Cliente:** {msg}")

    # Entrada de nova mensagem do candidato
    if not st.session_state.analysis_done:
        nova_msg = st.text_input("Digite sua mensagem:", key="input_candidato")
        if st.button("Enviar", key="btn_enviar") and nova_msg:
            # Atualiza histórico com mensagem do candidato
            st.session_state.chat_history.append(("Candidato", nova_msg))
            # Envia para simulação do cliente
            resposta_cliente = enviar_mensagem_candidato(nova_msg)
            st.session_state.chat_history.append(("Cliente", resposta_cliente))
            # Limpa input
            st.experimental_rerun()

    # Botão para finalizar e analisar conversa
    if st.button("Finalizar Conversa e Analisar"):
        conversa_texto = "\n".join(
            [f"{autor}: {msg}" for autor, msg in st.session_state.chat_history]
        )
        resultado = analisar_conversa(conversa_texto)
        if resultado:
            st.session_state.analysis_done = True
            st.success("Conversa analisada com sucesso. Resultados são confidenciais e não mostrados ao candidato.")
            # Aqui você pode salvar ou enviar o resultado para outra área administrativa
else:
    st.info("Preencha seu nome e selecione uma vaga para começar a simulação.")
