import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image

st.set_page_config(page_title="Emoji AI", page_icon="🎨", layout="centered")

# CSS riêng, để nguyên string
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #e0e0e0;
        margin-bottom: 2rem;
    }
    .result-box {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
    }
    .emoji-big {
        font-size: 5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">🎨 AI Nhận diện Emoji</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Vẽ tay – Nhận diện thông minh</p>', unsafe_allow_html=True)

@st.cache_resource
def load_emoji_model():
    return load_model('emoji_modelqh.h5')

model = load_emoji_model()
classes = ["☁️ Cloud", "👍 Thumb", "❤️ Heart", "😈 Smiling Horns", "😃 Grinning Face"]

uploaded_file = st.file_uploader("Chọn ảnh vẽ tay", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('L')
    img = img.resize((28, 28))
    img_array = np.array(img)
    img_array = 255 - img_array
    img_array = img_array.reshape(1, 784).astype('float32') / 255.0
    
    pred = model.predict(img_array, verbose=0)
    idx = np.argmax(pred[0])
    confidence = pred[0][idx]
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Ảnh bạn vừa tải", width=200)
    with col2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="emoji-big">{classes[idx].split()[0]}</div>
                <h2>{classes[idx]}</h2>
                <p>Độ tin cậy: <strong>{confidence*100:.1f}%</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
