import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

MEU_EMAIL_AGENDA = "fabiomuniz.personal@gmail.com" # Ajuste para o e-mail da sua agenda Google
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

# ETAPA 1: IDENTIFICAÇÃO
if st.session_state.step == 1:
    st.markdown('<p class="step-text">Etapa 1</p>', unsafe_allow_html=True)
    st.title("Quem está agendando?")
    nome = st.text_input("Nome Completo *", placeholder="Digite seu nome...")
    if st.button("Próximo >"):
        if nome:
            st.session_state.nome = nome.strip()
            proximo_passo()
            st.rerun()
        else: st.error("O nome é obrigatório.")

# ETAPA 2: MODALIDADE
elif st.session_state.step == 2:
    st.markdown('<p class="step-text">Etapa 2</p>', unsafe_allow_html=True)
    st.title("Tipo de Atendimento")
    modalidade = st.selectbox("Selecione *", [
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

# ETAPA 3: DATA E FRAÇÃO DE HORÁRIO
elif st.session_state.step == 3:
    st.markdown('<p class="step-text">Etapa 3</p>', unsafe_allow_html=True)
    st.title("Data e Horário")
    
    # Lógica de Horário Fixo
    nome_min = st.session_state.nome.lower()
    horario_sugerido = next((h for n, h in ALUNOS_FIXOS.items() if n in nome_min), "08:00")
    
    st.write("Escolha os dias das suas aulas (até 3 dias):")
    d1 = st.date_input("Aula 1", min_value=datetime.now().date(), key="d1")
    d2 = st.date_input("Aula 2", min_value=datetime.now().date(), key="d2")
    d3 = st.date_input("Aula 3", min_value=datetime.now().date(), key="d3")
    
    horario = st.text_input("Horário das Aulas (Fixo ou Fração)", value=horario_sugerido)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Próximo >"):
            st.session_state.datas = [d1, d2, d3]
            st.session_state.horario = horario
            proximo_passo()
            st.rerun()

# ETAPA 4: TERMOS E ACEITE
elif st.session_state.step == 4:
    st.markdown('<p class="step-text">Etapa 4</p>', unsafe_allow_html=True)
    st.title("Termos e Confirmação")
    st.markdown("""
    <div class="card">
    <b>Termos e Condições</b><br>
    - Tolerância de 20 min.<br>
    - Cancelamento com 24h.<br>
    - O agendamento será enviado como convite para a agenda do Coach Muniz.
    </div>
    """, unsafe_allow_html=True)
    aceito = st.checkbox("Eu concordo e quero enviar o convite para a agenda do Coach")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Finalizar Agendamento"):
            if aceito: proximo_passo(); st.rerun()
            else: st.warning("Aceite os termos.")

# ETAPA 5: ENVIO DO INVITE (AÇÃO PARA SUA AGENDA)
elif st.session_state.step == 5:
    st.balloons()
    st.title("Enviar para Agenda")
    st.write(f"Tudo pronto, **{st.session_state.nome}**! Agora clique no botão abaixo para gerar o convite oficial na agenda do Fábio.")
    
    # Criar o corpo do e-mail de invite
    corpo_email = (f"Solicitação de Agendamento - Team Muniz\n\n"
                   f"Aluno: {st.session_state.nome}\n"
                   f"Modalidade: {st.session_state.modalidade}\n"
                   f"Horário: {st.session_state.horario}\n"
                   f"Datas solicitadas:\n")
    
    for d in st.session_state.datas:
        corpo_email += f"- {d.strftime('%d/%m/%Y')}\n"
        
    assunto = f"INVITE: {st.session_state.modalidade.upper()} - {st.session_state.nome.upper()}"
    mailto_link = f"mailto:{MEU_EMAIL_AGENDA}?subject={urllib.parse.quote(assunto)}&body={urllib.parse.quote(corpo_email)}"
    
    st.markdown(f"""
    <div class="card" style="border-color: #D4AF37;">
    <b>Importante:</b> Ao clicar no botão, seu aplicativo de e-mail abrirá. Basta clicar em 'Enviar' para que o Fábio receba e confirme na agenda dele.
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("📧 ENVIAR INVITE PARA O COACH", mailto_link)
    
    st.write("---")
    # Backup via WhatsApp
    resumo_zap = f"Fábio, acabei de enviar os invites por e-mail para as aulas de {st.session_state.modalidade}!"
    st.link_button("📱 AVISAR NO WHATSAPP", f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(resumo_zap)}")

    if st.button("Novo Agendamento"):
        st.session_state.step = 1
        st.rerun()
