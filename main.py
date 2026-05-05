import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

# 1. IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento Direto", layout="centered", page_icon="📅")

# E-mail da sua agenda onde o compromisso deve aparecer
MEU_EMAIL_AGENDA = "fabiomuniz.personal@gmail.com" 
MEU_WHATSAPP = "5511987913509"

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
    .card { background-color: #111111; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ALUNOS FIXOS
ALUNOS_FIXOS = {
    "tathyanne": "11:30", "taina": "11:30", "vanderleia lucena": "15:00",
    "cleiia caroline": "18:00", "guilherme": "20:30", "thaina sena": "20:30"
}

if 'step' not in st.session_state:
    st.session_state.step = 1

# Função para gerar o link que injeta o evento na sua agenda
def criar_link_direto_agenda(nome, modalidade, data_dt, hora_str):
    try:
        h, m = map(int, hora_str.split(':'))
        data_inicio = datetime.combine(data_dt, datetime.min.time()).replace(hour=h, minute=m)
        data_fim = data_inicio + timedelta(hours=1)
        
        fmt = "%Y%m%dT%H%M%SZ"
        titulo = urllib.parse.quote(f"{modalidade.upper()}: {nome.upper()}")
        detalhes = urllib.parse.quote(f"Agendamento via App Team Muniz\nAluno: {nome}")
        
        # O segredo está no parâmetro 'add': ele convida seu e-mail direto
        return f"https://www.google.com/calendar/render?action=TEMPLATE&text={titulo}&dates={data_inicio.strftime(fmt)}/{data_fim.strftime(fmt)}&details={detalhes}&add={MEU_EMAIL_AGENDA}&sf=true&output=xml"
    except:
        return "#"

# --- FLUXO DE TELAS ---

if st.session_state.step == 1:
    st.title("Sistema de Injeção de Agenda")
    nome = st.text_input("Nome do Aluno:", placeholder="Ex: Fábio Muniz")
    if st.button("Avançar"):
        if nome:
            st.session_state.nome = nome.strip()
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.title("Detalhes do Treino")
    modalidade = st.selectbox("Modalidade:", ["Treino Presencial", "Consultoria On-line", "Avaliação"])
    
    nome_min = st.session_state.nome.lower()
    horario_sugerido = next((h for n, h in ALUNOS_FIXOS.items() if n in nome_min), "08:00")
    
    data = st.date_input("Data do Treino:", min_value=datetime.now().date())
    horario = st.text_input("Horário (Fração):", value=horario_sugerido)
    
    if st.button("Confirmar e Gerar Compromisso"):
        st.session_state.modalidade = modalidade
        st.session_state.data_final = data
        st.session_state.horario_final = horario
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.title("Finalizar Agendamento")
    st.write(f"Aluno: **{st.session_state.nome}**")
    st.write(f"Horário: **{st.session_state.horario_final}**")
    
    link_agenda = criar_link_direto_agenda(
        st.session_state.nome, 
        st.session_state.modalidade, 
        st.session_state.data_final, 
        st.session_state.horario_final
    )
    
    st.markdown(f"""
    <div class="card">
    Para que o treino apareça na minha agenda agora, você deve clicar no botão abaixo e confirmar o salvamento.
    </div>
    """, unsafe_allow_html=True)
    
    # Este botão abre a agenda já com seu e-mail como convidado obrigatório
    st.link_button("✅ INJETAR NA AGENDA DO COACH", link_agenda)
    
    st.write("---")
    resumo_wpp = f"Fábio, agendei meu treino de {st.session_state.modalidade} para o dia {st.session_state.data_final.strftime('%d/%m/%Y')} às {st.session_state.horario_final}. Já deve aparecer na sua agenda!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(resumo_wpp)}")
