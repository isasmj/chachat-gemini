import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import time

# Configuração da página
st.set_page_config(
    page_title=" Assistente VituMiau",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Carrega variáveis de ambiente
load_dotenv()

def get_api_key():
    return os.getenv('GEMINI_API_KEY')

def main():
    # Configuração do tema com efeitos especiais
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;800&family=Poppins:wght@300;500;700&display=swap');
    
    /* Fundo mágico com overlay */
    .stApp {
        background: linear-gradient(rgba(255, 240, 245, 0.9), rgba(255, 240, 245, 0.9)), 
                    url('https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdm95ZjdkbG10ZDhzenRzcmx6OXVoNmx3bXN5dmoya3JlN3NsejBnaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ov9jHiEzknijxAD3q/giphy.gif') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Poppins', sans-serif;
        min-height: 100vh;
    }
    
    /* Container principal */
    .magic-container {
        backdrop-filter: blur(8px);
    
        position: relative;
        overflow: hidden;
    }
    
    /* Efeito de brilho */
    .magic-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Título animado */
    .magic-title {
        font-family: 'Baloo 2', cursive;
        color: #ff3e8a;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 1rem;
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .magic-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 25%;
        width: 50%;
        height: 4px;
        background: linear-gradient(90deg, transparent, #ff6b9e, transparent);
        animation: titleUnderline 3s ease-in-out infinite;
    }
    
    @keyframes titleUnderline {
        0%, 100% { transform: scaleX(0.8); opacity: 0.7; }
        50% { transform: scaleX(1.2); opacity: 1; }
    }
    
    /* Subtítulo pulsante */
    .magic-subtitle {
        font-size: 1.5rem;
        color: #ff6b9e;
        text-align: center;
        margin-bottom: 2rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Área de texto com efeito */
    .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #ff9ec6 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 5px 25px rgba(255, 105, 180, 0.2) !important;
        transition: all 0.3s !important;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #ff3e8a !important;
        box-shadow: 0 5px 30px rgba(255, 62, 138, 0.4) !important;
    }
    
    /* Botão mágico */
    .stButton>button {
        background: linear-gradient(45deg, #ff3e8a, #ff6b9e) !important;
        color: white !important;
        border: none !important;
        padding: 16px 32px !important;
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s !important;
        width: 100% !important;
        box-shadow: 0 5px 25px rgba(255, 62, 138, 0.3) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(255, 62, 138, 0.5) !important;
    }
    
    .stButton>button::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: rgba(255, 255, 255, 0.1);
        transform: rotate(45deg);
        animation: buttonShine 3s ease-in-out infinite;
    }
    
    @keyframes buttonShine {
        0% { left: -100%; }
        20%, 100% { left: 100%; }
    }
    
    /* Avatar flutuante */
    .magic-avatar {
        width: 200px;
        height: 200px;
        margin: 0 auto 30px;
        border-radius: 50%;
        overflow: hidden;
        border: 6px solid white;
        box-shadow: 0 15px 40px rgba(255, 105, 180, 0.4);
        animation: float 6s ease-in-out infinite;
        position: relative;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    /* Resposta animada */
    .magic-response {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 30px;
        margin-top: 30px;
        border-left: 10px solid #ff3e8a;
        box-shadow: 0 15px 40px rgba(255, 105, 180, 0.2);
        font-size: 1.1rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Texto da resposta */
    .response-text {
        color: #555;
        line-height: 1.8;
        font-size: 1.2rem;
        position: relative;
    }
    
    .response-text::first-letter {
        font-size: 2rem;
        color: #ff3e8a;
        float: left;
        margin-right: 5px;
        line-height: 1;
    }
    
    /* Efeito de digitação */
    .typing-effect {
        display: inline-block;
        overflow: hidden;
        border-right: 3px solid #ff6b9e;
        white-space: nowrap;
        animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #ff6b9e }
    }
    
    /* Responsivo */
    @media (max-width: 768px) {
        .magic-container {
            padding: 1.5rem;
        }
        
        .magic-title {
            font-size: 2rem;
        }
        
        .magic-subtitle {
            font-size: 1.2rem;
        }
        
        .magic-avatar {
            width: 150px;
            height: 150px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Container mágico
    st.markdown('<div class="magic-container">', unsafe_allow_html=True)

    # Avatar animado
    st.markdown("""
    <div class="magic-avatar">
        <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExanFxbjJ3dHdnMnF6OXdyczgweXNwdzMydWhuanU5Nm53N2lma3ZwcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JIX9t2j0ZTN9S/giphy.gif" width="200" height="200" alt="Gato Mágico">
    </div>
    """, unsafe_allow_html=True)

    # Título animado
    st.markdown('<h1 class="magic-title">Assistente VirtuMiau</h1>', unsafe_allow_html=True)
    st.markdown('<p class="magic-subtitle">Seu ajudante felino</p>', unsafe_allow_html=True)

    # Input do usuário
    user_prompt = st.text_area(
        "O que você gostaria de saber hoje? 😽",
        height=150,
        placeholder="Digite sua pergunta  aqui...",
        key="user_input"
    )

    # Botão de envio
    if st.button("✨ OBTER RESPOSTA ") and user_prompt:
        with st.spinner("O gatinho está consultando os astros..."):
            try:
                # Configuração do Gemini
                genai.configure(api_key=get_api_key())
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # Geração da resposta
                response = model.generate_content(user_prompt)
                
                # Efeito de digitação simulado
                response_placeholder = st.empty()
                full_text = response.text
                typed_text = ""
                
                for i in range(len(full_text) + 1):
                    typed_text = full_text[:i]
                    response_placeholder.markdown(f"""
                    <div class="magic-response">
                        <h3 style="color: #ff3e8a; margin-top: 0;">RESPOSTA :</h3>
                        <div class="response-text">
                            {typed_text.replace('•', '✨')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.02)  # Ajuste a velocidade aqui
                
                # Mantém o texto completo após a animação
                response_placeholder.markdown(f"""
                <div class="magic-response">
                    <h3 style="color: #ff3e8a; margin-top: 0;">RESPOSTA :</h3>
                    <div class="response-text">
                        {full_text.replace('•', '✨')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"🧙‍♂️ O feitiço falhou: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()