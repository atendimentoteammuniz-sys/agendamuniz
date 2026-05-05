import streamlit as st
import urllib.parse
from datetime import datetime

# 1. CONFIGURAÇÃO DE TELA E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento Real", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
# Seu link oficial do Google Appointment Slots
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"

# Estilização Profissional
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
        border: none;
    }
    .card { 
        background-color: #111111; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #D4AF37; 
        margin-bottom: 15px;
    }
    .instrucao { color: #aaaaaa; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# 2. GERENCIAMENTO DE ESTADO
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'datas_selecionadas' not in st.session_state: st.session_state.datas_selecionadas = []

# --- NAVEGAÇÃO ---

# TELA 1: IDENTIFICAÇÃO
if st.session_state.step == 1:
    st.title("Team Muniz")
    st.subheader("Consultoria & Treinamento")
    
    nome = st.text_input("Informe seu nome completo:", value=st.session_state.nome)
    
    if st.button("VERIFICAR DISPONIBILIDADE"):
        if nome:
            st.session_state.nome = nome.strip()
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Por favor, digite seu nome para continuar.")

# TELA 2: SELEÇÃO DE DATAS
elif st.session_state.step == 2:
    st.title("Agendamento Estratégico")
    st.write(f"Olá, **{st.session_state.nome}**. Selecione as 3 datas pretendidas:")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        d1 = st.date_input("Data da Aula 01", format="DD/MM/YYYY")
        d2 = st.date_input("Data da Aula 02", format="DD/MM/YYYY")
        d3 = st.date_input("Data da Aula 03", format="DD/MM/YYYY")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info("No próximo passo, você escolherá os horários exatos que estão LIVRES na minha agenda oficial.")

    if st.button("CONFIRMAR DATAS E VER HORÁRIOS"):
        st.session_state.datas_selecionadas = [d1, d2, d3]
        st.session_state.step = 3
        st.rerun()

# TELA 3: VALIDAÇÃO NA AGENDA REAL
elif st.session_state.step == 3:
    st.title("Horários Disponíveis")
    
    st.markdown(f"""
    <div class="card">
        <p><b>Passo Final Obrigatório:</b></p>
        <p class="instrucao">Para garantir que não haja conflitos, clique no botão abaixo. Escolha os horários disponíveis para as datas selecionadas:
        <br>• {st.session_state.datas_selecionadas[0].strftime('%d/%m/%Y')}
        <br>• {st.session_state.datas_selecionadas[1].strftime('%d/%m/%Y')}
        <br>• {st.session_state.datas_selecionadas[2].strftime('%d/%m/%Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Botão que leva para o seu link específico do Google
    st.link_button("📅 ESCOLHER HORÁRIOS LIVRES AGORA", LINK_AGENDA_REAL)

    st.write("---")
    
    # Mensagem de WhatsApp para avisar você
    datas_txt = ", ".join([d.strftime('%d/%m/%Y') for d in st.session_state.datas_selecionadas])
    msg_zap = f"Fábio, sou o {st.session_state.nome}. Já escolhi meus horários na sua agenda para as datas: {datas_txt}."
    
    st.link_button("📱 JÁ AGENDEI! AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg_zap)}")

    if st.button("RECOMEÇAR"):
        st.session_state.step = 1
        st.rerun()
