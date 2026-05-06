import streamlit as st
import urllib.parse
import base64

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"

# BANCO DE DADOS DOS ALUNOS FIXOS
ALUNOS_FIXOS = {
    "Tathyane Oyarce e Tainá Oyarce": "11:30",
    "Vanderleia Lucena": "15:00",
    "Cleiia Caroline": "18:00",
    "Thainá Sena & Guilherme Jeronymo": "20:30"
}

# INICIALIZAÇÃO SEGURA DE TODAS AS VARIÁVEIS (Evita o erro AttributeError)
if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'horario' not in st.session_state: st.session_state.horario = ""
if 'modalidade' not in st.session_state: st.session_state.modalidade = "Treino Presencial"
if 'is_fixo' not in st.session_state: st.session_state.is_fixo = False

# FUNÇÃO PARA CARREGAR IMAGEM LOCAL COMO FUNDO
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

img_base64 = get_base64_image("5f31ca7e-881e-4d36-9ef3-215284a5f651 2.jpg")

if img_base64:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
                        url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp { background-color: #000000; }</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
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
    .card { 
        background-color: rgba(17, 17, 17, 0.9); 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #D4AF37; 
        margin-bottom: 15px; 
    }
    .caixa-nome {
        background-color: #D4AF37; color: black; padding: 15px;
        border-radius: 8px; text-align: center; font-size: 22px; font-weight: bold; margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FLUXO DE TELAS ---

# ETAPA 1: IDENTIFICAÇÃO
if st.session_state.step == 1:
    st.title("Team Muniz")
    st.subheader("Bem-vindo")
    
    opcao_nome = st.selectbox("Identifique-se:", ["Clique para selecionar"] + list(ALUNOS_FIXOS.keys()) + ["Sou um Novo Aluno"])
    
    if st.button("PRÓXIMO >"):
        if opcao_nome != "Clique para selecionar":
            if opcao_nome == "Sou um Novo Aluno":
                st.session_state.is_fixo = False
                st.session_state.step = 1.5
            else:
                st.session_state.is_fixo = True
                st.session_state.nome = opcao_nome
                st.session_state.horario = ALUNOS_FIXOS[opcao_nome]
                st.session_state.step = 2
            st.rerun()

# ETAPA 1.5: CADASTRO NOVO ALUNO
elif st.session_state.step == 1.5:
    st.title("Novo Aluno")
    nome_novo = st.text_input("Digite seu nome completo:")
    if st.button("CONFIRMAR NOME >"):
        if nome_novo:
            st.session_state.nome = nome_novo.strip()
            st.session_state.step = 2.5
            st.rerun()

# ETAPA 2: CONFIRMAÇÃO ALUNO FIXO
elif st.session_state.step == 2:
    st.title("Confirmar Horário")
    st.markdown(f'<div class="card">Olá <b>{st.session_state.nome}</b>, seu horário fixo é <b>{st.session_state.horario}</b>.</div>', unsafe_allow_html=True)
    if st.button("SIM, CONFIRMAR >"):
        st.session_state.step = 2.5
        st.rerun()
    if st.button("< VOLTAR"): st.session_state.step = 1; st.rerun()

# ETAPA 2.5: MODALIDADE
elif st.session_state.step == 2.5:
    st.title("Modalidade")
    modalidade_escolhida = st.selectbox("O que vamos treinar?", ["Treino Presencial", "Consultoria On-line", "Avaliação Bioimpedância"])
    if st.button("PRÓXIMO >"):
        st.session_state.modalidade = modalidade_escolhida
        st.session_state.step = 3
        st.rerun()

# ETAPA 3: TERMOS (TOLERÂNCIA 10 MIN)
elif st.session_state.step == 3:
    st.title("Termos do Time")
    st.markdown("""
    <div class="card">
    <b>Regras Oficiais:</b><br><br>
    • <b>Tolerância de atraso: 10 minutos.</b><br>
    • Cancelamento: Mínimo de 24h de antecedência.
    </div>
    """, unsafe_allow_html=True)
    if st.checkbox("Li e concordo com os termos"):
        if st.button("IR PARA AGENDA >"):
            st.session_state.step = 4
            st.rerun()

# ETAPA 4: AGENDA
elif st.session_state.step == 4:
    st.title("Finalizar Agendamento")
    st.write("Preencha este nome no Google:")
    st.markdown(f'<div class="caixa-nome">{st.session_state.nome}</div>', unsafe_allow_html=True)
    st.link_button("📅 ABRIR AGENDA DO COACH", LINK_AGENDA_REAL)
    
    st.write("---")
    # Agora a modalidade está garantida no estado
    msg = f"Olá Fábio, sou {st.session_state.nome}. Agendei {st.session_state.modalidade} na sua grade!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg)}")
    
    if st.button("RECOMEÇAR"):
        st.session_state.step = 1
        st.session_state.nome = ""
        st.rerun()
