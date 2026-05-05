import streamlit as st
import urllib.parse

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"

# 2. BANCO DE DADOS DE ALUNOS FIXOS (RECONHECIMENTO)
ALUNOS_FIXOS = [
    "tathyanne", "taina", "vanderleia lucena", 
    "cleiia caroline", "guilherme", "thaina sena"
]

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
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZAÇÃO DE ESTADO
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""

# --- FLUXO DE TELAS ---

# ETAPA 1: RECONHECIMENTO DE ALUNO
if st.session_state.step == 1:
    st.title("Team Muniz")
    st.subheader("Área de Agendamento")
    
    nome_input = st.text_input("Informe seu nome completo:", value=st.session_state.nome)
    
    if st.button("VALIDAR ACESSO >"):
        if nome_input:
            nome_valido = nome_input.strip().lower()
            # Validação: verifica se o nome digitado contém algum dos nomes da lista de fixos
            if any(fixo in nome_valido for fixo in ALUNOS_FIXOS):
                st.success(f"Acesso validado: Bem-vindo de volta, Aluno(a) Fixo!")
            else:
                st.info("Acesso validado como novo aluno/visitante.")
            
            st.session_state.nome = nome_input.strip()
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Por favor, digite seu nome.")

# ETAPA 2: TERMOS E REGRAS (TOLERÂNCIA 10 MIN)
elif st.session_state.step == 2:
    st.title("Termos do Time")
    st.markdown(f"""
    <div class="card">
    <b>Regras Oficiais - Coach Muniz:</b><br><br>
    • <b>Tolerância de atraso: 10 minutos.</b><br>
    • Cancelamento: Mínimo de 24h de antecedência.<br>
    • O agendamento só é oficial após conclusão na agenda do Google.
    </div>
    """, unsafe_allow_html=True)
    
    aceito = st.checkbox("Eu li e concordo com os termos")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< VOLTAR"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("FINALIZAR >"):
            if aceito:
                st.session_state.step = 3
                st.rerun()
            else: st.warning("Aceite os termos para continuar.")

# ETAPA 3: REDIRECIONAMENTO FINAL
elif st.session_state.step == 3:
    st.balloons()
    st.title("Tudo Pronto!")
    
    st.markdown('<div class="aviso-urgente">⚠️ NÃO ESQUEÇA DE PREENCHER SEU NOME!</div>', unsafe_allow_html=True)
    
    st.write("Identificação para a agenda:")
    st.markdown(f'<div class="caixa-nome">{st.session_state.nome}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
    <b>Instruções:</b><br>
    1. Clique no botão dourado abaixo para abrir a agenda oficial.<br>
    2. Escolha o horário disponível.<br>
    3. Digite seu nome e e-mail no formulário do Google.<br>
    4. Confirme seu agendamento.
    </div>
    """, unsafe_allow_html=True)

    st.link_button("📅 ABRIR AGENDA E ESCOLHER HORÁRIO", LINK_AGENDA_REAL)

    st.write("---")
    msg_zap = f"Olá Fábio, aqui é o {st.session_state.nome}. Já validei meus dados e estou escolhendo o melhor horário na sua agenda agora!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg_zap)}")

    if st.button("NOVO AGENDAMENTO"):
        st.session_state.step = 1
        st.session_state.nome = ""
        st.rerun()
