import streamlit as st
import urllib.parse
from datetime import datetime

# 1. IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"

st.markdown("""
    <style>
    .main { background-color: #000000; }
    h1, h2, h3 { color: #D4AF37 !important; font-weight: bold; }
    .stMarkdown { color: white; }
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        height: 50px;
        border-radius: 8px;
    }
    .card { background-color: #111111; padding: 20px; border-radius: 12px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO SEGURA DO ESTADO
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'modalidade' not in st.session_state: st.session_state.modalidade = ""
if 'datas_selecionadas' not in st.session_state: st.session_state.datas_selecionadas = []

# --- FLUXO DE TELAS ---

# ETAPA 1: NOME
if st.session_state.step == 1:
    st.title("Team Muniz")
    nome_input = st.text_input("Informe seu nome completo:", value=st.session_state.nome)
    if st.button("PRÓXIMO >"):
        if nome_input:
            st.session_state.nome = nome_input.strip()
            st.session_state.step = 2
            st.rerun()
        else: st.error("O nome é obrigatório.")

# ETAPA 2: MODALIDADE E DATAS
elif st.session_state.step == 2:
    st.title("Detalhes do Treino")
    st.session_state.modalidade = st.selectbox("Escolha a modalidade:", 
        ["Treino Presencial", "Consultoria On-line", "Avaliação Bioimpedância"],
        index=0 if not st.session_state.modalidade else ["Treino Presencial", "Consultoria On-line", "Avaliação Bioimpedância"].index(st.session_state.modalidade)
    )
    
    st.write("Selecione as 3 datas pretendidas (DD/MM/AAAA):")
    d1 = st.date_input("Data da Aula 01", format="DD/MM/YYYY")
    d2 = st.date_input("Data da Aula 02", format="DD/MM/YYYY")
    d3 = st.date_input("Data da Aula 03", format="DD/MM/YYYY")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("PRÓXIMO >"):
            st.session_state.datas_selecionadas = [d1, d2, d3]
            st.session_state.step = 3
            st.rerun()

# ETAPA 3: TERMOS E CONDIÇÕES
elif st.session_state.step == 3:
    st.title("Termos do Time")
    st.markdown("""
    <div class="card">
    <b>Regras Team Muniz:</b><br>
    - Tolerância de atraso: 20 min.<br>
    - Cancelamento: Mínimo de 24h de antecedência.<br>
    - O agendamento só é oficial após a confirmação na agenda do Coach.
    </div>
    """, unsafe_allow_html=True)
    
    aceito = st.checkbox("Eu concordo com os termos e regras")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 2; st.rerun()
    with col2:
        if st.button("FINALIZAR >"):
            if aceito:
                st.session_state.step = 4
                st.rerun()
            else: st.warning("Aceite os termos para continuar.")

# ETAPA 4: AGENDA E WHATSAPP
elif st.session_state.step == 4:
    st.balloons()
    st.title("Concluir Agendamento")
    
    # Verificação de segurança para o nome não vir vazio ou errado
    nome_final = st.session_state.nome
    mod_final = st.session_state.modalidade
    
    st.markdown(f"""
    <div class="card">
    <b>Aluno:</b> {nome_final}<br>
    <b>Modalidade:</b> {mod_final}<br>
    <b>Próximo passo:</b> Clique no botão abaixo para escolher seus horários livres.
    </div>
    """, unsafe_allow_html=True)

    st.link_button("📅 ABRIR AGENDA DO COACH", LINK_AGENDA_REAL)

    st.write("---")
    
    # Montagem da mensagem do WhatsApp garantindo o nome correto
    datas_txt = ", ".join([d.strftime('%d/%m/%Y') for d in st.session_state.datas_selecionadas])
    msg_zap = f"Olá Fábio, aqui é o {nome_final}. Acabei de solicitar agendamento de {mod_final} para as datas: {datas_txt}."
    
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg_zap)}")

    if st.button("RECOMEÇAR"):
        st.session_state.step = 1
        st.session_state.nome = ""
        st.rerun()
