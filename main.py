import streamlit as st
import urllib.parse

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    h1, h2 { color: #D4AF37 !important; text-align: center; font-weight: bold; }
    .stInfo { background-color: #111111; border: 1px solid #D4AF37; color: white; }
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold !important;
        height: 60px;
        border-radius: 10px;
    }
    .card-aluno {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #D4AF37;
        margin-bottom: 20px;
    }
    .status-fixo {
        background-color: #D4AF37;
        color: black;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS DE ALUNOS FIXOS
# O sistema ignora maiúsculas/minúsculas para facilitar a busca
ALUNOS_FIXOS = {
    "tathyanne": "11:30 am",
    "taina": "11:30 am",
    "vanderleia lucena": "15:00",
    "cleiia caroline": "18:00",
    "guilherme": "20:30",
    "thaina sena": "20:30"
}

st.title("SISTEMA DE AGENDAMENTO")
st.markdown("<h3 style='text-align: center; color: #888;'>TEAM MUNIZ</h3>", unsafe_allow_html=True)

# 3. IDENTIFICAÇÃO DO ALUNO
st.write("### 1. Identifique-se")
with st.container():
    st.markdown('<div class="card-aluno">', unsafe_allow_html=True)
    nome_input = st.text_input("Digite seu Nome Completo:").strip().lower()
    whatsapp = st.text_input("WhatsApp com DDD:")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. LÓGICA DE RECONHECIMENTO
if nome_input:
    # Busca se o nome digitado contém algum dos nomes dos alunos fixos
    aluno_encontrado = None
    horario_fixo = None
    
    for nome_fixo, horario in ALUNOS_FIXOS.items():
        if nome_fixo in nome_input:
            aluno_encontrado = nome_fixo.title()
            horario_fixo = horario
            break

    if aluno_encontrado:
        st.markdown(f'<div class="status-fixo">ALUNO FIXO DETECTADO: {aluno_encontrado}</div>', unsafe_allow_html=True)
        st.info(f"Seu horário padrão é às **{horario_fixo}**. Deseja confirmar para esta semana ou precisa trocar?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("CONFIRMAR MEU HORÁRIO"):
                msg = f"Olá Fábio, sou {aluno_encontrado}. Confirmando meu horário fixo das {horario_fixo}!"
                link_zap = f"https://wa.me/5511959617342?text={urllib.parse.quote(msg)}"
                st.link_button("✅ Enviar Confirmação", link_zap)
        
        with col2:
            if st.button("SOLICITAR TROCA"):
                st.warning("Acesse a agenda abaixo para ver disponibilidades de exceção.")
                st.link_button("📅 Ver Outros Horários", "https://calendar.app.google/YGhyV7GK38tuBBtv8")

    else:
        # Fluxo para novos alunos ou alunos não fixos
        st.write("### 2. Escolha seu horário")
        st.info("Clique abaixo para ver os horários disponíveis na agenda oficial.")
        
        if st.button("ABRIR AGENDA GOOGLE"):
            if nome_input and whatsapp:
                link_google = "https://calendar.app.google/YGhyV7GK38tuBBtv8"
                st.link_button("📅 Acessar Calendário", link_google)
            else:
                st.error("Por favor, preencha nome e WhatsApp.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 14px;'>Sem estratégia, esforço vira tentativa.</p>", unsafe_allow_html=True)
