import streamlit as st
import urllib.parse
from datetime import datetime

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_MINHA_AGENDA_GOOGLE = "https://calendar.app.google/YGhyV7GK38tuBBtv8"

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

# 2. BANCO DE DATOS DE ALUNOS FIXOS
ALUNOS_FIXOS = {
    "tathyanne": "11:30", "taina": "11:30", "vanderleia lucena": "15:00",
    "cleiia caroline": "18:00", "guilherme": "20:30", "thaina sena": "20:30"
}

if 'step' not in st.session_state:
    st.session_state.step = 1

def proximo_passo(): st.session_state.step += 1
def voltar_passo(): st.session_state.step -= 1

# ETAPA 1: NOME
if st.session_state.step == 1:
    st.markdown('<p class="step-text">Etapa 1</p>', unsafe_allow_html=True)
    st.title("Qual é seu nome?")
    nome = st.text_input("Nome Completo *", placeholder="Digite seu nome para verificarmos seu cadastro...")
    if st.button("Próximo >"):
        if nome:
            st.session_state.nome = nome.strip()
            proximo_passo()
            st.rerun()
        else: st.error("Digite seu nome para continuar.")

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

# ETAPA 3: RECONHECIMENTO E TERMOS
elif st.session_state.step == 3:
    st.markdown('<p class="step-text">Etapa 3</p>', unsafe_allow_html=True)
    st.title("Termos e Regras")
    
    nome_min = st.session_state.nome.lower()
    horario_padrao = next((h for n, h in ALUNOS_FIXOS.items() if n in nome_min), None)
    
    if horario_padrao:
        st.success(f"Aluno Fixo detectado! Seu horário reservado é às **{horario_padrao}**.")
        st.write("Você será direcionado para minha agenda oficial para confirmar o dia desejado.")
    else:
        st.info("Você será direcionado para minha agenda para escolher um horário disponível.")

    st.markdown("""
    <div class="card">
    <b>Regras do Time:</b><br>
    - Tolerância de atraso: 20 minutos.<br>
    - Cancelamentos: Mínimo de 24h de antecedência.<br>
    - O agendamento cai direto na agenda do Coach.
    </div>
    """, unsafe_allow_html=True)
    
    aceito = st.checkbox("Eu concordo com os termos e desejo agendar na agenda do Coach")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Ir para Agenda >"):
            if aceito:
                proximo_passo()
                st.rerun()
            else:
                st.warning("Aceite os termos para acessar a agenda.")

# ETAPA 4: FINALIZAÇÃO E DIRECIONAMENTO
elif st.session_state.step == 4:
    st.balloons()
    st.title("Tudo Pronto!")
    st.write(f"**{st.session_state.nome}**, agora é só escolher o dia e confirmar seu **{st.session_state.modalidade}**.")
    
    st.markdown("""
    <div class="card" style="border-color: #D4AF37;">
    <b>Instruções Finais:</b><br>
    1. Clique no botão abaixo para abrir minha agenda oficial.<br>
    2. Escolha o dia e o horário (fixo ou disponível).<br>
    3. Após confirmar no Google, me envie o aviso pelo WhatsApp.
    </div>
    """, unsafe_allow_html=True)

    # BOTÃO QUE VAI PARA A SUA AGENDA (Onde o aluno marca e cai pra você)
    st.link_button("📅 ABRIR MINHA AGENDA (GOOGLE CALENDAR)", LINK_MINHA_AGENDA_GOOGLE)
    
    st.write("---")
    
    # WHATSAPP DE AVISO
    resumo_wpp = f"Olá Fábio, aqui é {st.session_state.nome}. Acabei de acessar sua agenda para marcar um(a) {st.session_state.modalidade}!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(resumo_wpp)}")

    if st.button("Recomeçar"):
        st.session_state.step = 1
        st.rerun()
