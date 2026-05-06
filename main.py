import streamlit as st
import urllib.parse

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"

# BANCO DE DATA DOS ALUNOS FIXOS ATUALIZADO
ALUNOS_FIXOS = {
    "Tathyane Oyarce e Tainá Oyarce": "11:30",
    "Vanderleia Lucena": "15:00",
    "Cleiia Caroline": "18:00",
    "Thainá Sena & Guilherme Jeronymo": "20:30"
}

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
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE ESTADO
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'horario' not in st.session_state: st.session_state.horario = ""

# --- FLUXO DE TELAS ---

# ETAPA 1: RECONHECIMENTO DO ALUNO
if st.session_state.step == 1:
    st.title("Team Muniz")
    st.subheader("Identificação")
    
    opcao_nome = st.selectbox("Selecione seu nome:", ["Clique para selecionar"] + list(ALUNOS_FIXOS.keys()) + ["Outro (Novo Aluno)"])
    
    if st.button("PRÓXIMO >"):
        if opcao_nome != "Clique para selecionar":
            st.session_state.nome = opcao_nome
            st.session_state.horario = ALUNOS_FIXOS.get(opcao_nome, "Sob consulta")
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Selecione uma opção para continuar.")

# ETAPA 2: CONFIRMAÇÃO DE HORÁRIO
elif st.session_state.step == 2:
    st.title("Confirmação de Horário")
    st.write(f"Olá, **{st.session_state.nome}**.")
    
    st.markdown(f"""
    <div class="card">
    Seu horário fixo registrado é: <br>
    <span style="font-size: 24px; color: #D4AF37;"><b>{st.session_state.horario}</b></span>
    <br><br>Deseja confirmar este horário para seu agendamento?
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("SIM, CONFIRMAR >"):
            st.session_state.step = 3
            st.rerun()

# ETAPA 3: TERMOS
elif st.session_state.step == 3:
    st.title("Termos do Time")
    st.markdown("""
    <div class="card">
    <b>Regras Team Muniz:</b><br><br>
    • <b>Tolerância de atraso: 10 minutos.</b><br>
    • Cancelamento: Mínimo de 24h de antecedência.<br>
    • O agendamento só é oficial após conclusão na agenda do Google.
    </div>
    """, unsafe_allow_html=True)
    
    aceito = st.checkbox("Concordo com os termos e regras")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 2; st.rerun()
    with col2:
        if st.button("FINALIZAR >"):
            if aceito:
                st.session_state.step = 4
                st.rerun()
            else: st.warning("Aceite os termos para prosseguir.")

# ETAPA 4: AGENDA
elif st.session_state.step == 4:
    st.title("Finalizar na Agenda")
    
    st.write("Identificação para preencher no Google:")
    st.markdown(f'<div class="caixa-nome">{st.session_state.nome}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
    <b>Como proceder:</b><br>
    1. Clique no botão abaixo para abrir a grade.<br>
    2. Escolha o horário (**{st.session_state.horario}**) na data desejada.<br>
    3. Digite seu nome e e-mail para validar.
    </div>
    """, unsafe_allow_html=True)

    st.link_button("📅 ABRIR AGENDA DO COACH", LINK_AGENDA_REAL)

    st.write("---")
    msg_zap = f"Olá Fábio, sou {st.session_state.nome}. Confirmei meus dados e estou agendando meu horário de {st.session_state.horario} na sua grade oficial!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg_zap)}")

    if st.button("RECOMEÇAR"):
        st.session_state.step = 1
        st.rerun()
