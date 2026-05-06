import streamlit as st
import urllib.parse
import base64

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_WHATSAPP = "5511987913509"
LINK_AGENDA_REAL = "https://calendar.app.google/49vn5NJ3VTf2sMxq9"
LINK_MAPS = "https://maps.app.goo.gl/SuaLocalizacaoAqui" # Substitua pelo link da sua academia

# BANCO DE DATA ALUNOS FIXOS
ALUNOS_FIXOS = {
    "Tathyane Oyarce e Tainá Oyarce": "11:30",
    "Vanderleia Lucena": "15:00",
    "Cleiia Caroline": "18:00",
    "Thainá Sena & Guilherme Jeronymo": "20:30"
}

# INICIALIZAÇÃO DE ESTADO (MEMORY CLEANUP)
def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if 'step' not in st.session_state: st.session_state.step = 1
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'horario' not in st.session_state: st.session_state.horario = ""
if 'modalidade' not in st.session_state: st.session_state.modalidade = "Treino Presencial"

# FUNDO PERSONALIZADO
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except: return None

img_base64 = get_base64_image("5f31ca7e-881e-4d36-9ef3-215284a5f651 2.jpg")

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url("data:image/jpg;base64,{img_base64 if img_base64 else ''}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    h1, h2, h3 {{ color: #D4AF37 !important; font-weight: bold; }}
    .stMarkdown {{ color: white; }}
    .stButton>button {{
        width: 100%; background-color: #D4AF37 !important;
        color: black !important; font-weight: bold !important;
        height: 50px; border-radius: 8px;
    }}
    .card {{ 
        background-color: rgba(17, 17, 17, 0.9); 
        padding: 20px; border-radius: 12px; 
        border: 1px solid #D4AF37; margin-bottom: 15px; 
    }}
    .alerta-tempo {{ color: #FF4B4B; font-weight: bold; font-size: 14px; }}
    </style>
    """, unsafe_allow_html=True)

# --- FLUXO DE TELAS ---

if st.session_state.step == 1:
    st.title("Team Muniz")
    opcao = st.selectbox("Quem está acessando?", ["Selecione"] + list(ALUNOS_FIXOS.keys()) + ["Novo Aluno"])
    if st.button("PRÓXIMO >"):
        if opcao != "Selecione":
            if opcao == "Novo Aluno": st.session_state.step = 1.5
            else:
                st.session_state.nome = opcao
                st.session_state.horario = ALUNOS_FIXOS[opcao]
                st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 1.5:
    st.title("Seu Nome")
    nome_n = st.text_input("Nome completo:")
    if st.button("CONFIRMAR >"):
        if nome_n: 
            st.session_state.nome = nome_n.strip()
            st.session_state.step = 2.5
            st.rerun()

elif st.session_state.step == 2:
    st.title("Seu Horário")
    st.markdown(f'<div class="card">Confirmamos seu horário fixo: <b>{st.session_state.horario}</b>.</div>', unsafe_allow_html=True)
    if st.button("SIM, ESTÁ CORRETO >"):
        st.session_state.step = 2.5
        st.rerun()
    if st.button("< VOLTAR"): st.session_state.step = 1; st.rerun()

elif st.session_state.step == 2.5:
    st.title("Modalidade")
    st.session_state.modalidade = st.selectbox("Tipo de treino:", ["Treino Presencial", "Consultoria On-line", "Avaliação Bioimpedância"])
    if st.button("AVANÇAR >"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.title("Regras de Ouro")
    st.markdown(f"""
    <div class="card">
    <p class="alerta-tempo">⏱️ TOLERÂNCIA: 10 MINUTOS IMPRETERÍVEIS.</p>
    • Se seu treino é às 15:00, o limite de entrada é 15:10.<br>
    • Cancelamentos devem ser feitos com 24h de antecedência.
    </div>
    """, unsafe_allow_html=True)
    if st.checkbox("Li e estou ciente da regra de tolerância"):
        if st.button("IR PARA AGENDA >"):
            st.session_state.step = 4
            st.rerun()

elif st.session_state.step == 4:
    st.title("Etapa Final")
    titulo = f"Team Muniz + {st.session_state.nome} + {st.session_state.modalidade}"
    
    st.write("1️⃣ Clique no ícone abaixo para copiar o título:")
    st.code(titulo, language=None)
    
    st.markdown(f"""
    <div class="card">
    <b>Como finalizar:</b><br>
    • No formulário da agenda, cole o texto acima no campo <b>'Nome'</b>.<br>
    • Use o <b>e-mail cadastrado</b> no seu plano.<br>
    {"• 📍 Se precisar da localização, veja no botão abaixo." if st.session_state.modalidade == "Treino Presencial" else ""}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.modalidade == "Treino Presencial":
        st.link_button("📍 VER LOCALIZAÇÃO NO MAPS", LINK_MAPS)
        st.write("")

    st.link_button("📅 ABRIR GRADE DE HORÁRIOS", LINK_AGENDA_REAL)
    
    st.write("---")
    msg = f"Fábio, agendamento de {st.session_state.modalidade} iniciado por {st.session_state.nome}!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(msg)}")
    
    if st.button("SAIR / RECOMEÇAR"): reset_session()
