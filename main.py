import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO E IDENTIDADE VISUAL TEAM MUNIZ
st.set_page_config(page_title="Team Muniz - Agendamento", layout="centered", page_icon="📅")

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
        border: none;
    }
    .step-text { color: #D4AF37; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .card { background-color: #111111; padding: 25px; border-radius: 15px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS E LÓGICA
ALUNOS_FIXOS = {
    "tathyanne": "11:30", "taina": "11:30", "vanderleia lucena": "15:00",
    "cleiia caroline": "18:00", "guilherme": "20:30", "thaina sena": "20:30"
}

if 'step' not in st.session_state:
    st.session_state.step = 1

def proximo_passo():
    st.session_state.step += 1

def voltar_passo():
    st.session_state.step -= 1

# 3. FLUXO POR ETAPAS
st.image("https://images.squarespace-cdn.com/content/v1/5f4d3d8f5d0f6a2a0f8b8a8b/1602111244036-XJ0Z7Z7Z7Z7Z7Z7Z7Z7Z/Logo+Team+Muniz.png", width=120)

# ETAPA 1: NOME
if st.session_state.step == 1:
    st.markdown('<p class="step-text">Etapa 1</p>', unsafe_allow_html=True)
    st.title("Qual é seu nome?")
    st.write("Digite seu nome para verificar se você é aluno fixo.")
    
    nome = st.text_input("Nome Completo *", key="nome_input", placeholder="Digite seu nome...")
    
    if st.button("Próximo >"):
        if nome:
            st.session_state.nome = nome.strip()
            proximo_passo()
            st.rerun()
        else:
            st.error("Por favor, digite seu nome.")

# ETAPA 2: MODALIDADE
elif st.session_state.step == 2:
    st.markdown('<p class="step-text">Etapa 2</p>', unsafe_allow_html=True)
    st.title("O que vamos agendar?")
    
    modalidade = st.selectbox("Selecione a modalidade *", [
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

# ETAPA 3: DATA E HORÁRIO (Lógica de Aluno Fixo)
elif st.session_state.step == 3:
    st.markdown('<p class="step-text">Etapa 3</p>', unsafe_allow_html=True)
    st.title("Data e Horário")
    
    nome_min = st.session_state.nome.lower()
    horario_fixo = next((h for n, h in ALUNOS_FIXOS.items() if n in nome_min), None)
    
    if horario_fixo:
        st.success(f"Identificamos que você é aluno fixo! Seu horário é às {horario_fixo}.")
        st.session_state.horario = horario_fixo
        st.session_state.is_fixo = True
    else:
        st.info("Escolha uma data para enviarmos sua solicitação.")
        st.session_state.is_fixo = False
        st.session_state.horario = "A definir na agenda"

    data = st.date_input("Selecione a data", min_value=datetime.now().date())
    st.session_state.data = data.strftime("%d/%m/%Y")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Próximo >"): proximo_passo(); st.rerun()

# ETAPA 4: TERMOS E CONDIÇÕES
elif st.session_state.step == 4:
    st.markdown('<p class="step-text">Etapa 4</p>', unsafe_allow_html=True)
    st.title("Termos e Condições")
    
    st.markdown("""
    <div class="card">
    <b>Tolerância de Atraso</b><br>
    Atrasos serão abatidos do tempo da aula com tolerância de até 20 minutos. Após este período, o agendamento pode ser cancelado sem custos.<br><br>
    <b>Cancelamento</b><br>
    Cancelamento com no mínimo 24h de antecedência.<br><br>
    <b>Confirmação</b><br>
    Confirmação do agendamento será enviada via WhatsApp.
    </div>
    """, unsafe_allow_html=True)
    
    aceito = st.checkbox("Eu concordo com todos os termos e condições acima descritos")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("< Voltar"): voltar_passo(); st.rerun()
    with col2:
        if st.button("Finalizar"):
            if aceito:
                proximo_passo()
                st.rerun()
            else:
                st.warning("Você precisa aceitar os termos para continuar.")

# ETAPA 5: CONFIRMAÇÃO
elif st.session_state.step == 5:
    st.balloons()
    st.title("Quase lá!")
    st.write(f"Tudo pronto, **{st.session_state.nome}**! Clique abaixo para finalizar seu agendamento de **{st.session_state.modalidade}**.")
    
    # Gerar links
    resumo = (f"*AGENDAMENTO TEAM MUNIZ*\n\n"
              f"👤 *Nome:* {st.session_state.nome}\n"
              f"🎯 *Modalidade:* {st.session_state.modalidade}\n"
              f"📅 *Data:* {st.session_state.data}\n"
              f"⏰ *Horário:* {st.session_state.horario}")
    
    link_zap = f"https://wa.me/{MEU_WHATSAPP}?text={urllib.parse.quote(resumo)}"
    
    st.link_button("🚀 FINALIZAR E AVISAR NO WHATSAPP", link_zap)
    
    if not st.session_state.get('is_fixo'):
        st.write("---")
        st.write("Se você não for aluno fixo, escolha seu horário exato aqui:")
        st.link_button("📅 ABRIR AGENDA GOOGLE", "https://calendar.app.google/YGhyV7GK38tuBBtv8")

    if st.button("Novo Agendamento"):
        st.session_state.step = 1
        st.rerun()
