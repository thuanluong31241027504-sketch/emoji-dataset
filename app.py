import streamlit as st
import numpy as np
from keras.models import load_model
from PIL import Image

st.set_page_config(page_title="Emoji AI", page_icon="🎨")

st.title("🎨 Nhận diện Emoji vẽ tay")

@st.cache_resource
def load_emoji_model():
    return load_model('emoji_modelqh.h5')

try:
    model = load_emoji_model()
    st.success("✅ Model đã tải thành công")
except Exception as e:
    st.error(f"❌ Lỗi tải model: {e}")
    st.stop()

classes = ["☁️ Cloud", "👍 Thumb", "❤️ Heart", "😈 Smiling Horns", "😃 Grinning Face"]

uploaded_file = st.file_uploader("Chọn ảnh vẽ tay", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.spinner("Đang xử lý..."):
        img = Image.open(uploaded_file).convert('L')
        img = img.resize((28, 28))
        img_array = np.array(img, dtype=np.float32)
        img_array = 255 - img_array
        img_array = img_array.reshape(1, 784) / 255.0
        
        pred = model.predict(img_array, verbose=0)
        idx = np.argmax(pred[0])
        confidence = pred[0][idx]
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Ảnh bạn vừa tải", width=200)
    with col2:
        st.success(f"### {classes[idx]}")
        st.metric("Độ tin cậy", f"{confidence*100:.1f}%")
