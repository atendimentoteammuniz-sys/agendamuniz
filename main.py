import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

# 1. IDENTIDADE VISUAL E CONFIGURAÇÃO TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_EMAIL_AGENDA = "fabiomuniz.personal@gmail.com" # SEU E-MAIL DA AGENDA
MEU_WHATSAPP = "5511987913509"

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
        height: 45px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .card { background-color: #111111; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 15px; }
    .date-text { color: #D4AF37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. ALUNOS FIXOS
ALUNOS_FIXOS = {
    "tathyanne": "11:30", "taina": "11:30", "vanderleia lucena": "15:00",
    "cleiia caroline": "18:00", "guilherme": "20:30", "thaina sena": "20:30"
}

if 'step' not in st.session_state:
    st.session_state.step = 1

# Função para formatar o link de injeção na sua agenda
def gerar_link_google(nome, modalidade, data_obj, hora_str):
    try:
        h, m = map(int, hora_str.split(':'))
        data_inicio = datetime.combine(data_obj, datetime.min.time()).replace(hour=h, minute=m)
        data_fim = data_inicio + timedelta(hours=1)
        fmt = "%Y%m%dT%H%M%SZ"
        titulo = urllib.parse.quote(f"{modalidade.upper()}: {nome.upper()}")
        # O parâmetro 'add' envia o invite direto para você
        return f"https://www.google.com/calendar/render?action=TEMPLATE&text={titulo}&dates={data_inicio.strftime(fmt)}/{data_fim.strftime(fmt)}&add={MEU_EMAIL_AGENDA}&sf=true&output=xml"
    except: return "#"

# --- FLUXO ---

if st.session_state.step == 1:
    st.title("Identificação")
    nome = st.text_input("Nome do Aluno:", placeholder="Digite seu nome completo...")
    if st.button("Próximo >"):
        if nome:
            st.session_state.nome = nome.strip()
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.title("Datas e Horários")
    modalidade = st.selectbox("Modalidade:", ["Treino Presencial", "Consultoria On-line", "Avaliação"])
    
    # Busca horário fixo
    nome_min = st.session_state.nome.lower()
    h_sugerido = next((h for n, h in ALUNOS_FIXOS.items() if n in nome_min), "08:00")
    
    st.write("Selecione as 3 datas desejadas (Padrão: DD/MM/AAAA):")
    d1 = st.date_input("Aula 01", format="DD/MM/YYYY")
    d2 = st.date_input("Aula 02", format="DD/MM/YYYY")
    d3 = st.date_input("Aula 03", format="DD/MM/YYYY")
    
    horario = st.text_input("Horário (Fração):", value=h_sugerido)
    
    if st.button("Gerar Invites >"):
        st.session_state.modalidade = modalidade
        st.session_state.datas = [d1, d2, d3]
        st.session_state.horario = horario
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.title("Injetar na Minha Agenda")
    st.write(f"Aluno: **{st.session_state.nome}** | Horário: **{st.session_state.horario}**")
    
    st.warning("Clique nos 3 botões abaixo para confirmar cada aula na minha agenda:")

    for i, data in enumerate(st.session_state.datas, 1):
        data_br = data.strftime('%d/%m/%Y')
        link = gerar_link_google(st.session_state.nome, st.session_state.modalidade, data, st.session_state.horario)
        
        with st.container():
            st.markdown(f'<div class="card">AULA {i}: <span class="date-text">{data_br}</span></div>', unsafe_allow_html=True)
            st.link_button(f"📅 ENVIAR INVITE AULA {i} ({data_br})", link)

    st.write("---")
    # Resumo para o WhatsApp
    txt_zap = f"Fábio, enviei os 3 invites de {st.session_state.modalidade} para sua agenda!\nDatas: " + ", ".join([d.strftime('%d/%m/%Y') for d in st.session_state.datas])
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(txt_zap)}")

    if st.button("Novo Agendamento"):
        st.session_state.step = 1
        st.rerun()
