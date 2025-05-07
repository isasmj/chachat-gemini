import streamlit as st
from PIL import Image
import io
import requests
from datetime import datetime
from googletrans import Translator
import base64

# URL do GIF animado para o avatar
GIF_AVATAR_URL = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExanFxbjJ3dHdnMnF6OXdyczgweXNwdzMydWhuanU5Nm53N2lma3ZwcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JIX9t2j0ZTN9S/giphy.gif"

# Configuração da página com estilo mágico
st.set_page_config(
    page_title="Magic Image Generator - Stability AI",
    page_icon=GIF_AVATAR_URL,
    layout="wide"
)

# CSS personalizado com tema mágico
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
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #ff9ec6 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 5px 25px rgba(255, 105, 180, 0.2) !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #ff3e8a !important;
        box-shadow: 0 5px 30px rgba(255, 62, 138, 0.4) !important;
    }
    
    /* Botão mágico */
    .stButton>button {
        background: linear-gradient(45deg, #ff3e8a, #ff6b9e) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s !important;
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
    
    /* Imagem gerada com estilo */
    .generated-image {
        border-radius: 20px;
        border: 5px solid white;
        box-shadow: 0 15px 40px rgba(255, 105, 180, 0.3);
        margin: 20px 0;
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar estilizada */
    [data-testid="stSidebar"] {
        background: rgba(255, 240, 245, 0.85) !important;
        backdrop-filter: blur(8px) !important;
        border-right: 1px solid rgba(255, 182, 193, 0.3) !important;
    }
    
    /* Sliders estilizados */
    .stSlider .thumb {
        background: #ff3e8a !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 10px rgba(255, 62, 138, 0.3) !important;
    }
    
    .stSlider .track {
        background: #ff9ec6 !important;
    }
    
    /* Estilo para o avatar animado */
    .stChatMessage img.avatar {
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ff3e8a;
        box-shadow: 0 0 15px rgba(255, 62, 138, 0.5);
        transition: all 0.3s ease;
    }
    
    .stChatMessage img.avatar:hover {
        transform: scale(1.1);
        box-shadow: 0 0 25px rgba(255, 62, 138, 0.8);
    }
    
    /* Responsivo */
    @media (max-width: 768px) {
        .magic-title {
            font-size: 2rem;
        }
        
        .magic-subtitle {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Dimensões permitidas para SDXL
ALLOWED_DIMENSIONS = [
    (1024, 1024), 
    (1152, 896), (896, 1152),
    (1216, 832), (832, 1216),
    (1344, 768), (768, 1344),
    (1536, 640), (640, 1536)
]

# Sidebar para configurações
with st.sidebar:
    st.title("⚙️ Configurações Mágicas")
    api_key = st.text_input("🔑 Sua Chave da API Stability AI", type="password")
    st.markdown("[Obter chave da API](https://platform.stability.ai/)")
    
    st.divider()
    st.markdown("### 🎛 Parâmetros de Magia")
    cfg_scale = st.slider("✨ Criatividade (CFG Scale)", 1.0, 20.0, 7.0)
    steps = st.slider("🔢 Passos de Encantamento", 10, 150, 30)
    
    # Selecionador de dimensões permitidas
    dimension_options = [f"{w}×{h}" for w, h in ALLOWED_DIMENSIONS]
    selected_dim = st.selectbox("📏 Dimensões do Feitiço", dimension_options, index=0)
    width, height = map(int, selected_dim.split('×'))
    
    sampler = st.selectbox("🧙‍♂️ Método de Conjuração", [
        "DDIM", "DDPM", "K_DPMPP_2M", "K_DPMPP_2S_ANCESTRAL", 
        "K_DPM_2", "K_DPM_2_ANCESTRAL", "K_EULER", 
        "K_EULER_ANCESTRAL", "K_HEUN", "K_LMS"
    ], index=6)
    
    st.divider()
    st.markdown("Feito com ❤️ e um pouco de magia usando [Stability AI](https://stability.ai/)")

# Container mágico principal
st.markdown('<div class="magic-container">', unsafe_allow_html=True)

# Cabeçalho animado
st.markdown('<h1 class="magic-title">✨ Gerador Mágico de Imagens</h1>', unsafe_allow_html=True)
st.markdown('<p class="magic-subtitle">Transforme suas ideias em arte com IA</p>', unsafe_allow_html=True)

# Inicializa o histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=GIF_AVATAR_URL if message["role"] == "assistant" else None):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], use_column_width=True, output_format="PNG", caption="Imagem gerada pela magia da IA")

# Função para traduzir para inglês
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, dest='en')
        return translation.text
    except:
        return text

# Função para gerar imagens usando a API do Stability AI
def generate_image_with_stability(prompt, api_key, cfg_scale, steps, width, height, sampler):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = "https://api.stability.ai"
    
    english_prompt = translate_to_english(prompt)
    
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{"text": english_prompt}],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
            "sampler": sampler,
        },
    )

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.text}")
    
    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    return Image.open(io.BytesIO(image_data))

# Input do usuário
if prompt := st.chat_input("Descreva a imagem mágica que deseja criar..."):
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "type": "text"
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if not api_key:
        st.error("Por favor, insira sua chave da API Stability AI")
        st.stop()
    
    with st.chat_message("assistant", avatar=GIF_AVATAR_URL):
        with st.spinner("Conjurando sua imagem mágica..."):
            try:
                generated_image = generate_image_with_stability(
                    prompt=prompt,
                    api_key=api_key,
                    cfg_scale=cfg_scale,
                    steps=steps,
                    width=width,
                    height=height,
                    sampler=sampler
                )
                
                st.image(generated_image, use_column_width=True, output_format="PNG", caption="Sua imagem mágica foi conjurada!")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": generated_image,
                    "type": "image"
                })
                
                img_byte_arr = io.BytesIO()
                generated_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                st.download_button(
                    label="📥 Baixar Imagem Mágica",
                    data=img_byte_arr,
                    file_name=f"imagem_magica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"O feitiço falhou: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"O feitiço falhou: {str(e)}",
                    "type": "text"
                })

# Seção de exemplos
st.divider()
st.markdown("### 📜 Grimório de Exemplos")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🏰 Retrato Encantado**")
    st.code("Um retrato realista de uma fada anciã com olhos sábios e asas brilhantes, detalhes intrincados, iluminação suave")

with col2:
    st.markdown("**🌌 Paisagem Mágica**")
    st.code("Uma floresta encantada com árvores bioluminescentes e criaturas mágicas, estilo de conto de fadas, cores vibrantes")

with col3:
    st.markdown("**🐉 Arte de Feitiço**")
    st.code("Um dragão cósmico feito de estrelas e nebulosas, detalhes complexos, fundo de galáxia, estilo de arte conceitual fantástica")

# Fecha o container mágico
st.markdown('</div>', unsafe_allow_html=True)