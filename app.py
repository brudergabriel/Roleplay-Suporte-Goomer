import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Goomer - Sistema de Testes", layout="wide")

# URL base do seu agente SmythOS
AGENT_BASE_URL = "https://seu-agente.smythos.com/api"

# Interface principal
st.title("🎭 Sistema de Testes - Goomer Support")

# Abas para diferentes funcionalidades
tab1, tab2 = st.tabs(["Simulação de Cliente", "Análise de Conversa"])

with tab1:
    st.header("Simular Cliente Problemático")
    
    # Inputs para simulação
    tipo_cliente = st.selectbox(
        "Tipo de Cliente:",
        ["impaciente", "confuso", "irritado", "exigente"]
    )
    
    cenario = st.selectbox(
        "Cenário:",
        ["pedido_atrasado", "cobranca_incorreta", "produto_faltando", "app_bug", "cupom_invalido"]
    )
    
    mensagem_candidato = st.text_area("Mensagem do Candidato:", height=100)
    
    if st.button("Simular Resposta do Cliente"):
        if mensagem_candidato:
            # Chamada para a API do agente
            payload = {
                "mensagem_candidato": mensagem_candidato,
                "tipo_cliente": tipo_cliente,
                "cenario": cenario
            }
            
            with st.spinner("Gerando resposta do cliente..."):
                try:
                    response = requests.post(
                        f"{AGENT_BASE_URL}/simular_cliente",
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        st.success("Resposta do Cliente:")
                        st.write(resultado)
                    else:
                        st.error(f"Erro: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")

with tab2:
    st.header("Analisar Performance do Candidato")
    
    # Inputs para análise
    nome_candidato = st.text_input("Nome do Candidato:")
    vaga = st.selectbox("Vaga:", ["Suporte Jr", "Suporte Pleno", "Suporte Senior"])
    conversa_completa = st.text_area("Conversa Completa:", height=200)
    
    if st.button("Analisar Performance"):
        if nome_candidato and conversa_completa:
            payload = {
                "nome_candidato": nome_candidato,
                "conversa_completa": conversa_completa,
                "vaga": vaga
            }
            
            with st.spinner("Analisando performance..."):
                try:
                    response = requests.post(
                        f"{AGENT_BASE_URL}/analisar_conversa",
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        
                        # Mostrar resultados de forma organizada
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Nota Final", f"{resultado.get('nota_final', 0)}/10")
                            st.write(f"**Classificação:** {resultado.get('classificacao', '')}")
                        
                        with col2:
                            st.write("**Notas por Critério:**")
                            st.write(f"Conversa: {resultado.get('conversa', 0)}/10")
                            st.write(f"Escrita: {resultado.get('escrita', 0)}/10")
                            st.write(f"Empatia: {resultado.get('empatia', 0)}/10")
                            st.write(f"Investigação: {resultado.get('investigacao', 0)}/10")
                            st.write(f"Resolução: {resultado.get('resolucao', 0)}/10")
                        
                        st.write(f"**Conclusão:** {resultado.get('conclusao', '')}")
                        st.success("✅ Dados enviados para a planilha!")
                        
                    else:
                        st.error(f"Erro: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")
