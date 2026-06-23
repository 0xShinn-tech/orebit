import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Ore-Bit — Central de Mineração", 
    page_icon="☄️", 
    layout="wide"
)

# URL base da API do Django
API_BASE_URL = "http://127.0.0.1:8000/api"

# ==========================================
# SIDEBAR: NAVEGAÇÃO COMPLETA
# ==========================================
with st.sidebar:
    st.title("🛸 Ore-Bit Control")
    st.success("🟢 Modo de Acesso Aberto")
    st.divider()
    
    st.subheader("📍 Navegação")
    menu = st.radio(
        "Ir para:", 
        ["Central de Mineração", "Radar Espacial", "Cadastrar Naves", "Histórico de Operações"]
    )
    
    st.divider()
    st.caption("Controle de Extração e Gestão de Ativos Espaciais v2.0")

# ==========================================
# PÁGINA 1: CENTRAL DE MINERAÇÃO
# ==========================================
if menu == "Central de Mineração":
    st.title("🛸 Ore-Bit — Painel de Mapeamento")
    st.write("Visão geral em tempo real do processamento de minérios da frota.")
    
    try:
        response_naves = requests.get(f"{API_BASE_URL}/naves/", timeout=3)
        total_naves = len(response_naves.json()) if response_naves.status_code == 200 else 0
    except:
        total_naves = "— (Backend offline)"

    # Layout de Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Naves Ativas na Frota", value=total_naves)
    with col2:
        st.metric(label="Minério Extraído (Mês)", value="14,250 t", delta="+12%")
    with col3:
        st.metric(label="Quadrantes Mapeados", value="42/100", delta="5 novos")
        
    st.divider()
    
    st.subheader("📈 Produção de Minério por Quadrante")
    dados_grafico = pd.DataFrame({
        "Quadrante": ["Alpha-1", "Beta-2", "Gama-3", "Delta-4", "Epsilon-5"],
        "Ferro (t)": [450, 700, 320, 890, 510],
        "Platina (t)": [50, 120, 90, 210, 40]
    })
    
    fig = px.bar(dados_grafico, x="Quadrante", y=["Ferro (t)", "Platina (t)"], barmode="group")
    st.plotly_chart(fig, width='stretch')


# ==========================================
# PÁGINA 2: RADAR ESPACIAL (NOVA UTILIDADE)
# ==========================================
elif menu == "Radar Espacial":
    st.title("🛰️ Radar de Varredura Espacial")
    st.write("Monitore e selecione alvos ativos detectados nos quadrantes para mineração imediata.")
    st.divider()

    alvos = []
    naves = []
    backend_online = True

    # Coleta de dados do Django
    try:
        res_radar = requests.get(f"{API_BASE_URL}/radar/", timeout=3)
        res_naves = requests.get(f"{API_BASE_URL}/naves/", timeout=3)
        if res_radar.status_code == 200: alvos = res_radar.json()
        if res_naves.status_code == 200: naves = res_naves.json()
    except requests.exceptions.ConnectionError:
        backend_online = False
        st.warning("⚠️ Modo de Simulação: Desconectado do Django views.py. Exibindo alvos simulados.")
        alvos = [
            {"id": 1, "nome_alvo": "Asteroide Apophis-9", "quadrante": "Alpha-3", "minerio_disponivel": "Ferro", "volume_estimado": 1200.0, "perigo_nivel": "Baixo"},
            {"id": 2, "nome_alvo": "Cluster Ceres-B", "quadrante": "Beta-1", "minerio_disponivel": "Platina", "volume_estimado": 350.0, "perigo_nivel": "Alto"},
            {"id": 3, "nome_alvo": "Cometa Halley-X", "quadrante": "Gama-5", "minerio_disponivel": "Silício", "volume_estimado": 800.0, "perigo_nivel": "Médio"}
        ]
        naves = [{"id": 1, "nome": "Nave Simulada Vanguard"}]

    if not alvos:
        st.info("Nenhum corpo celeste detectado no radar neste momento.")
    else:
        # Monta a exibição gráfica do Radar usando Plotly Polar
        df_radar = pd.DataFrame(alvos)
        # Cria ângulos e distâncias arbitrárias baseadas no volume para plotar no gráfico circular
        df_radar['Distância (UA)'] = [5.0, 2.3, 7.1] if not backend_online else [float(x['id']) * 1.5 for x in alvos]
        df_radar['Ângulo'] = [45, 180, 290] if not backend_online else [float(x['id']) * 60 for x in alvos]
        
        fig_radar = px.scatter_polar(
            df_radar, r="Distância (UA)", theta="Ângulo", size="volume_estimado",
            color="perigo_nivel", hover_name="nome_alvo", template="plotly_dark",
            title="Sinais Ativos de Varredura", size_max=30
        )
        fig_radar.update_layout(polar=dict(angularaxis=dict(showticklabels=False, ticks='')))
        st.plotly_chart(fig_radar, width='stretch')
        
        st.divider()

        # Formulário de Escolha do Alvo para Minerar
        with st.form("ordem_mineracao_form"):
            st.subheader("🎯 Travar Mira e Despachar Nave")
            
            lista_alvos_str = [f"{a['nome_alvo']} | {a['minerio_disponivel']} ({a['volume_estimado']}t)" for a in alvos]
            lista_naves_str = [n['nome'] for n in naves]
            
            col_alvo, col_nave = st.columns(2)
            with col_alvo:
                alvo_selecionado = st.selectbox("Alvo Detectado", lista_alvos_str)
            with col_nave:
                nave_selecionada = st.selectbox("Nave Disponível", lista_naves_str)
                
            idx_alvo = lista_alvos_str.index(alvo_selecionado)
            dados_alvo_pure = alvos[idx_alvo]
            
            quantidade = st.number_input(
                f"Volume de Extração Solicitado (Max: {dados_alvo_pure['volume_estimado']}t)", 
                min_value=1.0, max_value=float(dados_alvo_pure['volume_estimado']), value=float(dados_alvo_pure['volume_estimado'])/2
            )
            
            btn_disparar = st.form_submit_button("💥 Executar Incursão de Extração", width='stretch')
            
            if btn_disparar:
                payload_operacao = {
                    "nave": nave_selecionada,
                    "minerio": dados_alvo_pure['minerio_disponivel'],
                    "quantidade": quantidade
                }
                
                if backend_online:
                    try:
                        res = requests.post(f"{API_BASE_URL}/historico/", json=payload_operacao, timeout=4)
                        if res.status_code in [200, 201]:
                            st.success(f"Ordem aceita! A nave {nave_selecionada} coletou {quantidade}t de {dados_alvo_pure['minerio_disponivel']}.")
                        else:
                            st.error(f"O Django recusou o registro (Status {res.status_code}).")
                    except:
                        st.error("Falha ao comunicar envio com o servidor.")
                else:
                    st.success(f"🚀 [SIMULAÇÃO] Ordem processada localmente para {nave_selecionada} extrair {quantidade}t.")


# ==========================================
# PÁGINA 3: CADASTRAR NAVES
# ==========================================
elif menu == "Cadastrar Naves":
    st.title("🚀 Gerenciamento da Frota")
    st.write("Adicione novas embarcações com especificações técnicas correspondentes ao banco.")
    
    with st.form("cadastro_nave_form"):
        st.subheader("Ficha Técnica da Embarcação")
        
        col_nome, col_tipo = st.columns(2)
        with col_nome:
            nome_nave = st.text_input("Nome da Nave", placeholder="Ex: Nebulosa X")
        with col_tipo:
            tipo_nave = st.selectbox("Classe/Tipo", ["Mineradora", "Cargueiro", "Reconhecimento"])
            
        col_cap, col_vel = st.columns(2)
        with col_cap:
            capacidade_maxima = st.number_input("Capacidade Máxima (t)", min_value=1, value=500)
        with col_vel:
            velocidade_mineracao = st.number_input("Velocidade de Mineração (t/h)", min_value=1, value=50)

        col_quad, col_status = st.columns(2)
        with col_quad:
            quadrante_atual = st.text_input("Quadrante Inicial", value="Alpha-1")
        with col_status:
            status = st.selectbox("Status Operacional", ["Ativa", "Em Manutenção", "Inativa"])
        
        botao_enviar = st.form_submit_button("Registrar Nave na Frota", width='stretch')
        
        if botao_enviar:
            if nome_nave.strip() == "":
                st.error("Por favor, insira um nome válido para a nave.")
            else:
                dados_nave = {
                    "nome": nome_nave,
                    "tipo": tipo_nave,
                    "capacidade_maxima": capacidade_maxima,
                    "velocidade_mineracao": velocidade_mineracao,
                    "status": status,
                    "quadrante": quadrante_atual,
                    "data_registro": datetime.now().strftime("%Y-%m-%d")
                }
                
                try:
                    response = requests.post(f"{API_BASE_URL}/naves/", json=dados_nave, timeout=4)
                    if response.status_code in [200, 201]:
                        st.success(f"Sucesso! A nave **{nome_nave}** foi integrada à API do Django.")
                    else:
                        st.warning(f"Erro no processamento. Status: {response.status_code}")
                        st.json(response.json()) 
                except requests.exceptions.ConnectionError:
                    st.error("Erro de Conexão: Backend Django inacessível.")
                    st.info("Payload gerado para debug:")
                    st.json(dados_nave)


# ==========================================
# PÁGINA 4: HISTÓRICO DE OPERAÇÕES
# ==========================================
elif menu == "Histórico de Operações":
    st.title("📊 Histórico Geral de Extração")
    st.write("Logs de todas as atividades de mineração registradas no banco central.")
    
    try:
        response_historico = requests.get(f"{API_BASE_URL}/historico/", timeout=4)
        if response_historico.status_code == 200:
            df = pd.DataFrame(response_historico.json())
            st.dataframe(df, width='stretch')
        else:
            st.error(f"Erro na API. Código: {response_historico.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Mostrando dados offline devido à desconexão do backend:")
        dados_mock = pd.DataFrame([
            {"ID": 1, "Nave": "Discovery I", "Minério": "Ferro", "Quantidade (t)": 120, "Data": "2026-06-22"},
            {"ID": 2, "Nave": "StarMiner", "Minério": "Platina", "Quantidade (t)": 15, "Data": "2026-06-23"}
        ])
        st.dataframe(dados_mock, width='stretch')