import streamlit as st
import urllib.parse

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
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
    
    .caixa-nome {
        background-color: #D4AF37;
        color: black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        margin: 20px 0;
        border: 4px solid white;
        text-transform: uppercase;
    }
    .aviso-urgente {
        color: #FF4B4B;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 10px;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE ESTADO
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'modalidade' not in st.session_state: st.session_state.modalidade = ""

# --- FLUXO DE TELAS ---

# ETAPA 1: NOME
if st.session_state.step == 1:
    st.title("Team Muniz")
    st.subheader("Consultoria & Treinamento")
    nome_input = st.text_input("Informe seu nome completo:", value=st.session_state.nome)
    if st.button("PRÓXIMO >"):
        if nome_input:
            st.session_state.nome = nome_input.strip()
            st.session_state.step = 2
            st.rerun()
        else: st.error("O nome é obrigatório.")

# ETAPA 2: MODALIDADE
elif st.session_state.step == 2:
    st.title("O que vamos treinar?")
    opcoes = ["Treino Presencial", "Consultoria On-line", "Avaliação Bioimpedância"]
    idx = opcoes.index(st.session_state.modalidade) if st.session_state.modalidade in opcoes else 0
    st.session_state.modalidade = st.selectbox("Selecione a modalidade:", opcoes, index=idx)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("PRÓXIMO >"):
            st.session_state.step = 3
            st.rerun()

# ETAPA 3: TERMOS
elif st.session_state.step == 3:
    st.title("Termos do Time")
    st.markdown('<div class="card"><b>Regras do Time:</b><br>- Tolerância: 20 min.<br>- Cancelamento: 24h.<br>- O horário escolhido na próxima tela é o que vale.</div>', unsafe_allow_html=True)
    
    aceito = st.checkbox("Eu concordo com as regras")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 2; st.rerun()
    with col2:
        if st.button("FINALIZAR >"):
            if aceito:
                st.session_state.step = 4
                st.rerun()
            else: st.warning("Aceite os termos para continuar.")

# ETAPA 4: REDIRECIONAMENTO E WHATSAPP
elif st.session_state.step == 4:
    st.balloons()
    st.title("Tudo Pronto!")
    
    st.markdown('<div class="aviso-urgente">⚠️ PREENCHA SEU NOME NA PRÓXIMA TELA!</div>', unsafe_allow_html=True)
    
    st.write("Copie seu nome para usar no agendamento:")
    st.markdown(f'<div class="caixa-nome">{st.session_state.nome}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
    <b>Instruções Finais:</b><br>
    1. Clique no botão abaixo para abrir minha agenda.<br>
    2. <b>Selecione o(s) dia(s) e horário(s)</b> que deseja.<br>
    3. Digite seu nome e e-mail para confirmar.<br>
    4. Me avise no WhatsApp ao terminar.
    </div>
    """, unsafe_allow_html=True)

    st.link_button("📅 ABRIR AGENDA E ESCOLHER HORÁRIOS", LINK_AGENDA_REAL)

    st.write("---")
    msg_zap = f"Olá Fábio, aqui é o {st.session_state.nome}. Já acessei sua grade para agendar {st.session_state.modalidade}. Vou escolher os melhores horários agora!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg_zap)}")

    if st.button("RECOMEÇAR"):
        st.session_state.step = 1
        st.session_state.nome = ""
        st.rerun()
