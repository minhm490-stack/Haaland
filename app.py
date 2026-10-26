import os
import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(
    page_title="Khánh Hoà Photobooth", 
    page_icon="🌸", 
    layout="centered"
)

st.title("🌸 Khánh Hoà Photobooth - Tone Hồng Pastel 🌸")
st.write("Hãy dùng webcam chụp lần lượt **4 bức ảnh** để tạo khung hình kỷ niệm siêu xinh nhé!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Khung chụp 1")
    cam1 = st.camera_input("Ảnh 1")
    cam2 = st.camera_input("Ảnh 2")

with col2:
    st.subheader("📸 Khung chụp 2")
    cam3 = st.camera_input("Ảnh 3")
    cam4 = st.camera_input("Ảnh 4")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("✨ Tạo Khung Ảnh Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGB"))

            # --- CẤU HÌNH KHUNG VUÔNG & TÔNG MÀU HỒNG PASTEL (THEO ẢNH 2) ---
            canvas_w = 600
            canvas_h = 750  # Kích thước khung tổng thể cân đối dạng dọc/vuông
            
            # Tông màu hồng pastel & trắng hoa tulip
            bg_color = (255, 245, 247, 255)       # Hồng phấn rất nhạt làm nền
            border_color = (248, 187, 208, 255)   # Hồng pastel ngọt ngào
            frame_bg = (255, 255, 255, 255)       # Nền trắng cho khung ảnh nhỏ
            text_color = (216, 112, 147, 255)     # Hồng đậm vintage

            canvas = Image.new("RGBA", (canvas_w, canvas_h), bg_color)
            draw = ImageDraw.Draw(canvas)

            # Vẽ viền ngoài trang trí
            draw.rectangle([(15, 15), (canvas_w - 15, canvas_h - 15)], outline=border_color, width=4)

            try:
                font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
                font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
            except IOError:
                font_title = font_sub = ImageFont.load_default()

            # --- TIÊU ĐỀ ---
            draw.text((canvas_w // 2, 45), "💖 KHÁNH HOÀ PHOTOCARD 💖", fill=text_color, font=font_title, anchor="mm")
            draw.text((canvas_w // 2, 75), "🌸 Memories of You & Me 🌸", fill=(220, 150, 17
