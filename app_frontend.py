import streamlit as st
import requests
import time
import random
import os

# Força o sistema a ignorar o proxy para conexões de rede local
os.environ['NO_PROXY'] = '127.0.0.1,localhost'

st.set_page_config(
    page_title="Ore-Bit — Central de Mineração",
    page_icon="☄️",
    layout="wide"
)

# URL base da API do seu Django - Garantindo a porta padrão 8000 e IP estável
API_BASE_URL = "http://127.0.0.1:8000/api"

st.title("🛸 Ore-Bit — Painel de Mapeamento e Extração")
st.write("Insira os dados manualmente. O Streamlit enviará o alvo para o Django e processará a extração.")
st.divider()

# --- PAINEL DE ENTRADA MANUAL (FORMULÁRIO) ---
col_form, col_espaco = st.columns([1, 1])

with col_form:
    with st.form(key="cadastro_asteroide", clear_on_submit=False):
        st.subheader("📝 Registrar Novo Alvo no Django")
        
        nome = st.text_input("Nome/Designação do Asteroide", placeholder="Ex: Psyche 16")
        tipo = st.selectbox("Classe/Tipo", ["M", "C", "S"])
        distancia = st.number_input("Distância da Base (Unidades)", min_value=1, value=120)
        tamanho = st.number_input("Tamanho do Asteroide (km)", min_value=0.1, value=10.0, step=0.1)
        st.write("📊 **Composição Estimada (0% a 100%):**")
        ferro = st.slider("Porcentagem de Ferro (%)", 0, 100, 45)
        niquel = st.slider("Porcentagem de Níquel (%)", 0, 100, 15)
        platina = st.slider("Porcentagem de Platina (%)", 0, 100, 5)
        agua = st.slider("Porcentagem de Água (%)", 0, 100, 10)
        
        botao_mapear = st.form_submit_button(label="🛰️ Salvar no Backend & Minerar", use_container_width=True)

# --- SINCROCONIZAÇÃO E ANIMAÇÃO ---
if botao_mapear:
    if not nome:
        st.error("Por favor, digite o nome do asteroide!")
    else:
        with col_espaco:
            # 1. SALVANDO O ASTEROIDE NO BACKEND (DJANGO)
            # Convertendo explicitamente os tipos primitivos exigidos pelo serializer
            payload_asteroide = {
                "nome": str(nome),
                "tipo": str(tipo),
                "distancia": int(distancia),
                "tamanho": float(tamanho), 
                "ferro": int(ferro),
                "niquel": int(niquel),
                "platina": int(platina),
                "agua": int(agua)
            }
            
            asteroide_id = None
            
            with st.spinner("💾 Sincronizando alvo com o banco de dados do Django..."):
                try:
                    response_ast = requests.post(f"{API_BASE_URL}/asteroides/", json=payload_asteroide)
                    
                    if response_ast.status_code == 201:
                        st.caption("✅ Asteroide salvo com sucesso no banco de dados!")
                        asteroide_id = response_ast.json().get('id')
                    else:
                        st.error(f"⚠️ O Django recusou os dados (Erro {response_ast.status_code})")
                        # Revela na interface o motivo estrutural do erro 400 enviado pelo serializer
                        try:
                            st.json(response_ast.json())
                        except:
                            st.text(response_ast.text)
                            
                except Exception as e:
                    st.error(f"❌ Erro de conexão com o Django: {e}")
            
            # Se o asteroide foi salvo com sucesso no banco
            if asteroide_id:
                # 2. MOSTRANDO O CARD NA TELA
                with st.container(border=True):
                    st.header(f"🪨 Alvo Lockado: {nome} (ID: {asteroide_id})")
                    st.caption(f"Classe: Tipo {tipo} | Distância: {distancia} UA")
                    st.divider()
                    
                    # 3. ANIMAÇÃO DA MINERAÇÃO
                    st.info("🚨 Sequência de lasers de extração ativada...")
                    barra_progresso = st.progress(0)
                    status_texto = st.empty()
                    
                    for porcentagem in range(1, 101):
                        time.sleep(0.02)
                        barra_progresso.progress(porcentagem)
                        if porcentagem < 50:
                            status_texto.text(f"⚡ Fragmentando núcleo metálico... ({porcentagem}%)")
                        else:
                            status_texto.text(f"📦 Recolhendo carga para os compartimentos... ({porcentagem}%)")
                    
                    status_texto.empty()
                    barra_progresso.empty()
                    
                    # 4. CÁLCULO DOS RESULTADOS
                    fator_riqueza = (ferro * 1) + (niquel * 1.5) + (platina * 5)
                    toneladas_obtidas = round(random.uniform(10, 50) * (fator_riqueza / 100), 2)
                    valor_mercado = round(toneladas_obtidas * random.uniform(200, 600), 2)
                    
                    st.success("🏆 Operação Concluída!")
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric(label="Total Refinado", value=f"{toneladas_obtidas} T")
                    with m2:
                        st.metric(label="Faturamento", value=f"🪙 Credits {valor_mercado:,.2f}")
                    
                    # 5. SALVANDO O HISTÓRICO DE MINERAÇÃO NO BACKEND (DJANGO)
                    payload_mineracao = {
                    "asteroide": int(asteroide_id), 
                    "total_minerado": float(toneladas_obtidas),
                    "valor_ganho": float(valor_mercado)
}
                    
                    try:
                        response_min = requests.post(f"{API_BASE_URL}/mineracoes/", json=payload_mineracao)
                        if response_min.status_code == 201:
                            st.caption("⚙️ Histórico de mineração salvo com sucesso no Django!")
                        else:
                            st.warning(f"⚠️ O asteroide foi criado, mas a mineração foi rejeitada. Erro {response_min.status_code}")
                            st.json(response_min.json())
                    except:
                        st.caption("⚠️ Erro ao conectar para salvar o relatório de mineração.")