import streamlit as st
import urllib.parse

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"

# BANCO DE DADOS DE ALUNOS FIXOS PARA SUGESTÃO/VALIDAÇÃO
ALUNOS_FIXOS = [
    "Tathyanne", "Taina", "Vanderleia Lucena", 
    "Cleiia Caroline", "Guilherme", "Thaina Sena"
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
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE ESTADO
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'modalidade' not in st.session_state: st.session_state.modalidade = ""

# --- FLUXO DE TELAS ---

# ETAPA 1: NOME E MODALIDADE
if st.session_state.step == 1:
    st.title("Team Muniz")
    st.subheader("Identificação")
    
    # Sugestão para alunos fixos e entrada de texto
    nome_input = st.selectbox("Se você é aluno fixo, selecione seu nome:", [""] + ALUNOS_FIXOS)
    if not nome_input:
        nome_input = st.text_input("Ou digite seu nome completo:", value=st.session_state.nome)
    
    st.write("---")
    opcoes_mod = ["Treino Presencial", "Consultoria On-line", "Avaliação Bioimpedância"]
    st.session_state.modalidade = st.selectbox("Selecione a modalidade:", opcoes_mod)
    
    if st.button("PRÓXIMO >"):
        if nome_input:
            st.session_state.nome = nome_input.strip()
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Por favor, identifique-se para continuar.")

# ETAPA 2: TERMOS COM ACEITE
elif st.session_state.step == 2:
    st.title("Termos e Regras")
    st.markdown(f"""
    <div class="card">
    <b>Regras Oficiais Team Muniz:</b><br><br>
    • <b>Tolerância de atraso: 10 minutos.</b><br>
    • Cancelamento: Mínimo de 24h de antecedência.<br>
    • O agendamento só é oficial após a conclusão na agenda do Google.
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
            else: st.warning("Aceite os termos para liberar a agenda.")

# ETAPA 3: REDIRECIONAMENTO PARA AGENDA
elif st.session_state.step == 3:
    st.balloons()
    st.title("Acesse a Agenda")
    
    st.write("Ao abrir o link, preencha seu nome exatamente assim:")
    st.markdown(f'<div class="caixa-nome">{st.session_state.nome}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
    <b>Próximos Passos:</b><br>
    1. Clique no botão abaixo para abrir a grade oficial.<br>
    2. Escolha o dia e horário disponível.<br>
    3. Confirme seus dados no formulário do Google.
    </div>
    """, unsafe_allow_html=True)

    st.link_button("📅 ABRIR AGENDA E ESCOLHER HORÁRIO", LINK_AGENDA_REAL)

    st.write("---")
    msg_zap = f"Olá Fábio, aqui é o {st.session_state.nome}. Já validei meus dados e estou agendando {st.session_state.modalidade} agora!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg_zap)}")

    if st.button("NOVO AGENDAMENTO"):
        st.session_state.step = 1
        st.session_state.nome = ""
        st.rerun()
