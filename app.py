import os
import io
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(
    page_title="Khanh Hoa Photobooth", 
    page_icon="🔥", 
    layout="centered"
)

st.title("Khanh Hoa Photobooth - Haaland & MCK")
st.write("Hay dung webcam chụp lần lượt 4 bức ảnh để ghép vào khung!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Khung chụp 1")
    cam1 = st.camera_input("Anh 1 (Tren trai)")
    cam2 = st.camera_input("Anh 2 (Duoi trai)")

with col2:
    st.subheader("Khung chụp 2")
    cam3 = st.camera_input("Anh 3 (Tren phai)")
    cam4 = st.camera_input("Anh 4 (Duoi phai)")

captured_list = [cam1, cam2, cam3, cam4]

if all(captured_list):
    if st.button("Ghep Anh Vao Khung Ngay", type="primary"):
        try:
            webcam_images = []
            for f in captured_list:
                f.seek(0)
                webcam_images.append(Image.open(f).convert("RGBA"))

            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "khung.png")
            
            if not os.path.exists(template_path):
                st.error("Khong tim thay file khung.png tren GitHub!")
            else:
                base_image = Image.open(template_path).convert("RGBA")
                
                # Tọa độ chuẩn xác mới khớp hoàn toàn với 4 ô trống của khung mới
                box_coords = [
                    (247, 270, 485, 492),  # Ô 1: Trên - Trái
                    (521, 270, 759, 492),  # Ô 2: Trên - Phải
                    (247, 532, 485, 754),  # Ô 3: Dưới - Trái
                    (521, 532, 759, 754)   # Ô 4: Dưới - Phải
                ]

                for i
