import streamlit as st
import requests
from datetime import datetime
import uuid

# Adicione esta função para forçar variação
def get_client_llm_response(candidate_message):
    # Adiciona timestamp único para forçar resposta diferente
    unique_context = f"[Conversa #{st.session_state.interaction_count} - {datetime.now().strftime('%H:%M:%S')}] {candidate_message}"
    
    payload = {
        "mensagem_candidato": unique_context,
        "tipo_cliente": get_client_persona(),
        "cenario": "estorno_duplicado"
    }
    
    # Debug
    print(f"🚀 Enviando: {payload}")
    
    try:
        response = requests.post(
            AGENT_SIMULATE_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "X-Request-ID": str(uuid.uuid4())  # ID único por requisição
            },
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        print(f"📥 Recebido: {data}")
        
        # Extração mais robusta
        if isinstance(data, dict):
            result = (
                data.get("Output") or
                data.get("resposta_cliente") or 
                data.get("reply") or
                str(data)
            )
            return result
            
        return str(data)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        # Fallbacks diferentes baseados na iteração
        fallbacks = [
            "Tá, mas como vocês vão resolver isso?",
            "Quanto tempo vai levar?", 
            "Mas isso resolve o meu prejuízo?",
            "Vocês conseguem verificar isso agora?"
        ]
        return fallbacks[st.session_state.interaction_count % len(fallbacks)]
