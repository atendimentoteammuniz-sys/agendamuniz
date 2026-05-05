import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

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
        height: 50px;
        border-radius: 8px;
    }
    .step-text { color: #D4AF37; font-size: 14px; text-transform: uppercase; }
    .card { background-color: #111111; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS DE ALUNOS FIXOS
ALUNOS_FIXOS = {
    "tathyanne": "11:30", "taina": "11:30", "vanderleia lucena": "15:00",
    "cleiia caroline": "18:00", "guilherme": "20:30", "thaina sena": "20:30"
}

if 'step' not in st.session_state:
    st.session_state.step = 1

def proximo_passo(): st.session_state.step += 1
def voltar_passo(): st.session_state.step -= 1

# Função para criar link direto de salvamento no Google Agenda
def link_google(nome, modalidade, data_str, hora_str):
    try:
        data_dt = datetime.strptime(f"{data_str} {hora_str}", "%d/%m/%Y %H:%M")
        data_fim = data_dt + timedelta(hours=1)
        fmt = "%Y%m%dT%H%M%SZ"
        titulo = urllib.parse.quote(f"{modalidade.upper()}: {nome.upper()}")
        return f"https://www.google.com/calendar/render?action=TEMPLATE&text={titulo}&dates={data_dt.strftime(fmt)}/{data_fim.strftime(fmt)}&sf=true&output=xml"
    except:
        return "#"

# ETAPA 1: NOME
if st.session_state.step == 1:
    st.markdown('<p class="step-text">Etapa 1</p>', unsafe_allow_html=True)
    st.title("Qual é seu nome?")
    nome = st.text_input("Nome Completo *", placeholder="Digite seu nome...", key="n1")
    if st.button("Próximo >"):
        if nome:
            st.session_state.nome = nome.strip()
            proximo_passo()
            st.rerun()
        else: st.error("Digite seu nome.")

# ETAPA 2: MODALIDADE
elif st.session_state.step == 2:
    st.markdown('<p class="step-text">Etapa 2</p>', unsafe_allow_html=True)
    st.title("O que vamos agendar?")
    modalidade = st.selectbox("Selecione a modalidade *", [
        "Treino Presencial", "Consultoria On-line", 
        "Avaliação Bioimpedância", "Aula Experimental"
    ])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Próximo >"):
            st.session_state.modalidade = modalidade
            proximo_passo()
            st.rerun()

# ETAPA 3: DATA ÚNICA E HORÁRIOS
elif st.session_state.step == 3:
    st.markdown('<p class="step-text">Etapa 3</p>', unsafe_allow_html=True)
    st.title("Data e Horários")
    
    # Seleciona a data apenas uma vez
    data_selecionada = st.date_input("Selecione o dia das aulas", min_value=datetime.now().date())
    st.session_state.data = data_selecionada.strftime("%d/%m/%Y")
    
    st.write("Defina os horários (você pode agendar até 3 aulas no mesmo dia ou deixar em branco):")
    
    nome_min = st.session_state.nome.lower()
    horario_padrao = next((h for n, h in ALUNOS_FIXOS.items() if n in nome_min), "08:00")
    
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h1 = st.text_input("Horário Aula 1", value=horario_padrao)
    with col_h2: h2 = st.text_input("Horário Aula 2", placeholder="Ex: 14:00")
    with col_h3: h3 = st.text_input("Horário Aula 3", placeholder="Ex: 19:00")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Próximo >"):
            st.session_state.horarios = [h for h in [h1, h2, h3] if h]
            proximo_passo()
            st.rerun()

# ETAPA 4: TERMOS
elif st.session_state.step == 4:
    st.markdown('<p class="step-text">Etapa 4</p>', unsafe_allow_html=True)
    st.title("Termos e Condições")
    st.markdown('<div class="card"><b>Tolerância:</b> 20 min (abatido da aula).<br><b>Cancelamento:</b> Mínimo 24h.</div>', unsafe_allow_html=True)
    aceito = st.checkbox("Eu concordo com os termos")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Finalizar"):
            if aceito: proximo_passo(); st.rerun()
            else: st.warning("Aceite os termos.")

# ETAPA 5: CONFIRMAÇÃO E GOOGLE AGENDA
elif st.session_state.step == 5:
    st.balloons()
    st.title("Resumo e Sincronização")
    st.write(f"Paciente/Aluno: **{st.session_state.nome}**")
    
    resumo_wpp = f"*AGENDAMENTO TEAM MUNIZ*\n👤 {st.session_state.nome}\n🎯 {st.session_state.modalidade}\n📅 Data: {st.session_state.data}\n\n"
    
    for i, hora in enumerate(st.session_state.horarios, 1):
        st.markdown(f'<div class="card"><b>Aula {i}:</b> {st.session_state.data} às {hora}</div>', unsafe_allow_html=True)
        link = link_google(st.session_state.nome, st.session_state.modalidade, st.session_state.data, hora)
        st.link_button(f"📅 SALVAR AULA {i} NO MEU GOOGLE", link)
        resumo_wpp += f"✅ Aula {i}: {hora}\n"

    st.write("---")
    st.link_button("🚀 ENVIAR CONFIRMAÇÃO VIA WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(resumo_wpp)}")
    
    if st.button("Novo Agendamento"):
        st.session_state.step = 1
        st.rerun()
