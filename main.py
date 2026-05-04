import streamlit as st
import urllib.parse

# 1. IDENTIDADE VISUAL TEAM MUNIZ
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
        font-size: 18px;
    }
    .card-aluno {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #D4AF37;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CABEÇALHO
st.title("SISTEMA DE AGENDAMENTO")
st.markdown("<h3 style='text-align: center; color: #888;'>TEAM MUNIZ</h3>", unsafe_allow_html=True)

# 3. COLETA DE DADOS
st.markdown("---")
st.write("### 1. Identifique-se")
with st.container():
    st.markdown('<div class="card-aluno">', unsafe_allow_html=True)
    nome = st.text_input("Nome Completo:")
    whatsapp = st.text_input("WhatsApp com DDD:")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. BOTÃO PARA A AGENDA OFICIAL
st.write("### 2. Escolha seu horário")
st.info("Clique no botão abaixo para abrir minha agenda oficial e escolher o melhor horário disponível para você.")

if st.button("VER HORÁRIOS DISPONÍVEIS"):
    if nome and whatsapp:
        # Link da sua agenda que você enviou
        link_google_agenda = "https://calendar.app.google/YGhyV7GK38tuBBtv8"
        
        # Mensagem para o aluno te avisar depois
        texto_zap = f"Olá Fábio, aqui é o(a) {nome}. Acabei de acessar seu calendário para agendar minha aula!"
        link_zap = f"https://wa.me/5511959617342?text={urllib.parse.quote(texto_zap)}"
        
        st.success(f"Ótimo, {nome}! O calendário será aberto.")
        st.link_button("📅 ABRIR CALENDÁRIO GOOGLE", link_google_agenda)
        
        st.markdown(f"**[Após escolher o horário, clique aqui para me avisar no WhatsApp]({link_zap})**")
    else:
        st.error("Por favor, preencha seu Nome e WhatsApp antes de prosseguir.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 14px;'>Sem estratégia, esforço vira tentativa.</p>", unsafe_allow_html=True)
